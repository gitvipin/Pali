#!/usr/bin/env python

import Queue
import threading
import src.worker as worker
import src.task as task

class MyTask(task.Task):

    def __init__(self, index):
        self._id = index

    def _run(self):
        pass

soln = {}

def _worker():
    while True:
         item = q.get()
         # do_work(item)
         tid = threading.current_thread().ident
         x = soln.get(tid, [])
         x.append(item)
         soln[tid] = x
         q.task_done()

q = Queue.Queue()
num_worker_threads = 3
thr = []
for i in range(num_worker_threads):
    # t = threading.Thread(target=worker)
    # t.daemon = True
    t = worker.WorkerThread(in_queue=q, out_queue=None, verbose=False)
    thr.append(t)
    t.start()

for i in range(10):
    item = MyTask(i)
    q.put(item)

q.join()
for t in thr:
    t.stop()
    q.put(None)
print soln
