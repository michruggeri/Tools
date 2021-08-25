#!/usr/bin/env python3

from xml.dom import minidom
import matplotlib.pyplot as plt
import sys

if len(sys.argv) == 1:
    filename=input("Insert the wavefunction file name: ")
else:
    filename=sys.argv[1]

flag = ""
while flag != "r" and flag != "c":
    flag = input("Are your coefficients [R]eal or [C]omplex? ").lower()

wf_file = minidom.parse(filename)
determinants = wf_file.getElementsByTagName("ci")
dets = []
vals = []
vals_r = []
vals_i = []
for det in determinants:
    dets.append(len(dets))
    #dets.append(int(det.attributes["id"].value[2:]))
    if flag == "r":
      vals.append(float(det.attributes["coeff"].value))
    elif flag == "c":
      vals_r.append(float(det.attributes["coeff_real"].value))
      vals_i.append(float(det.attributes["coeff_imag"].value))
    else:
      print("AAAAAAAAAAA")
cutoff = float(wf_file.getElementsByTagName("detlist")[0].attributes["cutoff"].value)
if flag == "r":
    ymax = max(vals)*1.1
    ymin = min(min(vals)*1.1,-0.1)
    plt.bar(dets,vals,color='mediumblue')
    plt.xticks(range(len(dets)))
    plt.xlabel("Determinant")
    plt.ylabel(r"CI Coefficient")
    plt.ylim([ymin,ymax])
    plt.axhline(y=0,color='k')
    plt.axhline(y=cutoff,color='red')
    plt.axhline(y=-cutoff,color='red')
    plt.axhline(y=1,color='steelblue',linestyle='--')
    plt.axhline(y=-1,color='steelblue',linestyle='--')
elif flag=="c":
    ymax = max(max(vals_r)*1.1,max(vals_i)*1.1)
    ymin = min(min(min(vals_r)*1.1,-0.1),min(min(vals_i)*1.1,-0.1))

    fig,axs = plt.subplots(2,constrained_layout=True)
    fig.suptitle("CI coefficients")

    axs[0].bar(dets,vals_r,color='mediumblue')
    axs[0].set_xticks(range(len(dets)))
    axs[0].set_xlabel("Determinant")
    axs[0].set_ylabel(r"Real part")
    axs[0].set_ylim([ymin,ymax])
    axs[0].axhline(y=0,color='k')
    axs[0].axhline(y=cutoff,color='red')
    axs[0].axhline(y=-cutoff,color='red')
    axs[0].axhline(y=1,color='steelblue',linestyle='--')
    axs[0].axhline(y=-1,color='steelblue',linestyle='--')
    
    axs[1].bar(dets,vals_i,color='mediumblue')
    axs[1].set_xticks(range(len(dets)))
    axs[1].set_xlabel("Determinant")
    axs[1].set_ylabel(r"Imaginary part")
    axs[1].set_ylim([ymin,ymax])
    axs[1].axhline(y=0,color='k')
    axs[1].axhline(y=cutoff,color='red')
    axs[1].axhline(y=-cutoff,color='red')
    axs[1].axhline(y=1,color='steelblue',linestyle='--')
    axs[1].axhline(y=-1,color='steelblue',linestyle='--')
else:
    print("CCCCCCCCCC")

if  len(sys.argv) >2:
    plot_file = sys.argv[2]
    if plot_file[-3:] in ("png","pdf","eps","svg"):
        print(f"Saving plot in {plot_file}")
        plt.savefig(plot_file)
    else:
        print("Invalid format (png, pdf, eps or svg)")
else:
    plt.show()
