import os


class Error(Exception):
    def __init__(self, msg):
        self.msg = msg


def run_in_shell(cmd):
    print "Running in shell:", cmd
    if os.system(cmd) != 0:
        raise Error("os.system(cmd) end up with non zero code")
    print ""


class Command(object):
    def __init__(self, command):
        self.command = command

    def run(self, shell=True):
        import subprocess as sp
        process = sp.Popen(self.command, shell=shell, stdout=sp.PIPE, stderr=sp.PIPE)
        self.pid = process.pid
        self.output, self.error = process.communicate()
        self.failed = process.returncode
        return self

    @property
    def returncode(self):
        return self.failed


def parse_d(filename):
    if os.path.exists(filename):
        cmd = "cat {0} | grep \"after filtering in control\"".format(filename)
        result = Command(cmd).run()
        result = str.strip(str.split(result.output, ": ")[1])
        return result
    else:
        raise Error("file does not exist")
