"""minimal pysocialbot example."""
import datetime
from pysocialbot import action, trigger, launcher, twitter
 
def posttime(env):
    return env.api.post(datetime.datetime.today().strftime("It's %I %p!"))
 
if __name__ == "__main__":
    BOT = launcher.Daemon()
    BOT.trigger = {trigger.Hourly(): action.Call(posttime)}
    BOT.resetstate()
    BOT.env.api = twitter.Api()
    BOT.run()