"""
PySocialBot manager
"""
import sys
USAGE = "Usage: python %s" % sys.argv[0]

def execute_manager(param, commands):
    """command-line manager."""
    argc = len(sys.argv) - 1
    if argc < 1:
        print(USAGE + " [action]")
    else:
        for commandset in commands:
            if sys.argv[1] in commandset:
                return commandset[sys.argv[1]](argc, param)
        print("Action %s is not defined" % sys.argv[1])