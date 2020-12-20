# Author: NianlongZou
# Date: 2019.10.20
# Description: Generate and refine structure and kpath 
#                read from MP pkl file.
#              ::Input File::
#                - mp.json
#                - structure.pkl
#                - config (optional)
#              ::Output File:
#                - kpath.pkl
#                - refin_structure.pkl
#

import os
import pymatgen as mg
from pymatgen.core.periodic_table import Element
from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.symmetry.bandstructure import HighSymmKpath
from pymatgen.electronic_structure.plotter import plot_brillouin_zone
from pymatgen.electronic_structure.plotter import plot_brillouin_zone_from_kpath
import spglib as spg
import numpy as np
import re
import sys
import pickle as pkl
import json

# +------------+
# | Read Files |
# +------------+
print("[do] Read Files...")
## structure.pkl
with open("structure.pkl",'rb') as frbp:
    structure = pkl.load(frbp)
print("[do] Generate POSCAR of original structures...")
poscar = structure.to(fmt="poscar")
with open("POSCAR-Origin", 'w') as fwp:
    fwp.write(poscar)
## material.json (mp.json)
with open("material.json", 'r') as jfrp:
    material_info = json.load(jfrp)
spg_info = material_info['spacegroup']
spg_num = spg_info["number"]
spg_symbol = spg_info["symbol"]
print("[info] Original SPG: %s --> %s" %(str(spg_num), spg_symbol))
## config
config_dat = {}
if os.path.isfile("config"):
    with open("config", 'r') as jfrp:
        config_dat = json.load(jfrp)
n_kpoint_path = config_dat.get('n_kpoint_path', 60)
flag_primtive = config_dat.get('flag_primtive', True)
print("[info] Number of kpoints per kpath: ", n_kpoint_path)

# +-----------------+
# | Symmetry Refine |
# +-----------------+
print("[do] Refine the Symmetry...")
syms = [0.3 * 0.9 ** x for x in range(100)][::-1]
for sym in syms:
    finder = SpacegroupAnalyzer(structure, symprec=sym)
    if finder.get_space_group_number() == spg_num:
        print("[info] Set symprec as %f" % (sym))
        break
else:
    symprec=0.01
    print("[warning] Any symprec won't give the same spg_num as Json INPUT.")
    print("[warning] We will use default symprec instead.")
    print("[warning] The spg will not coincident with MaterialProject...")
if flag_primtive:
    p_structure = finder.get_primitive_standard_structure()
else:
    p_structure = finder.get_conventional_standard_structure()    
new_finder = SpacegroupAnalyzer(p_structure)
new_spg_num = new_finder.get_space_group_number()
new_spg_symbol = new_finder.get_space_group_symbol()

if new_spg_num != spg_num:
    print("[warning] The refined structure have different spg with material")
    print("[warning]   project and symprec have been determined by previous")
    print("[warning]   calculation...") 
# Write the result to poscar file
print("[do] Generate POSCAR of refined structures...")
poscar = structure.to(fmt="poscar")
with open("POSCAR-Refined", 'w') as fwp:
    fwp.write(poscar)
print("[info] SPG: %s --> %s" %(str(new_spg_num), new_spg_symbol))

# +----------------+
# | Generate Kpath |
# +----------------+
print("[do] Generate Kpath...")
hsk_symbol_list = HighSymmKpath(p_structure).kpath['path']
hsk_vector_list = HighSymmKpath(p_structure).kpath['kpoints']
openmx_kapth_list = []
for part_of_hsk_symbol_list in hsk_symbol_list:
    for hsk_index in range(len(part_of_hsk_symbol_list)-1):
        start_hsk_symbol = part_of_hsk_symbol_list[hsk_index]
        end_hsk_symbol = part_of_hsk_symbol_list[hsk_index+1]
        start_hsk_vector_x = hsk_vector_list[start_hsk_symbol][0]
        start_hsk_vector_y = hsk_vector_list[start_hsk_symbol][1]
        start_hsk_vector_z = hsk_vector_list[start_hsk_symbol][2]
        end_hsk_vector_x = hsk_vector_list[end_hsk_symbol][0]
        end_hsk_vector_y = hsk_vector_list[end_hsk_symbol][1]
        end_hsk_vector_z = hsk_vector_list[end_hsk_symbol][2]
        str_openmx_kpath_line = \
            "%3d  %15.12f %15.12f %15.12f  %15.12f %15.12f %15.12f  %6s %6s" \
            %(n_kpoint_path, 
              start_hsk_vector_x, start_hsk_vector_y, start_hsk_vector_z, 
              end_hsk_vector_x, end_hsk_vector_y, end_hsk_vector_z, 
              start_hsk_symbol, end_hsk_symbol)
        openmx_kapth_list.append(str_openmx_kpath_line)
        print(str_openmx_kpath_line)
n_kpath=len(openmx_kapth_list)

# +--------------+
# | Save to Json |
# +--------------+
with open('refine_structure.pkl','wb') as fwbp:
    pkl.dump(p_structure, fwbp)
k_path_output={'k_path': openmx_kapth_list , 'n_k_path': n_kpath}
with open('kpath.pkl','wb') as fwbp:
    pkl.dump(k_path_output, fwbp)
with open('spg_num', "w") as fwp:
    fwp.write(str(new_spg_num))
    