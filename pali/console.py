#!/usr/bin/env python
"""
This module defines a wrapper for running child processes using
subprocess module.
"""


import os
import shlex
import signal
import subprocess
import time

from pali import logger
from pali import common

log = logger.getLogger(__name__)


class Console(object):
    """
    A wrapper around subprocess handle that does bookkeeping for the
    returned handle. Also provides necessary utility functions for
    checking state of child process or killing it in a proper manner.
    """

    def run_command(self, cmnd, env=None, cwd=None, timeout=-1):
        """
        Runs "cmnd" in single string and returns a tuple of  return code and
        result.

        Parameters
        ----------
        cmnd : str
            Command to be executed.
        env : string
            Set of variable to be set in string.
        cwd : string
            Working directory for child process.
        timeout : int
            time (in secs) to wait for child process to finish execution.
            -1 as default sets no time limit.

        Returns
        -------
        (int, string)
            returns a tuple of command execution return code and output.
        """

        self.proc = self._create_subprocess(cmnd=cmnd, cwd=cwd, env=env)

        # Start the counter for command to finish if requested.
        if timeout > 0:
            time_limit = time.time() + timeout

            while time.time() < time_limit:
                if self.is_alive(self.proc):
                    time.sleep(1)
                else:
                    break
            self.kill_process(self.proc)

        stdout_val = self.proc.communicate()[0]
        return self.proc.returncode, stdout_val.strip().decode('utf-8')

    def _create_subprocess(self, cmnd, stdout=None, stderr=None,
                           env=None, cwd=None):
        """
        Starts a subprocess and returns a handle for it.
        """
        stdout = subprocess.PIPE if not stdout else stdout
        stderr = subprocess.STDOUT if not stderr else stderr

        cmnd = shlex.split(cmnd)
        if common.is_windows():
            return subprocess.Popen(cmnd, shell=False, cwd=cwd, env=env,
                                    stdout=stdout, stderr=stderr,
                                    close_fds=False, start_new_session=True)
        else:
            return subprocess.Popen(cmnd, shell=False, cwd=cwd, env=env,
                                    stdout=stdout, stderr=stderr,
                                    close_fds=True, preexec_fn=os.setsid,
                                    bufsize=-1)

    def ctrl_c(self, timeout=1):
        """
        Sends SIGINT(Ctrl+C) interrupt to child process.
        """
        self.proc.send_signal(signal.SIGINT)
        # Wait for some time after sending SIGINT signal :
        # https://bugs.python.org/issue25942
        self.proc.wait(timeout)

    def kill_process(self, close_fds=False):
        """
        Kills a subprocess represented by handle 'proc'.
        """
        # command is still active, kill it.
        log.warning("Killing child process %s" % self.proc.pid)
        self.proc.kill()
        if close_fds:
            self.proc.communicate()

    def is_alive(self):
        """
        Returns True if subprocess is still running else False
        """
        return self.proc.poll() is None
