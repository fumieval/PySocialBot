#!/usr/bin/env python
"""PySocialBot Management Tool"""

"""
Default manage.py

Instruction:

First, Copy this file to path that contains your bot and rename "manage.py".
Second, type "python manage.py register" and follow the instructions to register user.
Examples:
    $ python manage.py register
    Please get the PIN Code from the following URL.
    https://api.twitter.com/oauth/authorize?oauth_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    PIN Code: (Enter the PIN code you've obtained.)
    Getting Access Token...
    Registered successfully: @screen_name.
Third, Change the file shown below.
    YOUR_SCREEN_NAME() -> screen name
    YOUR_DAEMON_SCRIPT() -> filename of bot script.
    RUNPATH -> the path to make process identifier file. (optional)
And Modify PARAM as needed.
    PIDFILE: process identifier's file name.
Last, remove this instruction.
"""
import os
from pysocialbot.twitter import management
from pysocialbot import daemontools

PATH = os.path.abspath(os.path.dirname(__file__))
RUNPATH = os.path.join(PATH, "var/run")

PARAM = {"screen_name": YOUR_SCREEN_NAME(),
         "SCRIPT": os.path.join(PATH, YOUR_DAEMON_SCRIPT()),
         "RUNPATH": RUNPATH,
         "PIDFILE": os.path.join(RUNPATH, "bot.pid")
         }
    
if __name__ == "__main__":
    management.execute_manager(PARAM, daemontools.DAEMONTOOLS_COMMAND)