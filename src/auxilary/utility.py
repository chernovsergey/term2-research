import logging
import os


class Error(Exception):
    def __init__(self, msg):
        self.msg = msg


class Command(object):
    def __init__(self, command):
        self.command = command

    def run(self, shell=True):
        INFO("sh: {0}".format(self.command))
        import subprocess as sp
        process = sp.Popen(self.command, shell=shell, stdout=sp.PIPE, stderr=sp.PIPE)
        self.pid = process.pid
        self.output, self.error = process.communicate()
        self.failed = process.returncode
        INFO(self.output)
        INFO(self.error)
        return self

    @property
    def returncode(self):
        return self.failed


def sh(cmd):
    if Command(cmd).run().returncode != 0:
        raise Error("Command(cmd) end up with non zero code")


def parse_d(filename):
    if os.path.exists(filename):
        cmd = "cat {0} | grep \"after filtering in control\"".format(filename)
        result = Command(cmd).run()
        result = str.strip(str.split(result.output, ": ")[1])
        return result
    else:

        raise Error("file {0} does not exist".format(filename))


def INFO(message):
    logging.info(message)


def DEBUG(message):
    logging.debug(message)


def ERR(message):
    logging.error(message)


get_basename = lambda x: os.path.basename(x)

get_dirname = lambda x: os.path.dirname(x)
