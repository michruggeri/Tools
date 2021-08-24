#!/usr/bin/env python3


"""
This script is used to generate binary strings used to describe determinants
to be used in MD wave function specifications for QMCPack; the state with 
the respective labels can be found in the einspline*.dat files. 
Given the number of single particle states and electrons the resulting
determinants will be stored in the determinants.dat file.
"""


def convert_integer_list(integer_list:list) -> str:
    """
    This function takes a list of integers and returns it as a single 
    uninterrupted string
    """
    converted=""
    for integer in integer_list:
        converted+=str(integer)
    return converted


def build_excitation(state:list,hole:int,particle:int) -> (list,str):
    """
    This function build an excited determinant; it starts from a 
    reference state (typically the ground state) given as an input,
    removes an electron from hole and adds one in particle. Note
    that putting a hole in an empty state or a particle in an occupied one
    will have no effect. As a feature this allows to add/remove electrons.
    """
    excitation = state[:]
    excitation[hole]=0
    excitation[particle]=1
    excitation_str = convert_integer_list(excitation)
    if sum(state) != sum(excitation):
         print("Warning: the total number of electrons changed;"\
                      f" is this what you want?")
         excitation_str += "     !"
    return excitation,excitation_str


def main() -> None:
    """
    Main function for gen_det. It builds the ground state of the system and
    uses a loop to build the desired determinants. The loop is broken if the
    input of hole and particle has some problem (e.g. wrong format or type,
    but also simply pressing enter). The output is (over)written in 
    determinants.dat
    """
    number_of_states = int(input("Number of states? "))
    number_of_electrons  = int(input("Number of electrons? "))
    print(f"Generating determinants putting {number_of_electrons} electrons"\
           f" in {number_of_states} SPOs.")
    ground_state = [1 if n<number_of_electrons else 0 for n in
            range(number_of_states)]
    print(f"GS: {convert_integer_list(ground_state)}")
    with open("determinants.dat","w") as output_file:
        while True:
            try:
                particle_hole = input("Hole and particle (from the GS)?"\
                        f" (Format: <hole> <particle>, both between 0 and"\
                        f" {number_of_states-1}) ")
                hole = int(particle_hole.split()[0])
                particle = int(particle_hole.split()[1])
                if (hole>=number_of_states or particle>=number_of_states 
                        or hole<0 or particle<0):
                    print(f"All input must be between 0 and"\
                            f" {number_of_states-1}")
                    continue
                state,state_str = build_excitation(ground_state,hole,particle)
                print(state_str)
                output_file.write(f"{state_str}\n")
            except:
                break
    print(f"Output written to determinants.dat")


if __name__ == "__main__":
    main()
