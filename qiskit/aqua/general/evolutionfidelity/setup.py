# -*- coding: utf-8 -*-

# (C) Copyright IBM Corp. 2018
# IBM Confidential
# =============================================================================

import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
import atexit

long_description = """An example to install a pluggable algorithm/component."""

requirements = [
    "qiskit-aqua>=0.4.0",
    "qiskit-terra>=0.7,<0.8",
    "numpy>=1.13"
]


def _post_install():
    from qiskit_aqua_cmd.preferences import Preferences
    preferences = Preferences()
    preferences.add_package('evolutionfidelity')
    preferences.save()


class CustomInstallCommand(install):
    def run(self):
        atexit.register(_post_install)
        install.run(self)


class CustomDevelopCommand(develop):
    def run(self):
        atexit.register(_post_install)
        develop.run(self)


class CustomEggInfoCommand(egg_info):
    def run(self):
        atexit.register(_post_install)
        egg_info.run(self)


setuptools.setup(
    name='evolutionfidelity',
    version="0.4.0",  # this should match __init__.__version__
    description='Example',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='IBM Q',
    author_email='qiskit@us.ibm.com',
    license='Apache-2.0',
    classifiers=(
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering"
    ),
    keywords='qiskit sdk quantum aqua',
    packages=setuptools.find_packages(exclude=['test*']),
    install_requires=requirements,
    include_package_data=True,
    python_requires=">=3.5",
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'egg_info': CustomEggInfoCommand
    }
)
