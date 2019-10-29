# -*- coding: utf-8 -*-

# Copyright 2018 IBM and its contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

# Authors: Diego M. Rodriguez <diego.moreda@ibm.com>

"""Helper for running the notebooks as unit tests.

Convenience script for running the notebooks as individual `unittest` tests
using the standard Python facilites. By default, all notebooks under
`qiskit/` are automatically discovered (can be modified via the
`NOTEBOOK_PATH` variable).

The test can be run by using the regular unittest facilities from the root
folder of the repository:

python -m unittest --verbose

python -m unittest  utils.test.test_tutorials.TutorialsTestCase.\
    test_reference_algorithms_bernstein_vazirani_ipynb

Tested under the following Jupyter versions:
ipython==6.3.1
nbconvert==5.3.1
nbformat==4.4.0
"""

import glob

import os
import re
import unittest
import warnings

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# Configurable parameters.
# List of manual exclusion (for example, ["reference/foo/problematic.ipynb"]).
EXCLUDED_NOTEBOOKS = []
# Timeout (in seconds) for a single notebook.
TIMEOUT = os.getenv('TIMEOUT', 6000)
# Jupyter kernel to execute the notebook in.
JUPYTER_KERNEL = os.getenv('JUPYTER_KERNEL', 'python3')
# Glob expression for discovering the notebooks.
NOTEBOOK_PATH = os.getenv('NOTEBOOK_PATH', 'qiskit/**/*.ipynb')


# Retrieve the notebooks recursively.
NOTEBOOK_FILENAMES = [f for f in sorted(glob.glob(NOTEBOOK_PATH,
                                                  recursive=True))
                      if not os.path.basename(f) in EXCLUDED_NOTEBOOKS]


class TutorialsTestCaseMeta(type):
    """
    Metaclass that dynamically appends a "test_TUTORIAL_NAME" method to the
    class.
    """
    def __new__(mcs, name, bases, dict_):
        def _str_to_identifier(string):
            """Convert a string to a valid Python identifier."""
            return re.sub(r'\W|^(?=\d)', '_', string)

        def create_test(filename):
            """Return a new test function."""
            def test_function(self):
                self._run_notebook(filename)
            return test_function

        for filename in NOTEBOOK_FILENAMES:
            # Add a new "test_file_name_ipynb()" function to the test case.
            test_name = "test_%s" % _str_to_identifier(filename)
            dict_[test_name] = create_test(filename)
            dict_[test_name].__doc__ = 'Test tutorial "%s"' % filename
        return type.__new__(mcs, name, bases, dict_)


class TutorialsTestCase(unittest.TestCase,
                        metaclass=TutorialsTestCaseMeta):
    """
    TestCase for running the tutorials.
    """
    @staticmethod
    def _run_notebook(filename):
        # Create the preprocessor.
        execute_preprocessor = ExecutePreprocessor(timeout=TIMEOUT,
                                                   kernel_name=JUPYTER_KERNEL)

        # Open the notebook.
        file_path = os.path.dirname(os.path.abspath(filename))
        with open(filename) as file_:
            notebook = nbformat.read(file_, as_version=4)

        with warnings.catch_warnings():
            # Silence some spurious warnings.
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            # Finally, run the notebook.
            execute_preprocessor.preprocess(notebook,
                                            {'metadata': {'path': file_path}})
