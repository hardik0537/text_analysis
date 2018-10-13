import tweepy
import socket
import re

class TwitterStreamListener(tweepy.StreamListener):
        
	def __init__(self, sc):
        super(TwitterStreamListener, self).__init__()
        self.client_socket = sc

    def on_status(self, status):
		tweet = self.get_tweet(status)
        self.client_socket.send((tweet[2]+"\n").encode('utf-8'))
        return True

    # Twitter error list : https://dev.twitter.com/overview/api/response-codes
    def on_error(self, status_code):
        print("Status code")
		print(status_code)
		if status_code == 403:
			print("The request is understood, but the access is not allowed. Limit may be reached.")
			return False

    def get_tweet(self,tweet):
        text = tweet.text
		if hasattr(tweet, 'extended_tweet'):
			text = tweet.extended_tweet['full_text']
		return [str(tweet.user.id),tweet.user.screen_name,self.clean_str(text)]

    def clean_str(self, string):
            
        string = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "", string, re.I | re.U)
		string = re.sub(r"\n|\t", " ", string)
		string = re.sub(r"(.)\1{2,}", r"\1\1", string)
		string = re.sub(r"(..)\1{2,}", r"\1\1", string)
		string = re.sub(r"(...)\1{2,}", r"\1\1", string)
		string = re.sub(r"(....)\1{2,}", r"\1\1", string)
		string = re.sub(r'RT ', '', string)
		return string

if __name__ == '__main__':
	# Authentication
        
    consumer_key = "82Li938chvcKlOKxQaexOU1nE"
    consumer_secret = "fxdQMmefCTULkBhAw8IlWYVji2uWho7qvsKk5upCyF2T99IN8F"
    access_token = "1002939150918701060-7kYXJPvvljP5J15v3rRUvGKk3gW1KG"
    access_token_secret = "eQgmhhFMcQ9i9a7deBy58DoyeSRDzcUmPmQ0MKODqJSgp"

    # Local connection
    host = "10.0.0.4"          # Get local machine name (copy internal address from EC2 instance).
    port = 5557                 # Reserve a port for your service.

    s = socket.socket()         # Create a socket object.
    s.bind((host, port))        # Bind to the port.

    print("Listening on port: %s" % str(port))

    s.listen(5)                 # Now wait for client connection.
    c, addr = s.accept()        # Establish connection with client.

    print("Received request from: " + str(addr))
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

    streamListener = TwitterStreamListener(c)
    myStream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')
    myStream.filter(track=['movie','movies'], async=True)
