
import os

class Error(Exception):
    def __init__(self, msg):
        self.msg = msg


def run_in_shell(cmd):
    print "Running in shell:", cmd
    if os.system(cmd) != 0:
        raise Error("os.system(cmd) end up with non zero code")
    print ""