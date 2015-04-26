#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Runner """

import datetime
import logging
import os
import subprocess
import tempfile

from . import utils

class RunnerOnce(object):
    """ Runner class """

    @staticmethod
    def _make_pendingdir(basedir):
        """ Make name of directory in which test data is kept """
        pendingdir = os.path.join(basedir, "pending", datetime.datetime.now()
                                                                .isoformat())
        rwx______ = int("700", 8)  # py2/py3 portable
        os.mkdir(pendingdir, rwx______)
        return pendingdir

    def _quickly_write_file(self, name, content):
        """ Quickly write file in pendingdir """
        with open(os.path.join(self.pendingdir, name), "w+") as filep:
            filep.write("%s\n" % content)

    def __init__(self, complete, schedule, basedir, test_name,
                 command_line, **kwargs):
        self.complete = complete
        self.basedir = basedir

        self.pendingdir = self._make_pendingdir(self.basedir)
        logging.debug("runner: pendingdir: %s", self.pendingdir)
        self._quickly_write_file("spec", "1.0")
        self._quickly_write_file("test_name", test_name)
        self._quickly_write_file("status", "pre_exec")

        self.max_runtime = kwargs.get("max_runtime", 30)
        self.started = utils.timestamp()
        self.schedule = schedule
        self.stdin = open(os.path.join(self.pendingdir, "stdin"), "w+b")
        bytes_for_stdin = kwargs.get("bytes_for_stdin")
        if bytes_for_stdin:
            self.stdin.write(bytes_for_stdin)
            self.stdin.seek(0, os.SEEK_SET)
        self.stdout = open(os.path.join(self.pendingdir, "stdout"), "w+b")
        self.stderr = open(os.path.join(self.pendingdir, "stderr"), "w+b")

        self.proc = subprocess.Popen(command_line, close_fds=True,
                                     stdin=self.stdin, stdout=self.stdout,
                                     stderr=self.stderr)

        logging.debug("runner: subprocess started with pid %d", self.proc.pid)
        self._quickly_write_file("pid", self.proc.pid)
        self._quickly_write_file("started", self.started)
        self._quickly_write_file("status", "running")
        self.schedule(5.0, 0, self.periodic_task_, ())

    def periodic_task_(self):
        """ Periodically monitor subprocess """
        current_time = utils.timestamp()
        exitcode = self.proc.poll()
        if exitcode is not None:
            logging.debug("runner: subprocess %d exited", self.proc.pid)
            logging.debug("runner: exitcode is %d", exitcode)
            self._quickly_write_file("status", "exited")
            self._quickly_write_file("exitcode", exitcode)
            self.final_state_()
        elif current_time - self.started > self.max_runtime:
            logging.debug("runner: terminating subprocess %d", self.proc.pid)
            self.proc.terminate()
            # Assume that once killed the process will terminate
            self._quickly_write_file("status", "killed")
            self.final_state_()
        else:
            logging.debug("runner: subprocess %d still running", self.proc.pid)
            self.schedule(5.0, 0, self.periodic_task_, ())

    def final_state_(self):
        """ Clear opened resources """
        self.proc = None
        self.stdin.close()
        self.stdout.close()
        self.stderr.close()
        if self.complete:
            self.complete()

    def get_pendingdir(self):
        """ Return the base directory """
        return self.pendingdir

class Runner(object):
    """ Runner object """

    def __init__(self, schedule, basedir):
        self.schedule = schedule
        self.basedir = basedir
        self.child = None

    def run(self, test_name, command_line, **kwargs):
        """ Run child process """
        if self.child:
            raise RuntimeError("child already running")
        self.child = RunnerOnce(self.complete_, self.schedule, self.basedir,
                                test_name, command_line, **kwargs)

    def complete_(self):
        """ Called when the child is done """
        self.child = None
