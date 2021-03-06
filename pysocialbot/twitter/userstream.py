"""
PySocialBot Twitter UserStream
"""
from itertools import takewhile, repeat
try:
    from itertools import imap
except ImportError:
    imap = map

import urllib
import urllib2

import json
import threading

from pysocialbot.twitter import User, Status
from pysocialbot.util import convert_class
from pysocialbot.struct import Object

STREAM_URL = "https://userstream.twitter.com/2/user.json"

def convert_status(data):
    """convert dictionary to Status object."""
    result = convert_class(Object(data), Status)
    result.user = convert_class(Object(result.user), User)
    return result

def convert_user(data):
    """convert dictionary to User object."""
    return convert_class(Object(data), User)

def stream(api):
    """Get data from Twitter."""
    param = {"delimited": "length"}
    header = {}
    api.auth.apply_auth(STREAM_URL, "POST", header, param)
    
    req = urllib2.Request(STREAM_URL)
    req.add_header("Authorization", header["Authorization"])

    url = urllib2.urlopen(req, urllib.urlencode(param))
        
    while True:
        length = url.readline().strip()
        if length.isdigit():
            yield json.loads(url.readline())

class UserStream(threading.Thread):
    
    """UserStream daemon."""
    
    def __init__(self, api, handler):
        threading.Thread.__init__(self, name="UserStream")
        self.daemon = True
        self.api = api
        self.handler = handler

    def run(self):
        """Get stream and call handler."""
        for data in stream(self.api):
            if 'event' in data:
                event = data['event']
                if event == "follow":
                    self.handler.follow(convert_user(data["source"]))
                elif event == "favorite":
                    self.handler.favorite(convert_user(data["source"]))
                elif event == "unfavorite":
                    self.handler.unfavorite(convert_user(data["source"]))
                elif event == "list_member_added":
                    self.handler.list_add(convert_user(data["source"]))
                elif event == "list_member_removed":
                    self.handler.list_remove(convert_user(data["source"]))
                elif event == "block":
                    self.handler.block(convert_user(data["source"]))
                elif event == "user_update":
                    self.handler.user_update(convert_user(data["source"]))
                elif event == "list_user_subscribed":
                    pass
                else:
                    raise NameError("undefined event %s" % event)
            else:
                if 'user' in data and "id" in data:
                    self.handler.status(convert_status(data))

class StreamHandler():
    
    """UserStream event handler."""
    
    def __init__(self):
        pass
    def status(self, status):
        """call when recieve new status."""
        pass
    def follow(self, source):
        """call when someone followed the user."""
        pass
    def favorite(self, source):
        """call when someone faved the user's tweet."""
        pass
    def block(self, source):
        """call when the user blocks someone."""
        pass
    def unfavorite(self, source):
        """call when someone unfaved the user's tweet."""
        pass
    def list_add(self, source):
        """call when someone added the user to list."""
        pass
    def list_remove(self, source):
        """call when someone removed the user to list."""
        pass
    def user_update(self, source):
        """call when the user updated its profile."""
        pass
    def list_subscribed(self, source):
        """call when user updated its profile."""
        pass