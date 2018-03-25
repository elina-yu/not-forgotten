#tweets out anniversary incidents
from datetime import datetime
import tweepy 
import pandas as pd

today = datetime.date.today()

#returns csv line numbers of incidents on this day into tweets[] given today's date, an array of dates from the csv  
def anniversary(today, dates, tweets):
	for i in dates:
		if ((datetime.strptime(today, "%m-%d").date()) == (dates[i])):
			tweets.append(i)
	
#Input file here
fileName = 'wikipedia_school_shooting.csv'
df = pd.read_csv(fileName)

dates= []
tweets = [] 
#Here we're converting the dates from Strings to datatimes so they're easier to compare
for date in df['Date']:
        datetime_object = datetime.strptime(date, "%m-%d").date()
	test = "Test {}"
	print(test.format(datetime_object))
        dates.append(datetime_object)
del df['Date']
df.insert(0, 'Date', dates)
	
anniversary(today, dates)

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

