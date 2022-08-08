#!/usr/bin/env python
'''
A simple test to check pause on worker threads.

To run the test (from repo root directory) :
    python -m unittest discover -p test_bbuffer.py ./tests
'''
import time
import unittest

import pali.logger as logger
from examples.bbuffer import TimeStampRecorder, Producer

log = logger.getLogger(__name__)


class TestWorkerPoolPause(unittest.TestCase):

    def test_thread_task_loop(self):
        pc = Producer()
        
        # Test : Start thread and wait for 3 seconds. 
        # Records should be peoduced in the buffer.
        pc.start()
        time.sleep(3)
        pcount = pc.produce_count()
        assert pcount, "Threaded Task didn't start"

        # Test : Stop thread and wait for 2 seconds.
        # Take produce count and wait for another 4 seconds, 
        # No more records should have been produced in the buffer
        pc.stop()
        time.sleep(2)
        pcount = pc.produce_count()
        time.sleep(4)
        assert pc.produce_count() == pcount, "Threaded Task didn't stop"


    def test_bounded_buffer(self):
        tc = TimeStampRecorder()

        # Test  Producers can be started / stopped.
        # Test : Start thread and wait for 3 seconds. 
        # Records should be peoduced in the buffer.
        tc.start(consumers=False)   # start prodcuers only.
        time.sleep(3)
        pcount = tc.get_buffer_size()
        assert pcount, "Timestamp Producer didn't start"

        # Test : Stop thread and wait for 2 seconds.
        # Take produce count and wait for another 4 seconds, 
        # No more records should have been produced in the buffer
        tc.stop(consumers=False)    # start producer only
        time.sleep(2)
        pcount = tc.get_buffer_size()
        time.sleep(4)
        assert tc.get_buffer_size() == pcount, "Timestamp Producer didn't stop"



        # Test : Consumers can be started / stopped.
        tc.start(producers=False)   # start consumers only.
        time.sleep(10)
        pcount = tc.get_buffer_size()
        assert not pcount, "Timestamp Consumer didn't start"

        # Test : Stop thread and wait for 2 seconds.
        # Take produce count and wait for another 4 seconds, 
        # No more records should have been produced in the buffer
        tc.stop(producers=False)    # start consumers only.
        tc.start(consumers=False)   # start producer again.
        time.sleep(4)
        tc.stop(consumers=False)   # stop producer again.
        pcount = tc.get_buffer_size()
        time.sleep(3)
        assert pcount == tc.get_buffer_size(), "Timestamp Consumer didn't stop"

        
       