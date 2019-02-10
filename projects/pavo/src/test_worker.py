#!/usr/bin/env python

import Queue
import threading
import worker
import main

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
    t = worker.WorkerThread(in_queue=q, out_queue=None)
    thr.append(t)
    t.start()

for i in range(10):
    item = main.MyTask(i)
    q.put(item)

q.join()
for t in thr:
    t.stop()
    q.put(None)
print soln
