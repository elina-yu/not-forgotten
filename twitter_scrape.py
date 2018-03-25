#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 16:14:20 2018

@author: esther
"""

# =============================================================================
# Use selenium and webdriver to access a twitter refined search page
# The twitter search is refined by key phrase "school shooting"
# Twitter search also refined by day
# We want to use this program to create a data file containing
# the number of tweets about "school shooting" per day
# =============================================================================

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import time, csv, datetime


# return True if year is leapyear
def is_leap_year(year):
	if (year % 4 == 0):
		if (year % 100 == 0):
			if (year % 400 == 0):
				return True
		else:
			return True
	return False

# check if last day or month/year and go to next day
def next_day(year, month, day):
    if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
        if (day == 31):
            if (month == 12):
                year+=1
                month=1
                day=1
            else:
                month+=1
                day=1
        else:
            day+=1
    elif (month == 4 or month == 6 or month == 9 or month == 11):
        if (day == 30):
            month+=1
            day=1
        else:
            day+=1
    elif (month == 2):
        if (is_leap_year(year)):
            if (day == 29):
                month+=1
                day=1
            else:
                day+=1
        else:
            if (day == 28):
                month+=1
                day=1
            else:
                day+=1
    return year, month, day

# check if next day is current day
def check_next_day(year, month, day):
    today = datetime.datetime.now()
    year, month, day = next_day(year, month, day)
    if (today.year == year and today.month == month and today.day == day):
        return True
    else:
        return False
        
# add date into link for since date
def since_date(year, month, day):
    if (month < 10):
        strline = "since%3A"+ str(year) + "-0" + str(month) + "-" + str(day)
        return strline
    else:
        strline = "since%3A"+ str(year) + "-" + str(month) + "-" + str(day)
        return strline 

# add date into link for until date
def until_date(year, month, day):
    year, month, day = next_day(year, month, day)
    
    if (month < 10):
        strline = "%20until%3A" + str(year) + "-0" + str(month) + "-" + str(day)
        return strline
    else:
        strline = "%20until%3A" + str(year) + "-" + str(month) + "-" + str(day)
        return strline
  
# get data for next day      
def next_day_data(year, month, day):
    while (check_next_day(year, month, day) == False):
        year, month, day = next_day(year, month, day)
        row = []
        data = []
        data.append(year)
        data.append(month)
        data.append(day)
        base = u'https://twitter.com/search?l=&q='
        query = u'"school%20shooting"%20'
        url = base+query+since_date(year, month, day)+until_date(year, month,day)
        
        option = webdriver.ChromeOptions()
        option.add_argument(" - incognito")
    
        # open browser
        driver = webdriver.Chrome(executable_path='/Users/esther/Desktop/chromedriver', chrome_options=option)
        
        # open website
        driver.get(url)
        time.sleep(1)
    
        body = driver.find_element_by_tag_name('body')
    
        for i in range(100):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            
        num_tweets = 0
    
        tweets = driver.find_elements_by_class_name('TweetTextSize')
        for tweet in tweets:
            num_tweets+=1
        driver.close()
            
        data.append(num_tweets)
        row.append(data)
        
        ## ADD TO CSV
        csvfile = open("twitter_data.csv", "a")
        writer = csv.writer(csvfile)
        writer.writerows(row)
        csvfile.close()    
    
# main method
def main():
    # start date is twitter start date march 21, 2006
    #year = 2006
    #month = 3
    #day = 21
    year = 2018
    month = 3
    day = 22
    row = []
    data = []
    data.append(year)
    data.append(month)
    data.append(day)
    row.append(["Year", "Month", "Day", "Count"])
    
    base = u'https://twitter.com/search?l=&q='
    query = u'"school%20shooting"%20'
    url = base+query+since_date(year, month, day)+until_date(year, month,day)
    
    option = webdriver.ChromeOptions()
    option.add_argument(" - incognito")

    # open browser
    driver = webdriver.Chrome(executable_path='/Users/esther/Desktop/chromedriver', chrome_options=option)
    
    # open website
    driver.get(url)
    time.sleep(1)

    body = driver.find_element_by_tag_name('body')

    for i in range(100):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        
    num_tweets = 0

    tweets = driver.find_elements_by_class_name('TweetTextSize')
    for tweet in tweets:
        num_tweets+=1
    driver.close()
        
    data.append(num_tweets)
    row.append(data)
    
    ## ADD TO CSV
    csvfile = open("twitter_data.csv", "w")
    
    writer = csv.writer(csvfile)
    writer.writerows(row)
    csvfile.close()
    
    next_day_data(year, month, day)
    
    
main()

    
    
    
    
    
    
