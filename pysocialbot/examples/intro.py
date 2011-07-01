"""minimal pysocialbot example."""
import datetime
from pysocialbot import launcher, twitter
 
def posttime(env):
    return env.api.post(datetime.datetime.today().strftime("It's %I %p!"))
 
if __name__ == "__main__":
    BOT = launcher.Daemon()
    BOT.trigger = {launcher.Hourly(): launcher.Call(posttime)}
    BOT.resetstate()
    BOT.env.api = twitter.Api()
    BOT.run()