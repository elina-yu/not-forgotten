#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy, time, sys
import numpy as np
import pandas as pd
import calendar
from datetime import datetime
from datetime import timedelta

#Dataframe - basically an excel table


#These are the keys we're going to use to access the twitter bot
CONSUMER_KEY = 'G9fqSBjRt5QKKdLSLG9aY9W7m'
CONSUMER_SECRET = 'c95Fx2wjpRdVQL1hxChkWVdtrX7wdFx9lUouJgoUdUuUgWmm2b'
ACCESS_KEY = '977333848362033152-PJBsxxpHN2hV4mReieonKqCBjTEoqSp'
ACCESS_SECRET = 'fY9z97EeNa5IkPRGKcegM0NsKr3rdRcUZDP5MNV2FpehN'
#Here we're accessing our bot using our keys
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

def parseIds(fileName):
	f = open(fileName, 'r')
	content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content] 
	return content

repliedIdsFile = 'repliedIds.txt'
repliedIds = parseIds(repliedIdsFile)

writeToFile = open(repliedIdsFile, 'a')


#Returns [number of incidents, casualties, injured given a date and a dataframe
def incidentsSince(date, df):
	df1 = df[df['Date'] > date]
	return [len(df1), df1['Deaths'].sum(), df1['Injuries'].sum()]
def switch(unit):
	switcher = {
		"days": 0,
		"weeks": 1,
		"months": 2,
		"years": 3,
	}
	return switcher.get(unit)

def lastIncidents(num, unit, df):
	units = [0,0,0,0]
	units[switch(unit)] = int(num)
	coef = [1,7, 30, 365]
	s1 = pd.Series(units)
	s2 = pd.Series(coef)
	s1 = s1.multiply(s2)
	d = datetime.today() - timedelta(days = sum(s1))
	return incidentsSince(d, df)

#Input file here
fileName = 'wikipedia_school_shooting.csv'


#The API is the collection of all the data Twitter has to offer, and here we're looking for tweets that @ us
api = tweepy.API(auth)
twt = api.search(q= "@NotForgottenBot")

dates = []

#Importing our CSV into a dataframe
df = pd.read_csv(fileName)
df['Injuries'].replace(['?', '1+'], 0, inplace = True)
df['Injuries'] = pd.to_numeric(df['Injuries'])
#Here we're converting the dates from Strings to datatimes so they're easier to compare
for date in df['Date']:
	datetime_object = datetime.strptime(date, '%B %d, %Y')
	dates.append(datetime_object)
del(df['Date'])
df.insert(0, 'Date', dates)

#Keywords we're looking for 
sinces = ['since', 'Since']
lasts = ['last', 'Last']
keywords = sinces + lasts

#Loop through all tweets mentioning us (twts)
for s in twt:
	#Check if we replied already
	if s.id_str in repliedIds:
		continue

	sn = s.user.screen_name
	if not (pd.Series(s.text.split()).isin(keywords).any()):
		try:
			api.update_status('@%s Use the keywords "since" or "last" to call the bot' % sn, s.id)
			continue
		except tweepy.error.TweepError as e:
			writeToFile.write(s.id_str + '\n')
			print("Already replied to.")
			continue


	#Check for each of our keywords
	
	'''Splitting the incoming tweet so that we can find the date they're looking for,
	then try to convert to datetime'''
	splittext = s.text.split()
	for i in sinces:
		if i in s.text:
			dateRequested = splittext[2]
			try:
				dateRequested = datetime.strptime(dateRequested, '%Y-%m-%d')
			except ValueError:
				try:
					api.update_status("@%s Tweet format: [keyword] [YYYY-mm-dd]" % sn, s.id)
				except tweepy.error.TweepError:
					print("Already replied to.")
					writeToFile.write(s.id_str + '\n')
				continue
			replyData = incidentsSince(dateRequested, df)
	for i in lasts:
		if i in s.text:
			num = splittext[2]
			unit = splittext[3]
			replyData = lastIncidents(num, unit, df)

	#Formatting and delivering our tweet
	
	numShootings = replyData[0]
	numCasualties= replyData[1]
	numInjuries = replyData[2]
	tweetFormat = "Incidents: {}\nInjuries: {}\nCasualties: {}\n"
	statusUpdate = tweetFormat.format(numShootings, numInjuries, numCasualties)
	m = "@{} {} #NeverAgain"
	try:
		s = api.update_status(m.format(sn, statusUpdate), s.id)
	except tweepy.error.TweepError as e:
		writeToFile.write(s.id_str + '\n')	
		print("Already replied to.")
		continue

	#Mark tweet as replied by adding to database
	writeToFile.write(s.id_str + '\n')

def getAnniv(df):
	anniv = []
	for i in df['Date']:
		if i.month == datetime.today().month and i.day == datetime.today().day:
			anniv.append(i)
	return anniv

# anniv = getAnniv(df)
# if len(anniv) > 0:
# 	for i in anniv:
# 		data = [dfa[i]['Date'], dfa[i]['Deaths'], dfa[i]['Location']]
# 		api.statusUpdate("On this day in %i, %i were killed in %s", data)
	
