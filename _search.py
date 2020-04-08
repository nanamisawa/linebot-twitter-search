import json, config
from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)    # 認証

url = "https://api.twitter.com/1.1/search/tweets.json"
print('----------------------------------------------------')
params = {'q' : "池袋 ラーメン", 'count' : 5}
req = twitter.get(url, params = params)

if req.status_code == 200:
    search_timeline = json.loads(req.text)
    for tweet in search_timeline['statuses']:
        print(tweet['user']['name'] + '::' + tweet['text'])
        print(tweet['created_at'])
        # いずれgeo情報でマップ表示したい。
        if 'geo' in tweet and tweet['geo'] is not None :
            print("**********", tweet['geo'])

        print('----------------------------------------------------')
else:
    print("ERROR: %d" % req.status_code)