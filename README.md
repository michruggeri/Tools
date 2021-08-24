# Tools
General utility scripts (data processing, input generation, etc.).

## stats.cpp
Script for data analysis of generic QMC data. Takes input of the form \<data\> \<weight\> (usually extracted fromoutput files using awk; in case data is unwighted the weight should still be given, but as a constant). Thiss script will print to terminal average, (reblocked) error and correlation length. Also there will be a block.dat file, a corr.dat file and a histo.dat file, with reblocking, correlation and histogram of the data.

## gen\_det.py
Generates binary strings used to define determinants to be used in QMCPack wave function files when using multi determinant wave functions.
