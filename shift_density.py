#!/usr/bin/env python3
"""
Script to shift an electronic density in xsf format by a 3d vector.
"""
from typing import Tuple, List, IO, Any
import numpy
import numpy.typing as npt


class Atoms:
    """
    Defines a list of atoms; its members are
    nat: int, the number of atoms
    at_types: list[int], the atomic types (each type corresponds to an atomic number)
    at_coord: list[np.array], the 3d atomic coordinates
    """

    def __init__(
        self,
        nat: int = 1,
        at_types: List[Any] = [1],
        at_coord: npt.NDArray = numpy.array([[0, 0, 0]]),
    ) -> None:
        self.nat = nat
        self.at_types = []
        for at_type in at_types:
            self.at_types.append(at_type)
        self.at_coord = numpy.empty_like(at_coord)
        self.at_coord[:] = at_coord

    def shift_coord(self, shift: npt.NDArray = numpy.array([0, 0, 0])) -> None:
        """
        Moves the atomic coordinates by the vector shift
        """
        for i in range(3):
            self.at_coord[i] += shift[i]

    def add_atom(
        self, at_type: Any = 1, at_coord: npt.NDArray = numpy.array([[0, 0, 0]])
    ) -> None:
        """
        Adds an atom to the Atom list
        """
        self.at_types.append(at_type)
        self.at_coord = numpy.append(self.at_coord, at_coord, axis=0)
        self.nat += 1


def read_input() -> Tuple[npt.NDArray, str, str]:
    """
    Reads the file name of the original density and the shift.
    Also builds the name of the output file.
    """
    filename = input("Insert the input file name: ").strip()
    shifts = input("Insert DX, DY and DZ:  ").split()
    delta = numpy.zeros(3)
    for i in range(3):
        delta[i] = shifts[i]
    fileout = filename[:-4] + "_shifted.xsf"
    return delta, filename, fileout


def read_data(
    filein: str = "",
) -> Tuple[npt.NDArray, Atoms, npt.NDArray, npt.NDArray, List[str]]:
    """
    Reads from the filein file information on the physical system and the density.
    """
    with open(filein, "r", encoding="utf-8") as file_in:
        content = file_in.read().split()
    cursor = content.index("PRIMVEC") + 1
    cell = numpy.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            cell[i][j] = float(content[cursor])
            cursor += 1
    print(cell)
    print(numpy.linalg.inv(cell))
    cursor = content.index("PRIMCOORD") + 1
    nat = int(content[cursor])
    cursor += 2  # skip the dummy 1
    at_types = []
    at_coord = numpy.zeros((nat, 3))
    for i in range(nat):
        at_types.append(content[cursor])
        cursor += 1
        for j in range(3):
            at_coord[i][j] = content[cursor]
            cursor += 1
    atoms = Atoms(nat, at_types, at_coord)
    cursor = content.index("BEGIN_DATAGRID_3D_density") + 1
    nind = numpy.zeros(3).astype(int)
    for i in range(3):
        nind[i] = int(content[cursor])
        cursor += 1
    start_coord = numpy.zeros(3)
    for i in range(3):
        start_coord[i] = content[cursor]
        cursor += 1
    for i in range(3):
        for j in range(3):
            cell[i][j] = float(content[cursor])
            cursor += 1
    ending = content.index("END_DATAGRID_3D_density")
    values = numpy.array(content[cursor:ending])
    values = numpy.reshape(values,tuple(nind))
    return cell, atoms, nind, start_coord, values


def get_shift(
    delta: npt.NDArray = numpy.array([0, 0, 0]),
    nind: npt.NDArray = numpy.array([1, 1, 1]),
    cell: npt.NDArray = numpy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
) -> List[int]:
    """
    Takes the real space shift and converts it in discrete increments for the three directions
    """
    rotated = delta @ numpy.linalg.inv(cell)
    print("rotated:\n", rotated)
    print("nind:\n", nind)
    dr = []
    for i in range(3):
        dr.append(int(rotated[i] * nind[i]))
    print("dr:\n", dr)
    return dr


def write_head(
    file_out: IO,
    cell: npt.NDArray = numpy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    atoms: Atoms = Atoms(),
    nind: npt.NDArray = numpy.array([1, 1, 1]),
    start_coord: npt.NDArray = numpy.array([0, 0, 0]),
) -> None:
    """
    Writes the initial part of the output file.
    """
    print(type(file_out))
    file_out.write(" CRYSTAL\n")
    file_out.write(" PRIMVEC\n")
    for i in range(3):
        file_out.write(
            f"    {cell[i][0]:11.8f}  {cell[i][1]:11.8f}  {cell[i][2]:11.8f}\n"
        )
    file_out.write(" PRIMCOORD\n")
    file_out.write(f"   {atoms.nat} 1\n")
    for i in range(atoms.nat):
        file_out.write(
            f"     {atoms.at_types[i]}  {atoms.at_coord[i][0]:11.8f}  "
            f"{atoms.at_coord[i][1]:11.8f}  {atoms.at_coord[i][2]:11.8f}\n"
        )
    file_out.write(" BEGIN_BLOCK_DATAGRID_3D\n")
    file_out.write("   density\n")
    file_out.write("   BEGIN_DATAGRID_3D_density\n")
    file_out.write(f"     {int(nind[0])} {int(nind[1])} {int(nind[2])}\n")
    file_out.write(
        f"    {start_coord[0]:11.8f}  {start_coord[1]:11.8f}  {start_coord[2]:11.8f}\n"
    )
    for i in range(3):
        file_out.write(
            f"    {cell[i][0]:11.8f}  {cell[i][1]:11.8f}  {cell[i][2]:11.8f}\n"
        )


def write_tail(file_out: IO) -> None:
    """
    Writes the final part of the output file
    """
    file_out.write("   END_DATAGRID_3D_density\n")
    file_out.write(" END_BLOCK_DATAGRID_3D\n")


def main() -> None:
    """
    Main function - call the others to shift the density/atomic positions
    """
    delta, filein, fileout = read_input()
    cell, atoms, nind, start_coord, values = read_data(filein)
    nindm1 = nind - 1
    for i in range(atoms.nat):
        for j in range(3):
            atoms.at_coord[i][j] += delta[j]
    dr = get_shift(delta, nind, cell)
    print(dr)
    data = numpy.zeros(tuple(nindm1))
    for i in range(nindm1[2]):
        for j in range(nindm1[1]):
            for k in range(nindm1[0]):
                ix = int((k + dr[0]) % (nindm1[0]))
                iy = int((j + dr[1]) % (nindm1[1]))
                iz = int((i + dr[2]) % (nindm1[2]))
                data[iz][iy][ix] = values[i][j][k]
    
    density = numpy.zeros(tuple(nind),dtype=float)
    density[:nindm1[2],:nindm1[1],:nindm1[0]] = data[:,:,:] # volume copy
    density[        -1,:nindm1[1],:nindm1[0]] = data[0,:,:] # face copies
    density[:nindm1[2],        -1,:nindm1[0]] = data[:,0,:]
    density[:nindm1[2],:nindm1[1],        -1] = data[:,:,0]
    density[        -1,        -1,:nindm1[0]] = data[0,0,:] # edge copies
    density[        -1,:nindm1[1],        -1] = data[0,:,0]
    density[:nindm1[2],        -1,        -1] = data[:,0,0]
    density[        -1,        -1,        -1] = data[0,0,0] # corner copy
    density.shape = tuple(nind)


    with open(fileout, "w", encoding="utf-8") as file_out:
        write_head(file_out, cell, atoms, nind, start_coord)
        count = 0
        file_out.write("       ")
        for i in range(int(nind[2])):
            for j in range(int(nind[1])):
                for k in range(int(nind[0])):
                    file_out.write(f"{density[i][j][k]:10.8f}")
                    count += 1
                    if count == 4:
                        file_out.write("\n       ")
                        count = 0
                    else:
                        file_out.write("   ")
        if count != 0:
            file_out.write("\n")
        write_tail(file_out)


if __name__ == "__main__":
    main()
