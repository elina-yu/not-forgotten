import tweepy, time, sys

# datafile = ''#filename

CONSUMER_KEY = 'G9fqSBjRt5QKKdLSLG9aY9W7m'
CONSUMER_SECRET = 'c95Fx2wjpRdVQL1hxChkWVdtrX7wdFx9lUouJgoUdUuUgWmm2b'
ACCESS_KEY = '977333848362033152-PJBsxxpHN2hV4mReieonKqCBjTEoqSp'
ACCESS_SECRET = 'fY9z97EeNa5IkPRGKcegM0NsKr3rdRcUZDP5MNV2FpehN'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# filename=open(datafile,'r')

twt = api.search(q= "@NotForgottenBot")

#list of specific strings we want to check for in Tweets
t = ['since',
    'last'] 

# if "since xx/xx/xxxx", do this

# if "last... (yrs, mos, weeks), do this
numShootings = 0
numInjuries= 0
numCasualties=0

tweetFormat = "Incidences: {}\nInjuries: {}\nCasualties: {}\n"
statusUpdate = tweetFormat.format(numShootings, numInjuries, numCasualties)


for s in twt:
	for i in t:
		if i in s.text:
			try:
				print("Original tweet: " +s.text)
				sn = s.user.screen_name
				m = "@{} {} #NeverAgain"
				s= api.update_status(m.format(sn, statusUpdate), s.id)
			except tweepy.error.TweepError as e:
				print("Already replied to.")
				continue
#filename.close()

