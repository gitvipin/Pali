'''
This module demonstrates examples of ProducerConsumer and
ThreadTaskLoop
'''
import time

from pali.bbuffer import ProducerConsumer
from pali.logger import getLogger, setup_logging
from pali.thread import ThreadTaskLoop

log = getLogger(__name__)

class TimeStampRecorder(ProducerConsumer):
    """
    A simple application of Bounded Buffer a.k.a ProducerConsumer.
    Producer generates timestamps every 2 seconds. 
    Consumer simply consumers timestamps generated and prints them on
    stdout.

    """
    NAME = "TimestampRecorder"

    def produce(self):
        """Generate timestamp every 2 seconds"""
        time.sleep(1)
        self.add_to_buffer(int(time.time()))

    def consume(self):
        """ Print timestamp every 1 second from buffer"""
        time.sleep(2)
        data = self.pop_from_buffer()
        log.info("Data : %s - Buffer size : %s", data,
                 self.get_buffer_size())


class Producer(ThreadTaskLoop):
    """
    A simple ThreadTaskLoop that will run '_task' method
    in a loop.
    """
    def __init__(self):
        super(Producer, self).__init__()
        self.array = []

    def produce_count(self):
        """ Returns number of elements produced so far."""
        return len(self.array)

    def _task(self):
        time.sleep(1)
        self.array.append(int(time.time()))


if __name__ == '__main__':
    setup_logging()

    # Create an instance of Producer and once started, 
    # We should see timestamps collected in it's
    # internal storage.
    pc = Producer()
    pc.start()

    # Create a timestamp recorder
    tc = TimeStampRecorder()
    tc.start()
    time.sleep(10)
    tc.stop()