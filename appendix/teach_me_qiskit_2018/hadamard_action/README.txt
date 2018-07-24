#######################################
# README for the                      #
# Teach Me QISKit Tutorial Competion  #
# Jupyter Notebooks collection        #
# -- Connor F                         #
#######################################

This is the README documentation file for 
this entry to the 'Teach Me QISKit' IBM Q
Community competition. This documentation serves to
explain each file in the submission and
briefly outline the didactic method of these
files in attempting to introduce practical
quantum information processing skills to
interested programmers without experience
in the field.

1. Table of Contents:
    - README.txt: this file
    - /images/ - directory for image files used in 
        notebooks
    - Approach1.ipynb: python jupyter notebook that 
        explains the action of a given set of
        quantum circuits by writing out the 
        computer state by hand.
    - Approach2.ipynb: python jupyter notebook that
        explains the action of the same given set
        of quantum circuits by using the NumPy library
        to make linear algebra computations that
        represent that operation of the circuits on
        the quantum register
    - Approach3.ipynb: python jupyter notebook that
        explains the action of the same given set 
        of quantum circuits by using IBM's QISKit
        library to create instances of quantum
        registers and circuits and operate on them
        through the QISKit API and either a local or 
        external backend (including the quantum chips
        at the Watson research center).
    - QConfig.py: Configuration file for storing APIToken
        needed to access IBM's external backends. Adapted
        from QConfig_copy.py file provided in IBM's qiskit 
        tutorial files under /1_introduction/
    - Appendix.ipynb: python jupyter notebook that 
        provides background on quantum computation, theory
        needed for each notebook, and
        further readings. A cursory glance at this 
        document before reading each of 
        the tutorial notebooks is recommended.
        
2. Statement of purpose:
    The following jupyter notebooks present three different
    approaches to solving the same simple yet clever quantum
    computational exercise that demonstrates the flow of
    information through a quantum logic machine. By solving
    this same problem through several different means, the notebooks 
    try to teach an understanding of evaluating circuit diagrams that
    does not depend on only one method of interpretation. Rather, 
    the reader will find that there are multiple modes of understanding 
    quantum information processing and quantum circuity, including
    those that use classical computation to assist in interfacing
    with quantum information -- in particular the QISKit library.
    Seeing the same problem worked in parallel both with and without 
    this library aims to show its benefit and develop a working knowledge 
    of the library basics in preparation for more detailed tutorials such
    as those provided by IBM on the QISKit GitHub.