# Author: NianlongZou
# Date: 2019.11.12
# Description:
#              ::Input File::
#                - mp.json
#                - structure.pkl
#                - config (optional)
#              ::Output File:
#                - kpath.pkl
#                - refin_structure.pkl
#
import seekpath
import pymatgen as mg
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.symmetry.bandstructure import HighSymmKpath
import spglib as spg
import pickle as pkl
import json
import os
import numpy as np
from numpy.linalg import inv
import h5py

#############################################################
# Interface
#############################################################


def str_to_cell(structure):
    lattice = structure.lattice.matrix
    positions = structure.frac_coords
    numbers = structure.atomic_numbers
    cell = (lattice, positions, numbers)
    return cell


def cell_to_str(cell):
    (lattice, positions, numbers) = cell
    structure = mg.Structure(lattice, numbers, positions)
    return structure


def input(filename, file_format):
    if file_format == 'pkl':
        with open(filename, mode='rb') as f:
            return pkl.load(f)
    if file_format == 'json':
        with open(filename, mode='r') as f:
            return json.load(f)


def output(obj, filename, file_format):
    """
    output file
    if format is json, input must be obj supported by json
    """
    if file_format == 'pkl':
        with open(filename, mode='wb') as f:
            pkl.dump(obj, f)
    if file_format == 'json':
        with open(filename, 'w') as f:
            f.write(
                json.dumps(obj,
                           sort_keys=True,
                           indent=4,
                           separators=(',', ': ')))


def input_str(filepath):
    """
    wrapper of input for structure 
    don't need to care about file_format of structure
    """
    if os.path.exists(filepath + 'structure.pkl'):
        return input(filepath + 'structure.pkl', 'pkl')
    elif os.path.exists(filepath + 'structure.json'):
        return mg.Structure.from_dict(
            input(filepath + 'structure.json', 'json'))
    elif os.path.exists(filepath + 'POSCAR'):
        return mg.Structure.from_file(filepath + 'POSCAR')
    elif os.path.exists(filepath + 'force_constants_xyz.hdf5'):
        f=h5py.File("force_constants_xyz.hdf5","r")
        lattice = f['lat'].value
        atom = str.split(f['atoms'].value)
        positions = f['fracpos'].value
        f.close()
        return mg.Structure(lattice, atom, positions)   
    else:
        raise IOError(
            "No input structure, please check your filepath carefully")


def input_config(filepath, config):
    """
    wrapper of input and output for config_dat.
    at the same time, default config will be add to config
    """
    config_dat = {}
    if os.path.isfile("config"):
        config_dat = input(filepath + 'config', 'json')
    for key in config_dat.keys():
        config[key] = config_dat[key]
    return config


def kdata_To_kpath(k_path, k_points, n_kpoint_path):
    """
    change kdata into openmx style kpath. both pymatgen's HighSymmKpath and seekpath's get_kpath will give a kdata
    kpath: path in symbol formula
    kpoints: high symmetry kpoints symbol to frac coordinate
    """
    k_path_list = []
    for cnt_line in range(len(k_path)):
        for cnt_path in range(len(k_path[cnt_line]) - 1):
            k_path_list.append(
                str(n_kpoint_path)+ ' '+\
                str(k_points[k_path[cnt_line][cnt_path]][0])+ ' '+\
                str(k_points[k_path[cnt_line][cnt_path]][1])+ ' '+\
                str(k_points[k_path[cnt_line][cnt_path]][2])+ ' '+\
                str(k_points[k_path[cnt_line][cnt_path + 1]][0])+ ' '+\
                str(k_points[k_path[cnt_line][cnt_path + 1]][1])+ ' '+\
                str(k_points[k_path[cnt_line][cnt_path + 1]][2])+ ' '+\
                str(k_path[cnt_line][cnt_path])+' '+\
                str(k_path[cnt_line][cnt_path + 1])
            )
    n_k_path = len(k_path_list)
    return {'k_path': k_path_list, 'n_k_path': n_k_path}


def symmO_To_symmOoutput(symm_O):
    symm_O_out = {}
    for key in symm_O:
        symm_O_out[key] = symm_O[key].tolist()
    return symm_O_out


#############################################################
# refine
#############################################################


def get_symprec(cell, spg_num_goal):
    """
    get the minimum symprec
    """
    syms = [0.3 * 0.8**x for x in range(100)][::-1]
    for symprec in syms:
        spglib_data = spg.get_symmetry_dataset(cell, symprec=symprec)
        if spglib_data != None:
            spg_num = spglib_data['number']
            if spg_num == spg_num_goal:
                print("[info] Set symprec as", symprec)
                break
    else:
        raise "[error] Any symprec won't give the same spg_num as Json INPUT."
    return symprec


def spglib_refine(cell, symprec):
    """
    use hall_num = 0 to refine the structure. As I know, this convention is the same as BCS's convention,
    and then use find_primitive to get primitive latt, 
    this will return the transform matrix from conv_latt to primitive_latt P
    As we must take the same cartesian coordinate as BCS ,so abs(R) matrix should be identity.
    (inversion of axis is permitted as this won't change the tensor)
    """
    dataset = spg.get_symmetry_dataset(cell, symprec)
    std_cell = (dataset['std_lattice'], dataset['std_positions'],
                dataset['std_types'])
    p_cell = spg.find_primitive(std_cell, symprec)
    P, R_p = get_transform_matrix(p_cell, symprec)
    #I = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    #error = np.max(abs(abs(R_p) - I))
    #assert error < 1e-8, "mapping to primitive have change the cartesian coordinate, which is forbid, error is: " + str(
    #    error)
    return p_cell, P, R_p

def get_pointgroup_international(cell, symprec):
    dataset = spg.get_symmetry_dataset(cell, symprec)
    return dataset['pointgroup_international']

def pymatgen_refine(structure, symprec):
    """
    using pymatgen to refine the structure, the defination of primitive standard is:
    Gives a structure with a primitive cell according to certain standards the standards are defined in 
    \Setyawan, W., & Curtarolo, S. (2010). High-throughput electronic band structure calculations: Challenges 
    and tools. Computational Materials Science, 49(2), 299-312. doi:10.1016/j.commatsci.2010.05.010
    """
    finder = SpacegroupAnalyzer(structure, symprec=symprec)
    refine_structure = finder.get_primitive_standard_structure(
        international_monoclinic=False)
    return refine_structure


def get_transform_matrix_p(cell, symprec):
    """
    get transformation matrix from a given cell(cell input) to xyz output primitive cell
    """
    U, R = get_transform_matrix(cell, symprec)
    refine_cell, P, R_p = spglib_refine(cell, symprec)
    nU = np.dot(inv(P), U)
    nR = np.dot(inv(R_p), R)
    error = np.max(
        abs(np.dot(inv(nR), np.dot(refine_cell[0].T, nU)).T - cell[0]))
    assert error < 1e-8, "nU,nR can't transform cell to primitive_cell,check std_cell carefully. error is: " + str(
        error)
    return nU, nR


def get_transform_matrix(cell, symprec):
    """
    get transformation matrix from a given cell(cell input) to spglib's crystallographic conventional cell(hall num = 0)
    U,R is defined in spglib document
    """
    spglib_data = spg.get_symmetry_dataset(cell, symprec=symprec)
    std_cell = (spglib_data['std_lattice'], spglib_data['std_positions'],
                spglib_data['std_types'])
    U = spglib_data['transformation_matrix']
    R = spglib_data['std_rotation_matrix']
    error = np.max(abs(np.dot(inv(R), np.dot(std_cell[0].T, U)).T - cell[0]))
    assert error < 1e-8, "U,R can't transform cell to conv_cell, error is: " + str(
        error)
    return U, R


def get_mp_kpath(cell, symprec):
    """
    generate mp kpath(Setyawan, W., & Curtarolo, S. (2010)) in BCS convention
    """
    structure_mp = pymatgen_refine(cell_to_str(cell), symprec)
    cell_mp = str_to_cell(structure_mp)
    U, R = get_transform_matrix_p(cell_mp, symprec)
    transform_O = inv(U)
    error = abs(np.linalg.det(transform_O) - 1)
    assert error < 1e-8, "transform_O is not unitary,error is: " + str(error)
    kpath = HighSymmKpath(structure_mp)
    k_path = kpath.kpath['path']
    k_points = kpath.kpath['kpoints']
    for kp in k_points.keys():
        k_points[kp] = np.dot(k_points[kp], transform_O)
    return k_path, k_points


def get_seekpath_kpath(cell, symprec):
    """
    generate seekpath kpath(HPKOT) in BCS convention
    """
    seekpath_data = seekpath.getpaths.get_path(
        cell, with_time_reversal=config['isTR'], symprec=symprec)
    cell_seekpath = (seekpath_data['primitive_lattice'],
                     seekpath_data['primitive_positions'],
                     seekpath_data['primitive_types'])
    U, R = get_transform_matrix_p(cell_seekpath, symprec)
    transform_O = inv(U)
    error = abs(np.linalg.det(transform_O) - 1)
    assert error < 1e-8, "transform_O is not unitary,error is: " + str(error)
    k_path = seekpath_data['path']
    k_points = seekpath_data['point_coords']
    for kp in k_points.keys():
        k_points[kp] = np.dot(k_points[kp], transform_O)
    return k_path, k_points


def get_crystall_symbol(cell, symprec):
    """
    get_crystall_symbol acoording to defination of Setyawan, W., & Curtarolo
    """
    finder = SpacegroupAnalyzer(cell_to_str(cell), symprec=symprec)
    lattice_type = finder.get_lattice_type()
    spg_symbol = finder.get_space_group_symbol()
    if lattice_type == "cubic":
        return 'c' + spg_symbol[0]
    elif lattice_type == "tetragonal":
        return 't' + spg_symbol[0]
    elif lattice_type == "orthorhombic":
        if spg_symbol[0] == 'C' or spg_symbol[0] == 'A':
            return 'oS'
        else:
            return 'o' + spg_symbol[0]
    elif lattice_type == "hexagonal":
        return 'hP'
    elif lattice_type == "rhombohedral":
        return 'hR'
    elif lattice_type == "monoclinic":
        if spg_symbol[0] == 'C':
            return 'mS'
        else:
            return 'm' + spg_symbol[0]
    elif lattice_type == "triclinic":
        return 'aP'
    else:
        warn("Unknown lattice type %s" % lattice_type)


#############################################################
#default config
#############################################################

filepath = ''
pkgpath = '/home/zounl/git/xyz_structure_refine/'
#filepath = '/home/xyz/xyz.w003.4000/xyz.w003/calculations/30819/'
config = {}
config['n_kpoint_path'] = 80
config['isTR'] = True
config['ignore_spgnum'] = False
print("[do] Read config...")
config = input_config(filepath, config)
#############################################################
#main
#############################################################

print("[do] Read Files...")
structure = input_str(filepath)
cell = str_to_cell(structure)
if  config['ignore_spgnum'] == False:
    material_dat = input(filepath + 'material.json', 'json')
    spg_dat = material_dat['spacegroup']
    print("[info] SPG from material project: %s : %s" %
      (str(spg_dat['number']), spg_dat['symbol']))

print("[do] Refine the Symmetry")
if config['ignore_spgnum']:
    spg_dat = {}
    symprec = 1e-5
    spglib_data = spg.get_symmetry_dataset(cell, symprec=symprec)
    if spglib_data != None:
        spg_dat['number'] = spglib_data['number']
        spg_dat['symbol'] = spglib_data['international']
        print("[info] SPG analyzed by spglib: %s : %s" %(str(spg_dat['number']), spg_dat['symbol']))
else:
    symprec = get_symprec(cell, spg_dat['number'])

refine_cell, P, R_p = spglib_refine(cell, symprec)
symm_O = spg.get_symmetry(refine_cell)

print("[do] generate seekpath kpath")
k_path_sk, k_points_sk = get_seekpath_kpath(cell, symprec)

print("[do] generate mp kpath")
k_path_mp, k_points_mp = get_mp_kpath(cell, symprec)

print("[do] Change info into xyz output format")
kpath_sk = kdata_To_kpath(k_path_sk, k_points_sk, config['n_kpoint_path'])
kpath_mp = kdata_To_kpath(k_path_mp, k_points_mp, config['n_kpoint_path'])
symm_O_out = symmO_To_symmOoutput(symm_O)
refine_structure = cell_to_str(refine_cell)

print("[do] get direction of tensor")
tensor_dir_json = input(pkgpath + 'tensor.json', 'json')
spglib_data = spg.get_symmetry_dataset(cell, symprec=symprec)
n_pointgroup = spglib_data['pointgroup']
tensor_dir = tensor_dir_json[n_pointgroup]

print("[do] Output")
output(refine_structure, filepath + 'refine_structure.pkl', 'pkl')
output(kpath_mp, filepath + 'kpath.pkl', 'pkl')
output(kpath_sk, filepath + 'kpath_sk.json', 'json')
output(kpath_mp, filepath + 'kpath_mp.json', 'json')
output(symm_O_out, filepath + 'symm_O.json', 'json')
output(tensor_dir, filepath + 'tensor_dir.json', 'json')
