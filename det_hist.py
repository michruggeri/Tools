#!/usr/bin/env python3

"""
This script takes a QMCPack wavefunction or optimization file and generates
histograms of the CI coefficients
"""

import sys
from xml.dom import minidom
from typing import Tuple, List
import matplotlib.pyplot as plt


def initialize(args: List[str]) -> Tuple[minidom.NodeList, float, str]:
    """
    Reads determinants and cutoff, asking for the input file if needed;
    asks if the coeffients are real or complex.
    """
    if len(args) == 1:
        filename = input("Insert the wavefunction file name: ")
    else:
        filename = args[1]

    flag = input("Are your coefficients [R]eal or [C]omplex? ").lower()
    while flag not in ("r", "c"):
        flag = input("Are your coefficients [R]eal or [C]omplex? ").lower()

    wf_file = minidom.parse(filename)
    determinants = wf_file.getElementsByTagName("ci")
    cutoff = float(
        wf_file.getElementsByTagName("detlist")[0].attributes["cutoff"].value
    )
    return determinants, cutoff, flag


def histo_real(determinants: minidom.NodeList, cutoff: float) -> None:
    """
    Builds the histogram (real case).
    """
    dets = []
    vals = []
    for det in determinants:
        dets.append(len(dets))
        vals.append(float(det.attributes["coeff"].value))
    ymax = max(vals) * 1.1
    ymin = min(min(vals) * 1.1, -0.1)
    plt.bar(dets, vals, color="mediumblue")
    plt.xticks(range(len(dets)))
    plt.xlabel("Determinant")
    plt.ylabel(r"CI Coefficient")
    plt.ylim([ymin, ymax])
    plt.axhline(y=0, color="k")
    plt.axhline(y=cutoff, color="red")
    plt.axhline(y=-cutoff, color="red")
    plt.axhline(y=1, color="steelblue", linestyle="--")
    plt.axhline(y=-1, color="steelblue", linestyle="--")


def histo_complex(determinants: minidom.NodeList, cutoff: float) -> None:
    """
    Builds the histogram (complex case).
    """
    dets = []
    vals_r = []
    vals_i = []
    for det in determinants:
        dets.append(len(dets))
        vals_r.append(float(det.attributes["coeff_real"].value))
        vals_i.append(float(det.attributes["coeff_imag"].value))
    ymax = max(max(vals_r) * 1.1, max(vals_i) * 1.1)
    ymin = min(min(min(vals_r) * 1.1, -0.1), min(min(vals_i) * 1.1, -0.1))
    fig, axs = plt.subplots(2, constrained_layout=True)
    fig.suptitle("CI coefficients")

    axs[0].bar(dets, vals_r, color="mediumblue")
    axs[0].set_xticks(range(len(dets)))
    axs[0].set_xlabel("Determinant")
    axs[0].set_ylabel(r"Real part")
    axs[0].set_ylim([ymin, ymax])
    axs[0].axhline(y=0, color="k")
    axs[0].axhline(y=cutoff, color="red")
    axs[0].axhline(y=-cutoff, color="red")
    axs[0].axhline(y=1, color="steelblue", linestyle="--")
    axs[0].axhline(y=-1, color="steelblue", linestyle="--")

    axs[1].bar(dets, vals_i, color="mediumblue")
    axs[1].set_xticks(range(len(dets)))
    axs[1].set_xlabel("Determinant")
    axs[1].set_ylabel(r"Imaginary part")
    axs[1].set_ylim([ymin, ymax])
    axs[1].axhline(y=0, color="k")
    axs[1].axhline(y=cutoff, color="red")
    axs[1].axhline(y=-cutoff, color="red")
    axs[1].axhline(y=1, color="steelblue", linestyle="--")
    axs[1].axhline(y=-1, color="steelblue", linestyle="--")


def print_fig(args: List[str]) -> None:
    """
    Print the histogram, either on screen or on the output file
    designated as an argument.
    """
    if len(args) > 2:
        plot_file = args[2]
        if plot_file[-3:] in ("png", "pdf", "eps", "svg"):
            print(f"Saving plot in {plot_file}")
            plt.savefig(plot_file)
        else:
            print("Invalid format (png, pdf, eps or svg)")
    else:
        plt.show()


def main() -> None:
    """
    Main functions, calls initialize, the figure builder and print_fig.
    """
    determinants, cutoff, flag = initialize(sys.argv)
    if flag == "r":
        histo_real(determinants, cutoff)
    elif flag == "c":
        histo_complex(determinants, cutoff)
    else:
        raise NameError("Irregular Real/Complex flag. This should not be happening.")
    print_fig(sys.argv)


if __name__ == "__main__":
    main()
