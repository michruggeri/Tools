# Tools et al.
General utility scripts (data processing, input generation, etc.), plus some code done for fun/testing/learning purposes.

## stats.cpp
Script for data analysis of generic QMC data, with reblocking. Takes input of the form \<data\> \<weight\> (usually extracted from output files using awk; in case data is unweighted the weight should still be given, but as a constant). This script will print to screen average, (reblocked) error and correlation length. Also there will be a block.dat file, a corr.dat file and a histo.dat file, with reblocking, correlation and histogram of the data.

## gen\_det.py
Generates binary strings used to define determinants to be used in QMCPack wave function files when using multi determinant wave functions.

## det\_hist.py
Generates a histogram of the CI coefficients taken from a QMCPack wave function or optimization file. Can print the histogram on screen, or generate a pdf, eps, png or svg figure. Works for either real or complex coefficients.

## shift\_density.py
Takes an electronic density file in xsf format (for vesta, xcrysden) and shifts the electron density and the atomic positions by an arbitrary vector (in three dimensions, with periodic boundary conditions).

## qmcpack\_input\_generator.py
A GUI (made with tkinter) to generate basic input files with QMCPack. Please check [QMCPack's documentation](https://qmcpack.readthedocs.io/en/develop/index.html) to add other options!

## babanuki.py
A simple baba-nuki/old maid game (see [Wikipedia](https://en.wikipedia.org/wiki/Old_maid_(card_game)) for more information).
