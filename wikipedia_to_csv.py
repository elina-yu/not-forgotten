#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 19:32:28 2018

@author: esther
"""

###### THIS CODE IS SPECIFIC TO THE WIKIPEDIA PAGE ######


from bs4 import BeautifulSoup
import urllib.request
import csv

# make a request to a web server and store the response
response = urllib.request.urlopen("https://en.wikipedia.org/wiki/List_of_school_shootings_in_the_United_States")

# convert the response to a string
html = response.read() 

soup = BeautifulSoup(html, "lxml")

all_rows = []

# boolean for if header has been added
header = False
# column number
column = 0


#loop through all the <tr> tags in the HTML code
for tr in soup.findAll('tr'):
    row = []
    
    # add the table headers
    if header == False:
        for th in tr.findAll('th'):
        # add the table headers
            row.append(th.contents[0])
        # header is now added
        header = True
        column+=1
        
    # add all the table data values of one row into a list
    for td in tr.findAll('td'):
        if column == 0:
            # some date columns aren't in spans
            if (len(td.find_all('span')) > 1):
                td.contents[0].replace_with('')
                for span in td.findAll('span'):
                    row.append(span.contents[0])
            else:
                row.append(td.contents[0])
        elif column == 1:
            row.append(td.find('a').contents[0])
        elif column == 2 or column == 3:
            row.append(td.contents[0])
        elif column == 4:
            row.append(td.get_text())
        column+=1
        
    if column == 0:
        # dont append because there's nothing
        continue
    else:
        # add the row into list of all rows
        all_rows.append(row)
        
    # reset columns
    column = 0
    
## CONVERT TO CSV
csvfile = open("wikipedia_school_shooting.csv", "w")

writer = csv.writer(csvfile)
writer.writerows(all_rows)
csvfile.close()
