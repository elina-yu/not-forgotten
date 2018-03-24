#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy, time, sys
import numpy as np
import pandas as pd
import calendar
from datetime import datetime

#Dataframe - basically an excel table

#Returns [number of incidents, casualties, injured given a date and a dataframe
def incidentsSince(date, df):
	df1 = df[df['Date'] > date]
	return [len(df1), df1['Deaths'].sum()]

#Input file here
fileName = 'schoolShootingData.csv'

#These are the keys we're going to use to access the twitter bot
CONSUMER_KEY = 'G9fqSBjRt5QKKdLSLG9aY9W7m'
CONSUMER_SECRET = 'c95Fx2wjpRdVQL1hxChkWVdtrX7wdFx9lUouJgoUdUuUgWmm2b'
ACCESS_KEY = '977333848362033152-PJBsxxpHN2hV4mReieonKqCBjTEoqSp'
ACCESS_SECRET = 'fY9z97EeNa5IkPRGKcegM0NsKr3rdRcUZDP5MNV2FpehN'

#Here we're accessing our bot using our keys
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

#The API is the collection of all the data Twitter has to offer, and here we're looking for tweets that @ us
api = tweepy.API(auth)
twt = api.search(q= "@NotForgottenBot")

dates = []

#Importing our CSV into a dataframe
df = pd.read_csv(fileName)

#Here we're converting the dates from Strings to datatimes so they're easier to compare
for date in df['Date']:
	datetime_object = datetime.strptime(date, '%B %d, %Y')
	dates.append(datetime_object)
del df['Date']
df.insert(0, 'Date', dates)

#Keywords we're looking for 
t = ['since', 'last']

#Loop through all tweets mentioning us (twts)
for s in twt:
	#Check for each of our keywords
	for i in t:
		if i in s.text:
			try:
				'''Splitting the incoming tweet so that we can find the date they're looking for,
				then try to convert to datetime'''
				splittext = s.text.split()
				dateRequested = splittext[2]
				try:
					dateRequested = datetime.strptime(dateRequested, '%Y-%m-%d')
				except ValueError:
					print(dateRequested + " is not a date.")

				sn = s.user.screen_name

				#Formatting and delivering our tweet
				replyData = incidentsSince(dateRequested, df)
				numShootings = replyData[0]
				numCasualties= replyData[1]
				numInjuries = 0
				tweetFormat = "Incidents: {}\nInjuries: {}\nCasualties: {}\n"
				statusUpdate = tweetFormat.format(numShootings, numInjuries, numCasualties)
				m = "@{} {} #NeverAgain"
				s = api.update_status(m.format(sn, statusUpdate), s.id)
			except tweepy.error.TweepError as e:
				print("Already replied to.")
				continue
