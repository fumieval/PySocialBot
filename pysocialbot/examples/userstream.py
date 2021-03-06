"""minimal pysocialbot example using userstream."""

from pysocialbot import launcher, twitter
from pysocialbot.twitter.userstream import UserStream, StreamHandler

class MyStreamHandler(StreamHandler):
    def __init__(self, env):
        StreamHandler.__init__(self)
        self.env = env
    def status(self, status):
        if "#python" in status.text:
            self.env.api.favorite(status.id)

if __name__ == "__main__":
    BOT = launcher.Daemon()
    BOT.env.api = twitter.Api()
    BOT.env.stream = UserStream(BOT.env.api, MyStreamHandler(BOT.env))
    BOT.hooks.append(lambda env: env.stream.start())
    BOT.run()