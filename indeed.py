#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.utils import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import TimeoutException, WebDriverException

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

import os
import random
import re
import sys
import json
import time

class ProxyAddress:
    
    def __init__(self):
        self.top = 0

    def get_proxy(self):
        with open("proxy_list.txt") as f:
            try:
                proxy = f.readlines()[self.top].strip()
                self.top += 1
                print(f"proxy: {proxy}")
                return proxy
            except:
                self.top = 0


class Request:
    selenium_retries = 0

    #region general browser related stuff
    def __init__(self, url):
        self.url = url
        self.driver = self.get_selenium_res()


    def get_selenium_res(self):
        try:
            proxy = ip.get_proxy()
            exec_path = os.path.join(os.getcwd(), "chromedriver")
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MACOS.value]
            user_agent_rotator = UserAgent(software_name=software_names, operating_systems=operating_systems, limit=100)
            user_agent = user_agent_rotator.get_random_user_agent()

            chrome_options = Options()
            chrome_options.add_argument(f"user-agent={user_agent}")
            #chrome_options.add_argument(f"--proxy-server={proxy}")
            
            driver = webdriver.Chrome(executable_path=exec_path, options=chrome_options)
            driver.get(self.url)

            time_to_wait = 90
            try:
                WebDriverWait(driver, time_to_wait).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
            finally:
                driver.maximize_window()
                return driver
            
        except (TimeoutException, WebDriverException):
            self.selenium_retries += 1
            print(f"initialization failed, retries: {self.selenium_retries}")
            self.get_selenium_res()
#endregion


#region specific scraper related extentions
    def begin_scrapping_jobs(self):
        self.scrape_jobs()
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Next']"))).click()
            self.begin_scrapping_jobs()
        except:
            print("all results scrapped")  


    def scrape_jobs(self):
        try:
            job_items = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-tn-component='organicJob']")))
            
            for item in job_items:
                self.popover_crtl()
                self.random_wait()
                
                item.location_once_scrolled_into_view
                item.click()
                try:
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "vjs-container-iframe")))
                    self.driver.switch_to.frame("vjs-container-iframe")
                    job_posts.append(self.scrape_job_frame())
                    self.driver.switch_to.default_content()
                except:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "vjs-container")))
                    self.scrape_job_post()
                finally:
                    self.random_wait()
        except:
            print(f"Unable to scrape job posts from the page {self.driver.current_url}")


    def scrape_job_post(self):
        print("extreme condions")
        

    def scrape_job_frame(self):
        job_post = {}
        job_post["job_type"] = "null"

        try:
            job_post["job_type"] = self.driver.find_element_by_css_selector("#jobDetailsSection > div.jobsearch-JobDescriptionSection-sectionItem").text#.split("\n")[1]
        finally:
            job_post = self.get_header_details()
            job_post["post_src"] = self.driver.find_element_by_id("applyButtonLinkContainer").find_element_by_tag_name("a").get_attribute("href")
            job_post["job_desc"] = self.driver.find_element_by_id("jobDescriptionText").text
            job_post["timestamp"] = self.extract_timestamp()
            return job_post


    def get_header_details(self):
        header = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "jobsearch-JobComponent-embeddedHeader"))).text
        header_items = header.split("\n")
        new_header_items = []
        
        for item in header_items:
            if self.check_ignore_cases(item):
                new_header_items.append(item)    
        
        if len(new_header_items) == 3:
            new_header_items.append("null")
        
        header_details = {"title": new_header_items[0], "company": new_header_items[1], "job_loc": new_header_items[2], "job_cat": new_header_items[3]}
        return header_details


    def check_ignore_cases(self, item):
        ignore_cases = [" reviews", "Apply", "Save", "- job post"]
        
        if item == "-":
            return False
        
        for case in ignore_cases:
            if re.search(case, item) is not None:
                return False
            
        return True


    def random_wait(self):
        n = random.randint(2, 7)
        self.driver.implicitly_wait(n)


    def popover_crtl(self):
        try:
            self.driver.find_element_by_id("popover-x").click()
            print("popover detected")
        except:
            pass


    def extract_timestamp(self):
        text = self.driver.find_element_by_class_name("jobsearch-JobMetadataFooter").text
        patterns = ["([0-9]+[\\+]*\\sdays*\\sago)", "(Today)", "(Yesterday)", "Just Posted"]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match is not None:
                return match.group(0)


    def close(self):
        self.driver.close()

#endregion


def run():
    request = Request(f"https://www.indeed.com/jobs?as_and=&as_phr=&as_any=&as_not=&as_ttl={args['title']}&as_cmp=&jt={args['job_type']}&st=&salary=&radius={args['radius']}&l={args['job_loc']}&fromage={args['job_age']}&limit=20&sort=&psf=advsrch&from=advancedsearch")
    request.random_wait()
    request.begin_scrapping_jobs()
    request.close()

    del request

def parse_args():
    _args = {"title":"python", "job_type":"all", "radius":"100", "job_age":"any", "job_loc":"New+York"}
    for item in range(1, len(sys.argv), 2):
        if sys.argv[item] == "-ttl":
            _args["title"] = sys.argv[item+1].replace(" ", "+")
        elif sys.argv[item] == "-jt":
            _args["job_type"] = sys.argv[item+1]
        elif sys.argv[item] == "-rad":
            _args["radius"] = sys.argv[item+1]
        elif sys.argv[item] == "-age":
            _args["job_age"] = sys.argv[item+1]
        elif sys.argv[item] == "-loc":
            _args["job_loc"] = sys.argv[item+1].replace(" ", "+")
    return _args


def write_output():
    with open(f"results-{args['title']}-{args['job_loc']}-{str(time.time())}.json", "w") as f:
        json.dump(job_posts, f, indent=4)


ip = ProxyAddress()
job_posts = []
args = parse_args()
run()
print(job_posts)
write_output()



