#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Runner """

import logging
import subprocess
import tempfile

from . import utils

class Runner(object):
    """ Runner class """

    singleton = None

    def __init__(self, schedule, test_name, command_line, max_runtime,
                 data_db, logs_db):
        self.schedule = schedule
        self.test_name = test_name
        self.command_line = command_line
        self.max_runtime = max_runtime
        self.data_db = data_db
        self.logs_db = logs_db
        self.begin = 0
        self.stdout = None
        self.stderr = None
        self.proc = None

    def run(self):
        """ Run this test """
        try:
            self.run_internal_()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            logging.warning("unhandled exception", exc_info=1)
            self.final_state_("pre_exec")

    def run_internal_(self):
        """ Internal function to run subprocess """
        if self.singleton:
            raise RuntimeError
        self.singleton = self
        self.begin = utils.timestamp()
        stdin = tempfile.TemporaryFile()
        self.stdout = tempfile.TemporaryFile()
        self.stderr = tempfile.TemporaryFile()
        self.proc = subprocess.Popen(self.command_line, close_fds=True,
            stdin=stdin, stdout=self.stdout, stderr=self.stderr)
        logging.debug("subprocess begin %d", self.proc.pid)
        self.sched_periodic_()

    def sched_periodic_(self):
        """ Schedule periodic task """
        self.schedule(5.0, 0, self.periodic_task_, ())

    def periodic_task_(self):
        """ Periodically monitor subprocess """
        try:
            self.periodic_impl_()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            logging.warning("unhandled exception", exc_info=1)
            self.final_state_("running")

    def periodic_impl_(self):
        """ Periodically monitor subprocess (impl) """
        current_time = utils.timestamp()
        exitcode = self.proc.poll()
        if exitcode is not None:
            logging.debug("subprocess exited %d", self.proc.pid)
            self.final_state_("exited")
        elif current_time - self.begin > self.max_runtime:
            logging.debug("subprocess terminated %d", self.proc.pid)
            self.proc.terminate()
            # Assume that once killed the process will terminate
            self.final_state_("killed")
        else:
            logging.debug("subprocess running %d", self.proc.pid)
            self.sched_periodic_()

    def final_state_(self, state_name):
        """ Final state """
        self.singleton = None
        logging.debug("subprocess %d: %s", self.proc.pid, state_name)
        self.proc = None
        if self.data_db:
            self.stdout.seek(0)
            self.data_db.insert(self.begin, self.test_name,
                                self.stdout.read().decode("iso-8859-1"))
            self.data_db.commit()
        self.stdout.close()
        if self.logs_db:
            self.stderr.seek(0)
            self.logs_db.insert(self.begin, self.test_name, "info",
                                self.stderr.read().decode("iso-8859-1"))
            self.logs_db.commit()
        self.stderr.close()
