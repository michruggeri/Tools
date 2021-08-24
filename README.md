# Tools et al.
General utility scripts (data processing, input generation, etc.), plus some code done for fun/testing/learning.

## stats.cpp
Script for data analysis of generic QMC data. Takes input of the form \<data\> \<weight\> (usually extracted from output files using awk; in case data is unweighted the weight should still be given, but as a constant). This script will print to screen average, (reblocked) error and correlation length. Also there will be a block.dat file, a corr.dat file and a histo.dat file, with reblocking, correlation and histogram of the data.

## gen\_det.py
Generates binary strings used to define determinants to be used in QMCPack wave function files when using multi determinant wave functions.
