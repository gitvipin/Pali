#!/usr/bin/env python
'''
This module contains the example of VM deployment through ovftool command.

A typical VM deployment can take anywhere 2-20 minutes depending on the size
of VM. This becomes a real good example of demonstrating that threads in the
Thread Pool are waiting for the tasks to be pushed in the Queue and take the
task from queue as soon as they become available which means they don't wait
for all the tasks to be pushed and "exeucte" or "run" to be called for tasks
to be picked up.
'''

import subprocess
import pipes


from src import logger
from src import task
from src import worker


log = logger.getLogger(__name__)

class OvfTask(task.Task):
    TEMPLATE=''
    INFRAHOST_IP=''
    DATASTORE=''
    PASSWORD=''
    OVF_CMND='ovftool --acceptAllEulas --datastore=%s --noSSLVerify --name=%s %s vi://root:%s@%s'

    def __init__(self, name):
        super(OvfTask, self).__init__()
        self.name = name

    def run_command(self, cmd):
        """
        Helper routing for running commands on command line.
        """
        log.debug("Running command: %s", " ".join(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            msg = "command %r failed, stdout: %r, stderr: %r"
            raise RuntimeError(msg % (" ".join(cmd), stdout, stderr))
        return stdout.rstrip().decode()

    def get_command(self):
        """
        Builds and returns the ovftool command.
        """
        return self.OVF_CMND % (self.DATASTORE,
                                self.name, self.TEMPLATE,
                                self.PASSWORD, self.INFRAHOST_IP)

    def _run(self):
        try:
            cmnd = self.get_command()
            log.info("Deploying VM %s through command : %s", self.name, cmnd)
            out = self.run_command(cmnd.split())
            log.info("Deployment finished for VM %s", self.name)
        except Exception as err:
            log.info("Deployment failed for VM %s", self.name)


def demo():

    tasks = [OvfTask(name='vip_esx_vm_%s' % x) for x in range(4)]

    # Add tasks one by one to highlight that worker threads are waiting for
    # jobs to be pushed onto the queue and will pickup the job as soon as
    # it becomes available on the queue.
    with worker.ThreadPool(2) as tpool:
        for t in tasks:
            tpool.append_task(t)

if __name__ == '__main__':
    demo()
