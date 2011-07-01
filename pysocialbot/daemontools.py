import os
import signal
import time
import daemon
from daemon.pidlockfile import PIDLockFile

def daemoncontext(pidfile, stdout=None, stderr=None):
    return daemon.DaemonContext(pidfile=PIDLockFile(pidfile),
                                stdout=open(stdout, 'w'),
                                stderr=open(stderr, 'w'))

def start(argc, param):
    """start daemon."""
    if os.access(param["PIDFILE"], os.F_OK):
        print("lisabotd(pid %s) already running" %
              open(param["PIDFILE"],"r").read().rstrip("\n"))
    else:
        os.system("echo -n Starting Lisabot Daemon")
        
        os.system("python %s --pidfile=%s" % (param["SCRIPT"], param["PIDFILE"]))
        
        while not os.access(param["PIDFILE"], os.F_OK):
            time.sleep(0.5)
            os.system("echo -n .")
        os.system("echo .")

def stop(argc, param):
    """stop daemon."""
    if os.access(param["PIDFILE"], os.F_OK):
        os.system("echo -n Stopping Lisabot Daemon")
        
        pid = int(open(param["PIDFILE"], "r").read())
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            for path in os.listdir(param["RUNPATH"]):
                os.remove(os.path.join(param["RUNPATH"], path))
        
        while os.access(param["PIDFILE"], os.F_OK):
            time.sleep(0.5)
            os.system("echo -n .")
        os.system("echo .")
    else:
        print("lisabotd is not running")

def restart(argc, param):
    """restart daemon."""
    if os.access(param["PIDFILE"], os.F_OK):
        stop(argc, param)
    start(argc, param)

DAEMONTOOLS_COMMAND = {"start": start,
                       "stop": stop,
                       "restart": restart,}