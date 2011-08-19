"""
Registering access key/token
"""
from urlparse import parse_qsl

import shelve
import oauth2 as oauth

from pysocialbot.misc import apply_settings
from pysocialbot.settings import (TW_CONSUMER_KEY, TW_CONSUMER_SECRET,
                                  TW_USER_DB_PATH,
                                  TW_REQUEST_TOKEN_URL,
                                  TW_ACCESS_TOKEN_URL,
                                  TW_AUTHORIZATION_URL)

def user_database():
    """Get access token from database."""
    return shelve.open(TW_USER_DB_PATH)


def instant_auth():
    """instant authenticate."""
    auth_result = auth()
    if auth_result:
        return auth_result[1]
    else:
        raise StandardError("Authentication Failure")
    
def auth():
    "Authenticate to twitter and get access token."
    apply_settings()
    #signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
    oauth_consumer = oauth.Consumer(key=TW_CONSUMER_KEY,
                                    secret=TW_CONSUMER_SECRET)
    oauth_client = oauth.Client(oauth_consumer)
    resp, content = oauth_client.request(TW_REQUEST_TOKEN_URL, 'GET')
    
    if resp['status'] == '200':
        request_token = dict(parse_qsl(content))
        print('Please get the PIN Code from the following URL.')
        print('%s?oauth_token=%s' % (TW_AUTHORIZATION_URL,
                                     request_token['oauth_token']))
        try:
            pincode = raw_input('PIN Code:')
        except NameError:
            pincode = input('PIN Code:')
    
        print('Getting Access Token...')
        token = oauth.Token(request_token['oauth_token'],
                            request_token['oauth_token_secret'])
        token.set_verifier(pincode)
    
        oauth_client  = oauth.Client(oauth_consumer, token)
        resp, content = oauth_client.request(TW_ACCESS_TOKEN_URL,
                                             method='POST',
                                             body='oauth_verifier=%s' % pincode)
        
        access_token  = dict(parse_qsl(content))
        
        if resp['status'] == '200':
            print("Authenticated successfully: @%s." % access_token['screen_name'])
            return access_token['screen_name'], (access_token['oauth_token'],
                                                 access_token['oauth_token_secret'])
        else:
            print("Couldn't get the token: status %s" % resp['status'])
            return None
    else:
        print('There was no response from twitter: status %s' % resp['status'])
        return None

def register():
    """Regist access token to database."""
    apply_settings()
    
    auth_result = auth()
    if auth_result:
        screen_name, (access_token, access_token_secret) = auth_result
        user_db = shelve.open(TW_USER_DB_PATH)
        user_db[screen_name] = access_token, access_token_secret
        user_db.sync()
        
        print("Registered: @%s" % screen_name)
        return 0, screen_name