# coding:utf-8
"""
PySocialBot Twitter API

todo: support proxy
"""
from __future__ import unicode_literals

import itertools
import tweepy
import re
import xml.sax.saxutils

from pysocialbot.twitter.register import user_database, instant_auth
from pysocialbot.settings import (TW_RETRY_INTERVAL, TW_RETRY_COUNT,
                                  TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
from pysocialbot.util import retry, convert_class
from pysocialbot.struct import Object

RETRY = retry(tweepy.error.TweepError,
              TW_RETRY_INTERVAL, TW_RETRY_COUNT)

ENTITIES = re.compile("RT @\w+.*|\.(@\w+ )+|http:\/\/(\w+|\.|\/)*|(^|\s)#.+($|\s)|@\w+")

def cuser(obj):
    """convert object to user."""
    return convert_class(obj, User)
def cstatus(obj):
    """convert object to user."""
    return convert_class(obj, Status)

class Api():
    
    """Twitter API."""
    
    def __init__(self, auth_name=None):
        """Authenticate and initialize."""
        if auth_name:
            access_token, access_token_secret = user_database()[auth_name]
        else:
            access_token, access_token_secret = instant_auth()
        
        self.auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
        self.auth.set_access_token(access_token, access_token_secret)
        
        self.api = tweepy.API(auth_handler=self.auth)
        
        self.following = []
        self.followers = []
        
    def post(self, text):
        """update status."""
        return RETRY(lambda: cstatus(self.api.update_status(text)))()
    
    def timeline(self, page=0):
        """get timeline."""
        home = self.api.friends_timeline(page=page)
        return RETRY(lambda: map(cstatus, home))()
    
    def mentions(self, page=0):
        """get timeline."""
        return RETRY(lambda: map(cstatus, self.api.mentions(page=page)))()
    
    
    def reply(self, status_id, text):
        """reply to status user_id."""
        return RETRY(lambda: cstatus(self.api.update_status(text, status_id)))()
    
    def retweet(self, status_id):
        """retweet status."""
        return RETRY(lambda: cstatus(self.api.retweet(status_id)))()
            
    def informalretweet(self, status, text):
        """informal retweet."""
        text_ = "%s RT @%s: %s" % (text,
                                   status.user.screen_name,
                                   status.text)
        return RETRY(lambda: cstatus(self.api.update_status(text_)))()
    
    def favorite(self, status_id):
        """Create favorite."""
        return RETRY(lambda: bool(self.api.create_favorite(status_id)))()
    
    def status(self, status_id):
        """Get status from user_id."""
        return RETRY(lambda: cstatus(self.api.get_status(status_id)))()
            
    def follow(self, user_id):
        """Follow the user."""
        return RETRY(lambda: cuser(self.api.create_friendship(user_id)))()
        
    def remove(self, user_id):
        """Remove(unfollow) the user."""
        return RETRY(lambda: cuser(self.api.destroy_friendship(user_id)))()
    
    def updatefriends(self):
        """Update friends list."""
        def retrycall(f):
            return RETRY(lambda: f())()
        self.following = retrycall(self.api.friends_ids)
        self.followers = retrycall(self.api.followers_ids)

    def unrewarded(self):
        """Return followers who is not followed by authenticated user."""
        return itertools.ifilterfalse(lambda x: x in self.following,
                                      self.followers)
        
    def unrequited(self):
        """Return friends who is not following authenticated user."""
        return itertools.ifilterfalse(lambda x: x in self.followers,
                                      self.following)

    def search(self, query, since_id):
        return RETRY(lambda: self.api.search(query, since_id=since_id))()

class User(Object):
    
    """User Object."""
    
    def __unicode__(self):
        return "@%s(%s)" % (self.screen_name, self.name)

class Status(Object):
    
    """Status Object."""
    
    def __unicode__(self):
        return "@%s: %s via %s" % (self.user.screen_name, self.text,
                                   self.source)
        
    def __repr__(self):
        return "http://twitter.com/#!/%s/status/%d" % (self.user.screen_name, self.id)

    def filter(self, items):
        new = Status()
        for attr in items:
            new.__dict__[attr] = self.__dict__[attr]

    def cleaned(self):
        return ENTITIES.sub("", xml.sax.saxutils.unescape(self.text)).strip()

STATUS_FILTER_MINIMAL=['user', 'text', 'source']
