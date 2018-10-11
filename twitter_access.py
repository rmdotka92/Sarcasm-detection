from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import tweepy


#consumer key, consumer secret, access token, access secret.

ckey = 'zrCt3iJOF3oBsEd5UrangR3Mj9'
csecret = 'SrdAQZNRc9WCe9gSXiIhXYmpLjiNWIU9kD0TB4yNaVgY3y9nRFT'
atoken = '1r006866381613215744-tmoYroVeXIyujSqdTVQhYwOSZzwFPC'
asecret = 'Rr07FOpQo1tuGR0lBAut6Y68YTBIZagTnJg9sfk51YqWtu'

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)
saveFile = open('twitDB_sarcasm.txt', 'a')

for tweet in tweepy.Cursor(api.search,
                           q="#sarcasm",
                           count=100,
                           result_type="mixed",
                           include_entities=True,
                           lang="en").items():
    if tweet.text[0:2] != 'RT':
        data = str(tweet.text.encode('ascii', 'ignore'))
        print(data)
        print("\n ================ \n")

        saveFile.write(data)
        saveFile.write('\n')

saveFile.close()




