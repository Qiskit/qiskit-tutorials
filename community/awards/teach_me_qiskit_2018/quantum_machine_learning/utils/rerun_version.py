# -*- coding: utf-8 -*-

# Copyright 2017 IBM RESEARCH. All Rights Reserved.
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
"""Script for updating the version cell of the notebooks.

Convenience script for re-running the cell that prints the information about
the versions required by the tutorials, and saving the file with the new
contents.

It should be invoked when a new version of the SDK is released, along with
updating the 'requirements.txt' file adjusting the "QISKit" dependency.

Usage:

$ python3 utils/rerun_version.py

The script will search for all the *.ipynb

"""

import glob
import os
import warnings

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


NOTEBOOK_FILENAMES = [a for a in sorted(glob.glob('**/*.ipynb',
                                                  recursive=True))]
# NOTEBOOK_FILENAMES = '1_introduction/compiling_and_running.ipynb'


class ExecuteOnlyVersionPreProcessor(ExecutePreprocessor):
    """ExecutePreprocessor that only runs "version" cells."""
    def preprocess_cell(self, cell, resources, cell_index):
        if cell.source.startswith('%run "../version.ipynb"'):
            return super(ExecuteOnlyVersionPreProcessor,
                         self).preprocess_cell(cell, resources, cell_index)

        return cell, resources


def update_notebook_version_cell(filename):
    """Run a notebook's version cell, updating the file.

    Args:
        filename (str): jupyter notebook filename.
    """
    # Open the notebook.
    file_path = os.path.dirname(os.path.abspath(filename))
    with open(filename) as f:
        notebook = nbformat.read(f, as_version=4)

    # Create the preprocessors.
    version_preprocessor = ExecuteOnlyVersionPreProcessor(
        timeout=600, kernel_name='python3')
    normal_preprocessor = ExecutePreprocessor(
        timeout=600, kernel_name='python3')

    with warnings.catch_warnings():
        # Silence a file permissions warning on jupyter, which is still not
        # merged into the current release.
        # https://github.com/jupyter/jupyter_client/pull/201
        warnings.filterwarnings('ignore', 'Failed to set sticky bit',
                                module='jupyter_client.connect')
        # Execute the notebook.
        if filename == 'version.ipynb':
            normal_preprocessor.preprocess(notebook,
                                           {'metadata': {'path': file_path}})
        else:
            version_preprocessor.preprocess(notebook,
                                            {'metadata': {'path': file_path}})

    # Save the notebook.
    with open(filename, 'wt') as f:
        nbformat.write(notebook, f)


def main():
    print('Updating the output of the version cell in notebooks ...')

    # Move "version.ipynb" to the front of the list.
    NOTEBOOK_FILENAMES.insert(
        0, NOTEBOOK_FILENAMES.pop(NOTEBOOK_FILENAMES.index('version.ipynb')))
    for i, filename in enumerate(NOTEBOOK_FILENAMES):
        print('[%2d/%2d]: %s ...' % (i+1, len(NOTEBOOK_FILENAMES), filename))
        try:
            update_notebook_version_cell(filename)
        except Exception as e:
            print('An error ocurred: %s' % str(e))


if __name__ == "__main__":
    main()