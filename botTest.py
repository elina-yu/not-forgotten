import tweepy, time, sys

# datafile = ''#filename

CONSUMER_KEY = 'G9fqSBjRt5QKKdLSLG9aY9W7m'
CONSUMER_SECRET = 'c95Fx2wjpRdVQL1hxChkWVdtrX7wdFx9lUouJgoUdUuUgWmm2b'
ACCESS_KEY = '977333848362033152-PJBsxxpHN2hV4mReieonKqCBjTEoqSp'
ACCESS_SECRET = 'fY9z97EeNa5IkPRGKcegM0NsKr3rdRcUZDP5MNV2FpehN'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

twt = api.search(q="@NotForgottenBot")

for s in twt:
	print(s.text)
	sn = s.user.screen_name
	m = "@%s Test" % (sn)
	s = api.update_status(m, s.id)


'''
TODO: Save answered tweets in a database and check to see if I've replied to it
Retrieve data from recent school shootings and adapt to tweets
'''
