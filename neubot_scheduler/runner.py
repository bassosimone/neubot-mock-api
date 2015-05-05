#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Runner """

import datetime
import logging
import subprocess
import tempfile

from . import utils

class Runner(object):
    """ Runner class """

    singleton = []

    def __init__(self, schedule, test_name, command_line, max_runtime,
                 data_db, logs_db, config_db, pending_dir, run_dir):
        self.schedule = schedule
        self.test_name = test_name
        self.command_line = command_line
        self.max_runtime = max_runtime
        self.data_db = data_db
        self.logs_db = logs_db
        self.config_db = config_db
        self.pending_dir = pending_dir
        self.run_dir = run_dir
        self.begin = 0
        self.stdout = None
        self.stderr = None
        self.proc = None

    def run(self):
        """ Run this test """
        if self.singleton:
            raise RuntimeError  # this must case a 500
        try:
            self.run_internal_()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            logging.warning("unhandled exception", exc_info=1)
            self.final_state_("pre_exec")

    def run_internal_(self):
        """ Internal function to run subprocess """
        self.singleton.append(self)
        self.begin = utils.timestamp()
        prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") \
                 + "-" + self.test_name + "-"
        delete = not self.config_db.select()["keep_temporary_files"]
        stdin = tempfile.NamedTemporaryFile(prefix=prefix + "stdin-",
                           suffix=".txt", dir=self.pending_dir, delete=delete)
        self.stdout = tempfile.NamedTemporaryFile(prefix=prefix + "stdout-",
                           suffix=".txt", dir=self.pending_dir, delete=delete)
        self.stderr = tempfile.NamedTemporaryFile(prefix=prefix + "stderr-",
                           suffix=".txt", dir=self.pending_dir, delete=delete)
        logging.debug("running %s in directory %s", self.command_line,
                      self.run_dir)
        self.proc = subprocess.Popen(self.command_line, close_fds=True,
            stdin=stdin, stdout=self.stdout, stderr=self.stderr,
            cwd=self.run_dir)
        logging.debug("%s: started", self.proc)
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
            logging.debug("%s: exited", self.proc)
            self.final_state_("exited")
        elif current_time - self.begin > self.max_runtime:
            logging.debug("%s: killed by us", self.proc)
            self.proc.terminate()
            # Assume that once killed the process will terminate
            self.final_state_("killed")
        else:
            logging.debug("%s: still running", self.proc)
            self.sched_periodic_()

    def final_state_(self, state_name):
        """ Final state """
        del self.singleton[:]
        logging.debug("%s: final state: %s", self.proc, state_name)
        self.proc = None
        if self.stdout:
            if self.data_db:
                self.stdout.seek(0)
                self.data_db.insert(self.begin, self.test_name,
                                    self.stdout.read().decode("iso-8859-1"))
                self.data_db.commit()
            self.stdout.close()
        if self.stderr:
            if self.logs_db:
                self.stderr.seek(0)
                self.logs_db.insert(self.begin, self.test_name, "info",
                                    self.stderr.read().decode("iso-8859-1"))
                self.logs_db.commit()
            self.stderr.close()
