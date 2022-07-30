#!/usr/bin/env python
'''
This module provides utilities for parallelizing work.
'''
from pali.common import PYTHON_2

if PYTHON_2:
    raise ImportError('"parallel" module is available only Python3.')

from concurrent.futures import ThreadPoolExecutor, as_completed

from pali.config import get_param
from pali.logger import getLogger

log = getLogger(__name__)

THREAD_COUNT = get_param('THREAD_POOL_CONCURRENCY', 32)


def ThreadPool(params, blocking=True, thread_count=None):
    """
    A wrapper method around python's in-built ThreadPool executor.

    Parameters
    ------------
    params : List
        List of tuples to be run in parallel in a threadpool.
    blocking : bool
        Waits for all tasks to finish when set to True else
        returns immediately after submission of tasks on Threadpool.
    thread_count: int
        Number of threads to be used in Thread Pool.

    Return
    ------------
    results : dict
        A dictionary of result of each task.
    """
    results = {}
    max_workers = thread_count or THREAD_COUNT

    with ThreadPoolExecutor(max_workers=max_workers) as tpool:
        futures = {}
        for _func, _ident, _args, _kwargs in params:
            _tfunc = tpool.submit(_func, *_args, **_kwargs)
            futures[_tfunc] = _ident

        if not blocking:
            return None

        for future in as_completed(futures):
            ident = futures[future]
            try:
                results[ident] = future.result()
            except Exception as err:
                log.warn("Error for %s - %s", ident, err)
    return results
