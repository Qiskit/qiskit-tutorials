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
"""Utils for displaying the versions required by the QISKit tutorials."""

from html import escape
from os import path

from pkg_resources import Requirement
from IPython.core.display import display, HTML


def version_information(sdk_develop=False):
    """Return an HTML table with the contents of requirements.txt"""
    def escaped_operator(operator):
        """Return the HTML-escaped operator."""
        if operator == '==':
            return ''
        else:
            return escape(operator)

    def requirement_as_row(requirement: Requirement):
        """Return a Requirement as an HTML table row."""
        tds = [requirement.name, '']
        tds[1] = ', '.join(['{} {}'.format(escaped_operator(operator), target)
                            for operator, target in sorted(requirement.specs,
                                                           reverse=True)])

        # If the version of QISKIT is not specified, show development branch.
        if sdk_develop and requirement.name == 'QISKit':
            tds[1] = '(git master branch)'

        return '<tr>{}</tr>'.format(''.join(['<td>{}</td>'.format(td) for
                                             td in tds]))

    filename = 'requirements.txt'
    # If the notebook is run from another one, the path will be the parent's.
    if not path.exists(filename):
        filename = '../requirements.txt'

    with open(filename, 'r') as requirements_file:
        str_requirements = requirements_file.readlines()
        requirements = [Requirement(i) for i in str_requirements]

    qiskit_branch = '<b>stable</b>'
    if sdk_develop:
        qiskit_branch = '<b>development</b>'
    output = ['<h2>Version information</h2>',
              '<p>Please note that this tutorial is targeted to the %s '
              'version of the QISKit SDK. The following versions of the '
              'packages are recommended:</p>' % qiskit_branch,
              '<table>',
              '<tr><th>Package</th><th colspan="2">Version</th></tr>']
    output.extend([requirement_as_row(req) for req in requirements])
    output.extend(['</table>'])

    return display(HTML('\n'.join(output)))
