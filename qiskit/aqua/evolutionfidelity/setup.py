# -*- coding: utf-8 -*-

# (C) Copyright IBM Corp. 2018
# IBM Confidential
# =============================================================================

import setuptools

long_description = """An example to install a pluggable algorithm/component."""

requirements = [
    "qiskit-aqua>=0.5",
    "numpy>=1.13,<1.16"
]

setuptools.setup(
    name='evolutionfidelity',
    version="0.1.0",  # this should match __init__.__version__
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
    entry_points={
        'qiskit.aqua.pluggables': [
            'EvolutionFidelity = evolutionfidelity:EvolutionFidelity'
        ],
    },
)
