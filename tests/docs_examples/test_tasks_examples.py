"""
Tests for examples from Tasks Guide.

These tests verify that all code snippets in docs/guide/tasks.md
actually work as described.
"""

import hashlib
import os
import sqlite3
import tempfile
import unittest
from unittest import mock

from pali.task import Task
from pali.worker import ThreadPool


class TestTaskGuideSimpleExample(unittest.TestCase):
    """Test the simple data processing example from the Tasks Guide."""

    def test_square_task_computes_result(self):
        class SquareTask(Task):
            def __init__(self, number):
                super(SquareTask, self).__init__()
                self.number = number
                self.result = None

            def _run(self):
                self.result = self.number ** 2

        task_obj = SquareTask(5)
        self.assertIsNone(task_obj.result)

        with ThreadPool(1) as tpool:
            tpool.append_task(task_obj)

        self.assertEqual(task_obj.result, 25)


class TestTaskGuideHttpExample(unittest.TestCase):
    """Test the HTTP request task example from the Tasks Guide."""

    def test_fetch_task_handles_successful_requests(self):
        class FakeResponse(object):
            def __init__(self, status_code, text='ok'):
                self.status_code = status_code
                self.text = text

        import sys
        import types

        fake_requests = types.SimpleNamespace(
            get=mock.Mock(return_value=FakeResponse(200, 'ok')),
            RequestException=Exception,
        )

        with mock.patch.dict(sys.modules, {'requests': fake_requests}):
            import requests

            class FetchTask(Task):
                def __init__(self, url):
                    super(FetchTask, self).__init__()
                    self.url = url
                    self.response = None
                    self.error = None

                def _run(self):
                    try:
                        self.response = requests.get(self.url, timeout=5)
                    except requests.RequestException as e:
                        self.error = e

            urls = [
                'https://api.example.com/data1',
                'https://api.example.com/data2',
                'https://api.example.com/data3',
            ]
            tasks = [FetchTask(url) for url in urls]

            with ThreadPool(3) as tpool:
                for t in tasks:
                    tpool.append_task(t)

            for t in tasks:
                self.assertIsNone(t.error)
                self.assertIsNotNone(t.response)
                self.assertEqual(t.response.status_code, 200)


class TestTaskGuideDatabaseExample(unittest.TestCase):
    """Test the database operation task example from the Tasks Guide."""

    def test_database_task_reads_rows(self):
        temp_dir = tempfile.mkdtemp(prefix='pali-db-test-')
        db_path = os.path.join(temp_dir, 'data.db')

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')
            cursor.executemany(
                'INSERT INTO users (id, name) VALUES (?, ?)',
                [(1, 'Alice'), (2, 'Bob'), (3, 'Carol')]
            )
            conn.commit()
            conn.close()

            class DatabaseTask(Task):
                def __init__(self, db_file, query, params=None):
                    super(DatabaseTask, self).__init__()
                    self.db_file = db_file
                    self.query = query
                    self.params = params or ()
                    self.result = None
                    self.error = None

                def _run(self):
                    try:
                        conn = sqlite3.connect(self.db_file)
                        cursor = conn.cursor()
                        cursor.execute(self.query, self.params)
                        self.result = cursor.fetchall()
                        conn.close()
                    except sqlite3.Error as e:
                        self.error = e

            tasks = [
                DatabaseTask(db_path, 'SELECT * FROM users WHERE id=?', (1,)),
                DatabaseTask(db_path, 'SELECT * FROM users WHERE id=?', (2,)),
                DatabaseTask(db_path, 'SELECT * FROM users WHERE id=?', (3,)),
            ]

            with ThreadPool(3) as tpool:
                for t in tasks:
                    tpool.append_task(t)

            expected = [(1, 'Alice'), (2, 'Bob'), (3, 'Carol')]
            for task_obj, expected_row in zip(tasks, expected):
                self.assertIsNone(task_obj.error)
                self.assertEqual(task_obj.result, [expected_row])
        finally:
            try:
                os.remove(db_path)
            except OSError:
                pass
            os.rmdir(temp_dir)


class TestTaskGuideFileExample(unittest.TestCase):
    """Test the file processing task example from the Tasks Guide."""

    def test_file_hash_task_computes_sha256(self):
        temp_dir = tempfile.mkdtemp(prefix='pali-file-test-')
        try:
            paths = []
            expected_hashes = {}
            for index, content in enumerate([b'hello', b'world', b'pali']):
                file_path = os.path.join(temp_dir, f'file{index}.bin')
                with open(file_path, 'wb') as handle:
                    handle.write(content)
                paths.append(file_path)
                expected_hashes[file_path] = hashlib.sha256(content).hexdigest()

            class FileHashTask(Task):
                def __init__(self, filepath):
                    super(FileHashTask, self).__init__()
                    self.filepath = filepath
                    self.hash = None
                    self.error = None

                def _run(self):
                    try:
                        sha256 = hashlib.sha256()
                        with open(self.filepath, 'rb') as f:
                            for chunk in iter(lambda: f.read(4096), b''):
                                sha256.update(chunk)
                        self.hash = sha256.hexdigest()
                    except IOError as e:
                        self.error = e

            tasks = [FileHashTask(path) for path in paths]
            with ThreadPool(4) as tpool:
                for t in tasks:
                    tpool.append_task(t)

            for t in tasks:
                self.assertIsNone(t.error)
                self.assertEqual(t.hash, expected_hashes[t.filepath])
        finally:
            for path in paths:
                try:
                    os.remove(path)
                except OSError:
                    pass
            try:
                os.rmdir(temp_dir)
            except OSError:
                pass


class TestTaskGuideErrorHandlingExample(unittest.TestCase):
    """Test error handling examples from the Tasks Guide."""

    def test_safe_task_captures_zero_division_error(self):
        class SafeTask(Task):
            def __init__(self, data):
                super(SafeTask, self).__init__()
                self.data = data
                self.result = None
                self.error = None

            def _run(self):
                try:
                    self.result = 1 / self.data
                except ZeroDivisionError as e:
                    self.error = e
                except Exception as e:
                    self.error = e

        task_obj = SafeTask(0)
        with ThreadPool(1) as tpool:
            tpool.append_task(task_obj)

        self.assertIsNone(task_obj.result)
        self.assertIsInstance(task_obj.error, ZeroDivisionError)

    def test_task_priority_comparison(self):
        class PriorityTask(Task):
            def __init__(self, name, priority):
                super(PriorityTask, self).__init__(priority=priority)
                self.name = name

            def _run(self):
                pass

        t1 = PriorityTask('Task A', priority=1)
        t2 = PriorityTask('Task B', priority=2)
        self.assertTrue(t1 < t2)


if __name__ == '__main__':
    unittest.main()
