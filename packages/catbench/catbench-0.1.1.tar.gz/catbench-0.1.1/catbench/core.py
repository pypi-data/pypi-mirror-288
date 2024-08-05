from ase.optimize import LBFGS
import os
import pickle
import torch
import json
import time
from copy import deepcopy
from ase.constraints import FixAtoms
import numpy as np
from ase.io import read, write
import requests
import json
import io
import copy
import os
from ase.io import read
import pickle

GRAPHQL = 'http://api.catalysis-hub.org/graphql'

def convert_trajectory(filename):
    images = read(filename, index=':')
    os.remove(filename)
    write(filename, images, format='extxyz')

def energy_cal_gas(calculator, atoms_origin, F_CRIT_RELAX):
    atoms = deepcopy(atoms_origin)
    atoms.calc = calculator
    cell_size = [10, 10, 10]
    atoms.set_cell(cell_size)
    atoms.center()
    atomic_numbers = atoms.get_atomic_numbers()
    max_atomic_number = np.max(atomic_numbers)
    max_atomic_number_indices = [i for i, num in enumerate(
        atomic_numbers) if num == max_atomic_number]
    fixed_atom_index = np.random.choice(max_atomic_number_indices)
    c = FixAtoms(indices=[fixed_atom_index])
    atoms.set_constraint(c)
    tags = np.ones(len(atoms))
    atoms.set_tags(tags)
    opt = LBFGS(atoms)
    opt.run(fmax=F_CRIT_RELAX)

    return atoms, atoms.get_potential_energy()

def energy_cal(calculator, atoms_origin, F_CRIT_RELAX, N_CRIT_RELAX, damping, z_target, logfile='', filename=''):
    atoms = deepcopy(atoms_origin)
    atoms.calc = calculator
    tags = np.ones(len(atoms))
    atoms.set_tags(tags)
    if z_target != 0:
        atoms.set_constraint(fixatom(atoms, z_target))

    if logfile == 'no':
        opt = LBFGS(atoms, logfile=None, damping=damping)
        opt.run(fmax=F_CRIT_RELAX, steps=N_CRIT_RELAX)
        elapsed_time = 0
    else:
        time_init = time.time()
        logfile = open(logfile, 'w', buffering=1)
        logfile.write('######################\n')
        logfile.write('##  NNP relax starts  ##\n')
        logfile.write('######################\n')
        logfile.write('\nStep 1. Relaxing\n')
        opt = LBFGS(atoms, logfile=logfile,
                    trajectory=filename, damping=damping)
        opt.run(fmax=F_CRIT_RELAX, steps=N_CRIT_RELAX)
        convert_trajectory(filename)
        logfile.write('Done!\n')
        elapsed_time = time.time() - time_init
        logfile.write(f'\nElapsed time: {elapsed_time} s\n\n')
        logfile.write('###############################\n')
        logfile.write('##  Relax terminated normally  ##\n')
        logfile.write('###############################\n')
        logfile.close()

    return atoms.get_potential_energy(), opt.nsteps, atoms, elapsed_time

def fixatom(atoms, z_target):
    indices_to_fix = [
        atom.index for atom in atoms if atom.position[2] < z_target]
    const = FixAtoms(indices=indices_to_fix)
    return const

def calc_displacement(atoms1, atoms2):
    positions1 = atoms1.get_positions()
    positions2 = atoms2.get_positions()
    displacements = positions2 - positions1
    displacement_magnitudes = np.linalg.norm(displacements, axis=1)
    max_displacement = np.max(displacement_magnitudes)
    return max_displacement

def find_median_index(arr):
    orig_arr = deepcopy(arr)
    sorted_arr = sorted(arr)
    length = len(sorted_arr)
    median_index = (length - 1) // 2
    median_value = sorted_arr[median_index]
    for i, num in enumerate(orig_arr):
        if num == median_value:
            return i, median_value

def fix_z(atoms, rate_fix):
    if rate_fix:
        z_max = max(atoms.positions[:, 2])
        z_min = min(atoms.positions[:, 2])
        z_target = z_min + rate_fix * (z_max - z_min)

        return z_target
    
    else:
        return 0

def execute_benchmark(calculators, NNP_name, benchmark, F_CRIT_RELAX, N_CRIT_RELAX, rate, disp_thrs_slab, disp_thrs_ads, again_seed, damping):
    path_pkl = os.path.join(os.getcwd(), f"raw_data/{benchmark}.pkl")
    
    with open(path_pkl, 'rb') as file:
        cathub_data = pickle.load(file)

    save_directory = os.path.join(os.getcwd(), "result", NNP_name)
    print(f"Starting {NNP_name} Benchmarking")
    # Basic Settings==============================================================================
    os.makedirs(f'{save_directory}/traj', exist_ok=True)
    os.makedirs(f'{save_directory}/log', exist_ok=True)
    os.makedirs(f'{save_directory}/gases', exist_ok=True)

    final_result = {}

    final_outlier = {}
    final_outlier['Time'] = []
    final_outlier['normal'] = []
    final_outlier['outlier'] = []

    # Calculation Part==============================================================================

    accum_time = 0
    gas_energies = {}

    print("Starting calculations...")
    for key in cathub_data.keys():
        print(key)
        final_result[key] = {}
        final_result[key]['cathub'] = {}
        final_result[key]['cathub']['ads_eng'] = cathub_data[key]['cathub_energy']
        for structure in cathub_data[key]['raw'].keys():
            if 'gas' not in str(structure):
                final_result[key]['cathub'][f'{structure}_abs'] = cathub_data[key]['raw'][structure]['energy_cathub']
        final_result[key]['outliers'] = {'slab_conv': 0, 'ads_conv': 0, 'slab_move': 0, 'ads_move': 0, 'slab_seed': 0, 'ads_seed': 0, 'ads_eng_seed' : 0}

        trag_path = f'{save_directory}/traj/{key}'
        log_path = f'{save_directory}/log/{key}'

        os.makedirs(trag_path, exist_ok=True)
        os.makedirs(log_path, exist_ok=True)

        POSCAR_star = cathub_data[key]['raw']['star']['atoms']
        z_target = fix_z(POSCAR_star, rate)

        informs = {}
        informs['ads_eng'] = []
        informs['slab_disp'] = []
        informs['ads_disp'] = []
        informs['slab_seed'] = []
        informs['ads_seed'] = []

        time_total_slab = 0
        time_total_ads = 0

        for i in range(len(calculators)):
            ads_energy_calc = 0
            for structure in cathub_data[key]['raw'].keys():
                if 'gas' not in str(structure):
                    POSCAR_str = cathub_data[key]['raw'][structure]['atoms']
                    energy_calculated, steps_calculated, CONTCAR_calculated, time_calculated = energy_cal(calculators[i], POSCAR_str, F_CRIT_RELAX, N_CRIT_RELAX, damping, z_target, f'{log_path}/{structure}_{i}.txt', f'{trag_path}/{structure}_{i}')
                    ads_energy_calc += energy_calculated * cathub_data[key]['raw'][structure]['stoi']
                    accum_time += time_calculated
                    if structure == 'star':
                        slab_steps = steps_calculated
                        slab_displacement = calc_displacement(POSCAR_str, CONTCAR_calculated)
                        slab_energy = energy_calculated
                        slab_time = time_calculated
                        time_total_slab += time_calculated
                    else:
                        ads_step = steps_calculated
                        ads_displacement = calc_displacement(POSCAR_str, CONTCAR_calculated)
                        ads_energy = energy_calculated
                        ads_time = time_calculated
                        time_total_ads += time_calculated
                else:
                    gas_tag = f'{structure}_{i}th'
                    if gas_tag in gas_energies.keys():
                        ads_energy_calc += gas_energies[gas_tag] * cathub_data[key]['raw'][structure]['stoi']
                    else:
                        print(f'{gas_tag} calculating')
                        gas_POSCAR, gas_energy = energy_cal_gas(
                            calculators[i], cathub_data[key]['raw'][structure]['atoms'], F_CRIT_RELAX)
                        gas_energies[gas_tag] = gas_energy
                        ads_energy_calc += gas_energy * cathub_data[key]['raw'][structure]['stoi']
                        write(f'{save_directory}/gases/POSCAR_{gas_tag}', gas_POSCAR)

            if slab_steps == N_CRIT_RELAX:
                final_result[key]['outliers']['slab_conv'] += 1

            if ads_step == N_CRIT_RELAX:
                final_result[key]['outliers']['ads_conv'] += 1

            if slab_displacement > disp_thrs_slab:
                final_result[key]['outliers']['slab_move'] += 1

            if ads_displacement > disp_thrs_ads:
                final_result[key]['outliers']['ads_move'] += 1

            final_result[key][f'{i}'] = {
                    'ads_eng': ads_energy_calc,
                    'slab_abs': slab_energy,
                    'ads_abs': ads_energy,
                    'slab_disp': slab_displacement,
                    'ads_disp': ads_displacement,
                    'time_slab': slab_time,
                    'time_O': ads_time
                }
            
            informs['ads_eng'].append(ads_energy_calc)
            informs['slab_disp'].append(slab_displacement)
            informs['ads_disp'].append(ads_displacement)
            informs['slab_seed'].append(slab_energy)
            informs['ads_seed'].append(ads_energy)

        ads_med_index, ads_med_eng = find_median_index(informs['ads_eng'])
        slab_seed_range = np.max(np.array(informs['slab_seed'])) - np.min(np.array(informs['slab_seed']))
        ads_seed_range = np.max(np.array(informs['ads_seed'])) - np.min(np.array(informs['ads_seed']))
        ads_eng_seed_range = np.max(np.array(informs['ads_eng'])) - np.min(np.array(informs['ads_eng']))
        if slab_seed_range > again_seed:
            final_result[key]['outliers']['slab_seed'] = 1
        if ads_seed_range > again_seed:
            final_result[key]['outliers']['ads_seed'] = 1
        if ads_eng_seed_range > again_seed:
            final_result[key]['outliers']['ads_eng_seed'] = 1
        
        final_result[key]['final'] = {
            'ads_eng_median': ads_med_eng,
            'median_num': ads_med_index,
            'slab_max_disp': np.max(np.array(informs['slab_disp'])),
            'ads_max_disp': np.max(np.array(informs['ads_disp'])),
            'slab_seed_range': slab_seed_range,
            'ads_seed_range': ads_seed_range,
            'time_total_slab': time_total_slab,
            'time_total_O': time_total_ads,
        }

        outlier_sum = sum(final_result[key]['outliers'].values())
        final_outlier['Time'] = accum_time

        if outlier_sum == 0:
            final_outlier['normal'].append(key)
        else:
            final_outlier['outlier'].append(key)

        with open(f'{save_directory}/{NNP_name}_result.json', 'w') as file:
            json.dump(final_result, file, indent=4)

        with open(f'{save_directory}/{NNP_name}_outlier.json', 'w') as file:
            json.dump(final_outlier, file, indent=4)

        with open(f'{save_directory}/{NNP_name}_gases.json', 'w') as file:
            json.dump(gas_energies, file, indent=4)

    print("f{NNP_name} Benchmarking Finish")

def fetch(query):
    return requests.get(
        GRAPHQL, {'query': query}
    ).json()['data']

def reactions_from_dataset(pub_id, page_size=40):
    reactions = []
    has_next_page = True
    start_cursor = ''
    page = 0
    while has_next_page:
        data = fetch("""{{
      reactions(pubId: "{pub_id}", first: {page_size}, after: "{start_cursor}") {{
        totalCount
        pageInfo {{
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor 
        }}  
        edges {{
          node {{
            Equation
            reactants
            products
            reactionEnergy
            reactionSystems {{
              name
              systems {{
                energy
                InputFile(format: "json")
              }}
            }}  
          }}  
        }}  
      }}    
    }}""".format(start_cursor=start_cursor,
                 page_size=page_size,
                 pub_id=pub_id,
                 ))
        has_next_page = data['reactions']['pageInfo']['hasNextPage']
        start_cursor = data['reactions']['pageInfo']['endCursor']
        page += 1
        print(has_next_page, start_cursor, page_size *
              page, data['reactions']['totalCount'])
        reactions.extend(map(lambda x: x['node'], data['reactions']['edges']))

    return reactions

def aseify_reactions(reactions):
    for i, reaction in enumerate(reactions):
        for j, _ in enumerate(reactions[i]['reactionSystems']):
            system_info = reactions[i]['reactionSystems'][j].pop('systems')

            with io.StringIO() as tmp_file:
                tmp_file.write(system_info.pop('InputFile'))
                tmp_file.seek(0)
                atoms = read(tmp_file, format='json')
                atoms.pbc = True
                reactions[i]['reactionSystems'][j]['atoms'] = atoms

            reactions[i]['reactionSystems'][j]['energy'] = system_info['energy']

        reactions[i]['reactionSystems'] = {
            x['name']: {'atoms': x['atoms'], 'energy': x['energy']}
            for x in reactions[i]['reactionSystems']
        }

def json2pkl(benchmark):
    save_directory = os.path.join(os.getcwd(), 'raw_data')
    os.makedirs(save_directory, exist_ok=True)
    path_json = os.path.join(save_directory, f'{benchmark}.json')
    path_output = os.path.join(os.getcwd(), f"raw_data/{benchmark}.pkl")
    if not os.path.exists(path_output):
        if not os.path.exists(path_json):
            raw_reactions = reactions_from_dataset(benchmark)
            raw_reactions_json = {"raw_reactions": raw_reactions}
            with open(path_json, 'w') as file:
                json.dump(raw_reactions_json, file, indent=4)

        with open(path_json, 'r') as f:
            data = json.load(f)
        loaded_data = data['raw_reactions']
        dat = copy.deepcopy(loaded_data)
        aseify_reactions(dat)

        data_total = {}
        tags = []

        for i, _ in enumerate(dat):
            input = {}
            reactants_json = dat[i]['reactants']
            reactants_dict = json.loads(reactants_json)

            products_json = dat[i]['products']
            products_dict = json.loads(products_json)

            sym = dat[i]['reactionSystems']['star']['atoms'].get_chemical_formula()
            reaction_name = dat[i]['Equation']

            tag = sym + "_" + reaction_name
            if tag in tags:
                count = tags.count(tag)
                tags.append(tag)
                tag = f'{tag}_{count}'
            else:
                tags.append(tag)
            
            if len(products_dict.keys()) != 1:
                print("error")

            if 'star' not in reactants_dict.keys():
                raise ValueError("star not exist in reactants")

            for key in dat[i]['reactionSystems']:
                if key in reactants_dict.keys():
                    input[key] = {
                        'stoi': -reactants_dict[key],
                        'atoms': dat[i]['reactionSystems'][key]['atoms'],
                        'energy_cathub': dat[i]['reactionSystems'][key]['energy'],
                    }
                elif key in products_dict.keys():
                    input[key] = {''
                                'stoi': 1,
                                'atoms': dat[i]['reactionSystems'][key]['atoms'],
                                'energy_cathub': dat[i]['reactionSystems'][key]['energy'],
                                }

            data_total[tag] = {}
            data_total[tag]['raw'] = input
            data_total[tag]['cathub_energy'] = dat[i]['reactionEnergy']
            energy_check = 0
            star_num = 0
            for structure in input.keys():
                if 'star' in str(structure):
                    star_num += 1
                energy_check += input[structure]['energy_cathub'] * input[structure]['stoi']

            if star_num != 2 :
                raise ValueError("Stars are not 2")
            
            if dat[i]['reactionEnergy'] - energy_check > 0.001:
                print(tag)
                print(dat[i]['reactionEnergy'] - energy_check)
                print(dat[i]['reactionEnergy'])
                print(energy_check)
                print(data_total[tag])
                raise ValueError("Reaction energy check failed")
            
        with open(path_output, 'wb') as file:
            pickle.dump(data_total, file)