# Indeed-Job-Scraper
Scrapes indeed job posts using advanced search feature of indeed.com

**Description***
Indeed.py contains the whole source code for this automation, result-.json contains the scraped results againset the user entered query. This script uses proxies from proxy_list.txt
When user searches on indeed it returns a web page containing listings of matching jobs but each job post is loaded in an iframe when clicked. To bypass this problem instead of using requests or urllib, I used selenium as creates a new instance of browser hence the page will behave as if in a real browser.

***Usage***
Input to indeed.py is passed using command line arguments. It takes input in the form of dictionary item. There are five flags for which values can be set.
1 *-ttl* used to set job title in indeed.py
2 *-jt* used to set job type in category
3 *-rad* used to define within radius of jobs
4 *-age* used to define the age of job
5 *-loc* used to set the location in query

*Example command to invoke script would be something like*

```$ python3 indeed.py -ttl "Python Developer" -jt all -rad 10 -age any -loc "New York"```

The above command searches for Python Developer jobs of all type within 10 miles radius of New york from any time.
There is no specific order in passing the arguments but you'll have to use the switches *-ttl, -jt, -rad, -age, -loc* to pass a value correctly otherwise script won't recognize it and a default value will be used.

*-ttl* 
switch expects a string value to be used as job title in search query. Note, if value contains a space, enclose the value in double or single quotes

*-jt*
switch expects any value from below mentioned list
```[all, commisions, contract, intenship, fulltime, parttime, temporary]```

*-rad*
expects a value of type int which uses below mentioned conventions
```
0 = only in
5 = 5mi
10 = 10mi
15 = 15mi
15 = 25mi
50 = 50mi
100 = 100mi
```

*-age* 
switch expects a value as per mentioned in below convention
```
any = anytime
15 = within 15 days 
7 = within 7 days
3 = within 3 days
1 = since yesterday
last = since my last visit
```

*-loc*
switch expects a string value for location


***Requirements***

python 3.x
selenium
random_user_agent


*chromedriver should be placed in the directory as indeed.py*
