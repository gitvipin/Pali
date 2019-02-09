#!/usr/bin/env python


import task as task

class Stage(task.Task):
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




