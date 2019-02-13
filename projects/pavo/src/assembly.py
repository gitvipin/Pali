#!/usr/bin/env python
'''
This module defines the Abstract Interface and Implementation for
Pipeline Stages, Pipelines and Assembly.

A Stage is an atomic step as part of whole pipelining process. A Pipeline
is a collection of Stages. An Assembly is collection of Pipelines.

There can be several stages in a pipeline but there must be a serial order
in which they shall be executed. This is the reason Stages are kept in the
form of Linked List inside a pipeline. No two stages of same pipeline can
be executed in parallel. However, there can be multiple pipelines
that can be run in parallel.

A single thread shall be assigned to execute a pipeline stage as it
is always executed in serial order.

Pipelines are nothing but a description of collection of steps to be
executed on a given set of data.

One usecase of pipelines is to configure endpoints / VMs / nodes. Here,
set of steps to be executed is same for all the endpoints but need to be
separately and can also be executed in parallel. In such a case, a pipeline
will be defined once but Assembly will create multiple Pipelines with varying
IP addresses of endpoints to be configured.

'''

import abc
import logging
import task as task

class Stage(task.Task):

    """
    Stages are like the atomic step of pipelines execution.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._next= None
        self.log = logging.getLogger(__name__)

    @abc.abstractmethod
    def _run(self, data):
        """
        override this.  The data map can be used to pass runtime messages
        to the next stage
        """
        pass


class Pipeline(object):

    def __init__(self):
        """
        A pipeline is a collection of pipeline stages.
        """
        self.stages = []



class Assembly(object):

    def __init__(self):
        '''
        Assembly is a collection of pipelines.
        '''
        self.pipelines = []




