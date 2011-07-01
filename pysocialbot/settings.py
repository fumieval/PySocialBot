"""
PySocialBot Settings
"""
import os
#--- Core Settings ---

#The interval to check the trigger.
#If this value is too low, the daemon may strain your CPU.
RUN_INTERVAL = 0.2

#--- Twitter Settings ---

#The file that is saving access token.
TW_USER_DB_PATH = os.environ['HOME'] + "/.pysocialbot/twitter/user.db"

#The number of retries when the api failed to access.
TW_RETRY_COUNT = 3

#The interval of retries when the api failed to access.
TW_RETRY_INTERVAL = 1.0

#Consumer Key and Consumer Secret. You don't have to change these settings.
TW_CONSUMER_KEY = "xEB1KUCy0V2eGK7fUp9b9g"
TW_CONSUMER_SECRET = "13hzGL3DXKvApQGjKrFQvNObVA4iDWZgM4wEpLIS44"

#You don't have to change these settings.
TW_REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
TW_ACCESS_TOKEN_URL  = "https://api.twitter.com/oauth/access_token"
TW_AUTHORIZATION_URL = "https://api.twitter.com/oauth/authorize"
TW_SIGNIN_URL = "https://api.twitter.com/oauth/authenticate"