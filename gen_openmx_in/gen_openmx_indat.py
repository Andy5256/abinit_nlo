# Author: NianlongZou, ZetaoZhang, JizhangWang & YangLi
# Date: 2019.10.29
# Description: This file is using for generate OpenMX input file.
#               save *.dat in folder OpenMX_dat.
#              VDW, LDA+U and magnetism are temporarily ignored.
#              ::Input File::
#                - kpath.pkl
#                - structure.pkl
#                - template_dat.dat
#                - pao_vps_list.json 
#                - config (optional)
#              ::Output File:
#                - openmx_in.dat
#                - rest_config
#

import os
import sys
import json
import numpy as np
import pandas as pd
import pickle as pkl
import pymatgen as mg
from pymatgen.core.periodic_table import Element
from pymatgen.core.structure import Structure

# +----------------------------------+
# | Read & Set Some Basic Parameters |
# +----------------------------------+
## Read 'config' File
parameters_json = {}
parameters_json_file = 'config'
if os.path.isfile(parameters_json_file):
    with open(parameters_json_file, 'r') as frp:
        parameters_json = json.load(frp)
## PAO & VPS Data Path
relv_data_path = '../../package/calc/lib/openmx/pao_vps.atom'
data_path = os.path.abspath(relv_data_path)
#data_path = parameters_json.get('DataPath', abs_data_path)
## The Choice Set of PAO & VPS (PVS)
# This parameter should be a list of str, which contains the name of PAO & VPS 
#   sets (PVS) in 'pao_vps_list.json'. We will set the PAO and VPS of each 
#   element according to 'pao_vps_list.json'. The order of PVS in the list 
#   determines their priority, if the element doesn't contain in priorier set, 
#   it will try in the next one.  
atomic_pao_set = parameters_json.get('AtomicPao', ["ab22d"])
## SCF Criterion for each atom
# scf.criterion = scf_criter_per_atom * NumberOfAtoms.
scf_criter_per_atom = parameters_json.get('ScfCriterPerAtom', 1e-8)
scf_criter_per_atom = float(scf_criter_per_atom) #(Hartree)
## The Density of Kmesh
# scf.Kgrid = (k_1, k_2, k_3) 
# k_i = kmesh_density/|a_i|, i=1,2,3
kmesh_density = parameters_json.get('KmeshDensity', 80)
## SOC
enable_soc = parameters_json.get('EnableSOC', False)
## Profess Experience
enable_scf_pro_exp = parameters_json.get('EnableScfProExp', False)

# +-------------+
# | OpenMX Keys |
# +-------------+
openmx_paramters_set = {
## File Name and Path
    "System.CurrrentDirectory"           : './'        ,
    "System.Name"                        : 'openmx'    ,
    "level.of.stdout"                    : '1'         ,
    "level.of.fileout"                   : '1'         ,
    "DATA.PATH"                          : None        , # data_path
## Defination of Atomic Species
    "Species.Number"                     : None        , # @structure.pkl
    "Block_Definition.of.Atomic.Species" : None        , # @structure.pkl
## Structures
    "Atoms.Number"                       : None        , # @structure.pkl
    "Atoms.SpeciesAndCoordinates.Unit"   : 'FRAC'      ,
    "Block_Atoms.SpeciesAndCoordinates"  : None        , # @structure.pkl
    "Atoms.UnitVectors.Unit"             : 'Ang'       ,
    "Block_Atoms.UnitVectors"            : None        , # @structure.pkl
## SCF Related Parameters
# Basic parameters
    "scf.ProExpn.VNA"                    : None        , # enable_scf_pro_exp
    "scf.XcType"                         : 'GGA-PBE'   ,
    "scf.ElectronicTemperature"          : '300.0'     ,
    "scf.energycutoff"                   : '300'       ,
    "scf.maxIter"                        : '1000'      ,
    "scf.EigenvalueSolver"               : 'Band'      ,
    #"scf.Ngrid"                         : None        ,
    "scf.Kgrid"                          : None        , # kmesh_density
    "scf.Generation.Kpoint"              : 'MP'        ,
    "scf.criterion"                      : None        , # scf_criter_per_atom
    #"scf.lapack.dste",                  : None        ,
    "scf.partialCoreCorrection"          : 'ON'        ,
# SOC and Noncollinear (ignore the magnetic)
    "scf.SpinPolarization"               : None        , # enable_soc
    "scf.SpinOrbit.Coupling"             : None        , # enable_soc
    #"scf.Constraint.NC.Spin",           : None        ,
    #"scf.Constraint.NC.Spin.v",         : None        ,
# Band and Unfolding
    #"Unfolding.Electronic.Band",        : None        ,
    #"Unfolding.LowerBound",             : None        ,
    #"Unfolding.UpperBound",             : None        ,
    #"Unfolding.Nkpoint",                : None        ,
    #"Unfolding.desired_totalnkpt",      : None        ,
    #"Block_Unfolding.kpoint",           : None        ,
# DFT-D3 VDW (zero damping functions)
    #"scf.dftD",                         : None        ,
    #"version.dftD",                     : None        ,
    #"DFTD3.damp",                       : None        ,
    #"DFTD.Unit",                        : None        ,
    #"DFTD.rcut_dftD",                   : None        ,
    #"DFTD.cncut_dftD",                  : None        ,
    #"DFTD.IntDirection",                : None        ,
# Mixing Parameters
    "scf.Mixing.Type"                    : 'RMM-DIISK' ,
    "scf.Init.Mixing.Weight"             : '0.3'       ,
    "scf.Mixing.History"                 : '30'        ,
    "scf.Mixing.StartPulay"              : '6'         ,
    "scf.Mixing.EveryPulay"              : '1'         ,
# 1DFFT
    "1DFFT.NumGridK"                     : '900'       , 
    "1DFFT.NumGridR"                     : '900'       ,
    "1DFFT.EnergyCutoff"                 : '3600.0'    ,
# Density of State 
    #"Dos.fileout",                      : None        ,
    #"Dos.Erange",                       : None        ,
    #"Dos.Kgrid",                        : None        ,
# L(S)DA+U
    #"scf.Hubbard.U",                    : None        ,
    #"scf.Hubbard.Occupation",           : None        ,
    #"Block_Hubbard.U.values",           : None        ,
# Other Parameters 
    #"scf.Electric.Field",               : None        ,
    #"scf.system.charge",                : None        ,
# Orbital Optimization (Blank for Now)
# Geometry Optimization (Never use)
    "MD.Type"                            : 'Nomd'      ,
    #"MD.maxIter",                       : None        ,
    #"MD.Opt.criterion",                 : None        ,
## Band Calculations
    "Band.dispersion"                    : 'on'        ,
    "Band.Nkpath"                        : None        , # @kpath.pkl
    "Block_Band.kpath"                   : None        , # @kpath.pkl
## Iterface for developers
    "HS.fileout"                         : 'On'        ,
}

# +--------------------------+
# | Sub Functions Defination |
# +--------------------------+
## Read the Keys in the Key List
def get_openmx_dat(template_dat):
    in_dat = template_dat
    for key in openmx_paramters_set.keys():
        value = get_openmx_value(key)
        in_dat = in_dat.replace("__%s__" % key, value)
    return in_dat
## Set the Value for Each Key
def get_openmx_value(key):
    if (openmx_paramters_set[key] != None):
        return openmx_paramters_set[key]
    elif (key == "DATA.PATH"):
        return data_path
    elif (key == "Species.Number"):
        return str(len(structure_info_dict['formula']))
    elif (key == "Block_Definition.of.Atomic.Species"):
        epv_list = [] # Element-Pao-Vps List
        for element in structure_info_dict['formula'].keys():
            for atomic_pao in atomic_pao_set:
                if element in pvs_json[atomic_pao].keys():
                    pao_set = pvs_json[atomic_pao]
                    break
            else:
                print("Error:openmx_json doesn't have this element",element)
                return "__NotInOpenMX__"
            pao = pao_set[element][0]
            vps = pao_set[element][1]
            epv_list.append(" %-4s %-20s %s" % (element, pao, vps))
            str_epv = "\n".join(epv_list)
        return str_epv
    elif (key == "Atoms.Number"):
        structure = structure_info_dict['structure']
        return str(len(structure.species))
    elif (key == "Block_Atoms.SpeciesAndCoordinates"):
        atom_pos_list = []
        structure = structure_info_dict['structure']
        for site_index in range(len(structure.sites)):
            site_dict = structure.sites[site_index].as_dict()
            frac_pos = site_dict['abc']
            element = site_dict['species'][0]['element']
            for atomic_pao in atomic_pao_set:
                if element in pvs_json[atomic_pao].keys():
                    pao_set = pvs_json[atomic_pao]
                    break
            else:
                print("Error:openmx_json doesn't have this element",element)
                return "__NotInOpenMX__"
            electron_num = pao_set[element][2] / 2
            if enable_soc:
                pos_line = " %d %-3s %20.16f %20.16f %20.16f   \
                             %.1f %.1f 0.0 0.0 0.0 0.0 0 off" \
                           % (site_index + 1, element, frac_pos[0], frac_pos[1],
                              frac_pos[2], electron_num, electron_num)
            else:
                pos_line = " %d %-3s %20.16f %20.16f %20.16f   %.1f %.1f " \
                           % (site_index + 1, element, frac_pos[0], frac_pos[1],
                              frac_pos[2], electron_num, electron_num)
            atom_pos_list.append(pos_line)
            str_atom_pos = "\n".join(atom_pos_list)
        return str_atom_pos
    elif (key == "Block_Atoms.UnitVectors"):
        structure = structure_info_dict['structure']
        lattice = structure.lattice.matrix
        unit_vec_list = []
        for axis in lattice:
            unit_vec_list.append(" %20.16f %20.16f %20.16f" % tuple(axis))
        str_unit_vec = "\n".join(unit_vec_list)
        return str_unit_vec
    elif (key == "scf.ProExpn.VNA"):
        if enable_scf_pro_exp:
            return 'On'
        else:
            return 'Off'
    elif (key == "scf.Kgrid"):
        structure = structure_info_dict['structure']
        str_kgrid = "%4s %4s %4s" \
                    % (round(kmesh_density/(2*structure.lattice.a))*2 + 1, 
                       round(kmesh_density/(2*structure.lattice.b))*2 + 1, 
                       round(kmesh_density/(2*structure.lattice.c))*2 + 1)
        return str_kgrid
    elif (key == "scf.criterion"):
        structure = structure_info_dict['structure']
        scf_criter = scf_criter_per_atom * len(structure.species)
        return str(scf_criter)
    elif (key == "scf.SpinPolarization"):
        if enable_soc:
            return "NC"
        else:
            return "Off"
    elif (key == "scf.SpinOrbit.Coupling"):
        if enable_soc:
            return "On"
        else:
            return "Off"
    elif (key == "Band.Nkpath"):
        return str(structure_info_dict['n_k_path'])
    elif (key == "Block_Band.kpath"):
        str_kpath = "\n".join(structure_info_dict['k_path'])
        return str_kpath
    else:
        # If do not find this key
        print("Error:no corresponding method to deal with this key:")
        return "__NotInOpenMX__"

# +------------+
# | Read Files |
# +------------+
# OpenMX *.dat Template
#openmx_template_file = os.path.join(sys.path[0], 'openmx_template.dat')
#with open(openmx_template_file, "r") as frp:
#    template_dat = frp.read()
template_dat = '''
# 
# File name and path
#

System.CurrrentDirectory          __System.CurrrentDirectory__
System.Name                       __System.Name__
level.of.stdout                   __level.of.stdout__
level.of.fileout                  __level.of.fileout__
DATA.PATH                         __DATA.PATH__

#
# Defination of Atomic Species
#

Species.Number                    __Species.Number__
<Definition.of.Atomic.Species
__Block_Definition.of.Atomic.Species__
Definition.of.Atomic.Species>

#
# Structure
#

Atoms.Number                      __Atoms.Number__
Atoms.SpeciesAndCoordinates.Unit  __Atoms.SpeciesAndCoordinates.Unit__
<Atoms.SpeciesAndCoordinates
__Block_Atoms.SpeciesAndCoordinates__
Atoms.SpeciesAndCoordinates>
Atoms.UnitVectors.Unit            __Atoms.UnitVectors.Unit__
<Atoms.UnitVectors
__Block_Atoms.UnitVectors__
Atoms.UnitVectors>

#
# SCF Related Parameters
#

scf.XcType                        __scf.XcType__
scf.ElectronicTemperature         __scf.ElectronicTemperature__
scf.energycutoff                  __scf.energycutoff__
scf.maxIter                       __scf.maxIter__
scf.EigenvalueSolver              __scf.EigenvalueSolver__
#scf.Ngrid                        _____________
scf.Kgrid                         __scf.Kgrid__
scf.Generation.Kpoint             __scf.Generation.Kpoint__
scf.criterion                     __scf.criterion__ 
#scf.lapack.dste                  _____________
scf.partialCoreCorrection         __scf.partialCoreCorrection__  

## SOC and Noncollinear ##
scf.SpinPolarization              __scf.SpinPolarization__
scf.SpinOrbit.Coupling            __scf.SpinOrbit.Coupling__
#scf.Constraint.NC.Spin
#scf.Constraint.NC.Spin.v

## Band analysis and Unfolding ##
#Unfolding.Electronic.Band        __Unfolding.Electronic.Band__
#Unfolding.LowerBound             __Unfolding.LowerBound__
#Unfolding.UpperBound             __Unfolding.UpperBound__
#Unfolding.Nkpoint                __Unfolding.Nkpoint__
#Unfolding.desired_totalnkpt      __Unfolding.desired_totalnkpt__
#<Unfolding.kpoint
#__Unfolding.kpoint__
#Unfolding.kpoint>

## DFT-D3 VDW correction with zero damping functions ##
#scf.dftD                         __scf.dftD__
#version.dftD                     __version.dftD__
#DFTD3.damp                       __DFTD3.damp__
#DFTD.Unit                        __DFTD.Unit__
#DFTD.rcut_dftD                   __DFTD.rcut_dftD__
#DFTD.cncut_dftD                  __DFTD.cncut_dftD__
#DFTD.IntDirection                __DFTD.IntDirection__
## Mixing parameters related to RMM-DIISK method ##
scf.Mixing.Type                   __scf.Mixing.Type__
scf.Init.Mixing.Weight            __scf.Init.Mixing.Weight__
scf.Mixing.History                __scf.Mixing.History__
scf.Mixing.StartPulay             __scf.Mixing.StartPulay__
scf.Mixing.EveryPulay             __scf.Mixing.EveryPulay__

## 1DFFT ##
1DFFT.NumGridK                    __1DFFT.NumGridK__
1DFFT.NumGridR                    __1DFFT.NumGridR__
1DFFT.EnergyCutoff                __1DFFT.EnergyCutoff__
## Orbital Optimization ## (Blank)

## LDA+U ##
#scf.Hubbard.U                    __scf.Hubbard.U__
#scf.Hubbard.Occupation           __scf.Hubbard.Occupation__
#<Hubbard.U.values
# __Hubbard.U.values__
#Hubbard.U.values>

## Others ##
scf.ProExpn.VNA                   __scf.ProExpn.VNA__
#scf.Electric.Field               _____________
#scf.system.charge                _____________
## Density of state ##
#Dos.fileout                      _____________
#Dos.Erange                       _____________
#Dos.Kgrd                         _____________

#
# Geometry Optimization
#

MD.Type                           __MD.Type__
#MD.maxIter                       _____________
#MD.Opt.criterion                 _____________

#
# Band Calculations
#

Band.dispersion                   __Band.dispersion__
Band.Nkpath                       __Band.Nkpath__
<Band.kpath
__Block_Band.kpath__
Band.kpath>

#
# Iterface for developers
#

HS.fileout                        __HS.fileout__

## END ##
'''
# OpenMX PVS Configuration
with open("pao_vps_list.json", "r") as frp:
    pvs_json = json.load(frp)
# Structure Pkl
with open("structure.pkl", "rb") as frbp:
    structure_pkl = pkl.load(frbp)
# Kpath Pkl
with open("kpath.pkl", "rb") as frbp:
    kpath = pkl.load(frbp)

# +--------------+
# | Data Process |
# +--------------+
# Get the Material Formula
formula = {}
for site_index in range(len(structure_pkl.sites)):
    site_dict = structure_pkl.sites[site_index].as_dict()
    element = site_dict['species'][0]['element']
    formula[element] = formula.get(element, 0) + 1
# Compress the Material Data
structure_info_dict = {}
structure_info_dict['formula'] = formula
structure_info_dict['structure'] = structure_pkl
structure_info_dict['k_path'] = kpath['k_path']
structure_info_dict['n_k_path'] = kpath['n_k_path']
print('# === Strcture & Kpath ===#')
print(structure_info_dict)
print('# ========================#')

# +--------------------------+
# | Generate OpenMX *_in.dat |
# +--------------------------+
in_dat = get_openmx_dat(template_dat)
if "__NotInOpenMX__" in in_dat:
    raise "Some keys are not in OpenMX!"
with open("openmx_in.dat", "w") as fwp:
    fwp.write(in_dat)
