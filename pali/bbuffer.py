'''
This module implements Bounded Buffer (a.k.a. Producer Consumer).
'''
from pali.common import queue
from pali.thread import ThreadTaskLoop

from pali import logger

log = logger.getLogger(__name__)

class ProducerConsumer(object):
    BUFFER_SIZE = 1000
    RECORD_PUT_TIMEOUT = 2
    RECORD_GET_TIMEOUT = 2
    NAME = ''

    class Producer(ThreadTaskLoop):
        pass

    class Consumer(ThreadTaskLoop):
        pass
    def __init__(self, buffer_size=None):
        """
        ProducerConsumer defines a general Producer Consumer pattern
        that can be used by various applications by simply defining
        "produce" and "consume" methods.

        Parameters
        -----------
        buffer_size : int
            Size of the buffer that holds elements produced by producer.
        """
        self.buffer_size = buffer_size or self.BUFFER_SIZE
        self._buffer = queue.Queue(maxsize=self.buffer_size)

        self._producer = self.Producer()
        self._producer._task = self.produce

        self._consumer = self.Consumer()
        self._consumer._task = self.consume

    @property
    def cname(self):
        return self.NAME or self.__class_.name

    def produce(self):
        """
        Produces elements and adds them in buffer.
        """
        raise NotImplementedError("%s::produce is not defined", self.cname)

    def consume(self):
        """
        Takes elements from buffer and processes them.
        """
        raise NotImplementedError("%s::produce is not defined", self.cname)

    def start(self, producers=True, consumers=True):
        """
        Starts producer and consumer tasks in separate threads.

        Parameters
        ----------
        producers: bool
            starts producer thread if set. Defaults to True
        consumers: bool
            starts consumer thread if set. Defaults to True
        """
        if producers:
            self._producer.start()

        if consumers:
            self._consumer.start()

    def stop(self, producers=True, consumers=True):
        """
        Stops producer and consumer tasks in separate threads.

        Parameters
        ----------
        producers: bool
            stops producer thread if set. Defaults to True
        consumers: bool
            stops consumer thread if set. Defaults to True
        """
        if producers:
            self._producer.stop()

        if consumers:
            self._consumer.stop()

    def add_to_buffer(self, record):
        """
        Adds record to buffer with FIFO order.

        Parameters
        ----------
        record : Any
            Adds record to internal buffer if buffer is not full already.
            If buffer is full, an error message is generate and record is
            ignored.
        """
        try:
            self._buffer.put(record, block=False,
                             timeout=self.RECORD_PUT_TIMEOUT)
        except queue.Full:
            log.error("Queue full %s", self.cname)
        except Exception as err:
            log.error("Error : %s", err)
            raise

    def pop_from_buffer(self):
        """
        Returs record from buffer in FIFO order.

        Parameters
        ----------
        record : Any
            Adds record to internal buffer if buffer is not full already.
            If buffer is full, an error message is generate and record is
            ignored.
        """
        try:
            return self._buffer.get(block=False, timeout=self.RECORD_GET_TIMEOUT)
        except queue.Empty:
            log.debug("Queue full %s", self.cname)
        except Exception as err:
            log.error("Error : %s", err)
            raise

    def get_buffer_size(self):
        """
        Returns approximate buffer size.
        """
        return self._buffer.qsize()