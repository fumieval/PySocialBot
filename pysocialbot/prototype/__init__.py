from pysocialbot import twitter
from pysocialbot.launcher import Daemon
from pysocialbot.twitter.userstream import UserStream

def bot_twitter_userstream(env, screen_name, triggers, handler):
    """Create minimal twitter-bot using UserStream."""
    bot = Daemon(env)
    bot.trigger = triggers

    bot.env.api = twitter.Api(screen_name)
    bot.env.stream = UserStream(bot.env.api, handler(bot.env))
    
    bot.hooks.append(lambda env: env.stream.start())
    return bot