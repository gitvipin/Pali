

To run the unit tests, run the following command from the root directory.
    python -mtests.task_test1

Run through unittest.

To run individual tests
    python -munittest discover

To run all the tests in the directory.
    python -munittest discover -s ./tests/ -t .

Run all tests from root directory and get report
    python -munittest discover ./tests -v

Generating Package
    - python3 setup.py sdist bdist_wheel
    - https://packaging.python.org/tutorials/packaging-projects/

