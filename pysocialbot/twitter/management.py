"""
PySocialBot management tool
"""
import sys
import pysocialbot.twitter
import pysocialbot.twitter.register
from pysocialbot.manager import USAGE

def getapi(param):
    return pysocialbot.twitter.Api(param["screen_name"])

def post(argc, param):
    if argc == 2:
        getapi(param).post(sys.argv[2])
    elif argc == 3:
        getapi(param).reply(sys.argv[3], sys.argv[2])
    else:
        print(USAGE + "post [message] [in_reply_to_status_id]")

def retweet(argc, param):
    if argc == 2:
        getapi(param).retweet(sys.argv[2])
    else:
        print(USAGE + "retweet [id]")

def status(argc, param):
    if argc == 2:
        print(unicode(getapi(param).status(sys.argv[2])))
    else:
        print(USAGE + "status [id]")

def delete(argc, param):
    if argc == 2:
        getapi(param).api.destroy_status(sys.argv[2])
    else:
        print(USAGE + "delete [id]")
        
def mentions(argc, param):
    if argc == 1:
        m = getapi(param).mentions()
    elif argc == 2:
        m = getapi(param).mentions(page=sys.argv[2])
    for s in m:
        print(unicode(s))
        
def timeline(argc, param):
    if argc == 1:
        timeline = getapi(param).timeline()
    elif argc == 2:
        timeline = getapi(param).timeline(page=sys.argv[2])
    for s in timeline:
        print(unicode(s))
        
def register(argc, param):
    pysocialbot.twitter.register.register()

def registered(argc, param):
    print ' '.join(pysocialbot.twitter.register.user_database())

TWITTER_COMMAND = {"post": post,
                   "retweet": retweet,
                   "status": status,
                   "delete": delete,
                   "mentions": mentions,
                   "timeline": timeline,
                   "register": register,
                   "registered": registered,}
