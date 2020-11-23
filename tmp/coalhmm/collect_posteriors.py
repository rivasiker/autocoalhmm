# This script generates an HDF5 file for a certain run by combining the coordinates from the info table
# and the posterior probabilities as outputted from coalHMM. Moreover, it takes into account that coalHMM
# gets rid of sites if more than half of the sequences are gaps. The ouputted HDF5 file contains -1 instead
# NaN, because HDF5 files cannot save missing values in integer columns. 

import pandas as pd
import sys
import pickle

# Save the run identifier
run = int(sys.argv[1])
if len(pickle.load(open('../params.pickle', 'rb'))) == 7:
    with open('../params.pickle', 'rb') as f:
        [path, species1, species2, species3, species4, target_seqname, big_maf_file] = pickle.load(f)
ifelse len(pickle.load(open('../params.pickle', 'rb'))) == 8:
    with open('../params.pickle', 'rb') as f:
        [path, species1, species2, species3, species4, target_seqname, big_maf_file, error_sp1] = pickle.load(f)
ifelse len(pickle.load(open('../params.pickle', 'rb'))) == 9:
    with open('../params.pickle', 'rb') as f:
        [path, species1, species2, species3, species4, target_seqname, big_maf_file, error_sp1, error_sp2] = pickle.load(f)
# Create list for ordering columns in the final table
if target_seqname.split('.')[0] in [species1, species2, species3, species4]:
    sp_lst = [species1, species2, species3, species4]
    for i in [species1, species2, species3, species4]:
        sp_lst.append('chr.'+i)
    for i in range(4):
        sp_lst.append('V{}'.format(i))
else:
    sp_lst = [species1, species2, species3, species4, target_seqname.split('.')[0]]
    for i in [species1, species2, species3, species4, target_seqname.split('.')[0]]:
        sp_lst.append('chr.'+i)
    for i in range(4):
        sp_lst.append('V{}'.format(i))
# Load the info table with the coordinates and the gap information
info_table = pd.read_csv('../info_tables/run_{}.csv'.format(run))
# Load the posterior probabilities
posteriors = pd.read_csv('../outputs/run_{}/posteriors'.format(run), delim_whitespace=True)

# Create empty dictionaries for the position and the chromosome
pos = {}
chrom = {}
# Add species as keys to the dictionaries
for species in list(set(info_table['species'])):
    pos[species] = []
    chrom['chr.'+species] = []
 
# For each individual fasta file in the run
for n in range(max(info_table['file'])+1):
    # Filter the sub-table for the fasta file
    tab = info_table[info_table['file'] == n]
    tab_coalhmm = tab[tab['species'].isin([species1, species2, species3, species4])]
    # Re-set binary vector for the columns for which the posteriors have been computed
    a = ''
    # Define list of gap information from the subtable
    lst = list(tab_coalhmm['gaps'])
    # For each index in the list of gap info
    for i in range(len(lst[0])):
        # If at least 50% of the rows are non-gaps (from the coalHMM param file)
        if int(lst[0][i])+int(lst[1][i])+int(lst[2][i])+int(lst[3][i]) >= 2:
            # Add a 1 to the binary vector
            a += '1'
        else:
            # Add a 0 to the binary vector
            a += '0'
    lst = list(tab['gaps'])
    # For each of the species
    for count, species in enumerate(list(tab['species'])):
        # Save the start coordinate
        start = int(tab[tab['species'] == species]['start'])
        # Save the chromosome name
        chromosome = tab[tab['species'] == species]['chr'].to_string(index = False).strip()
        # For each element in the binary vector
        for i in range(len(a)):
            # If at least 50% of the rows are non-gaps
            if a[i] == '1':
                # If the site is not a gap
                if lst[count][i] == '1':
                    # Add the coordinate
                    pos[species].append(start)
                    # Add the chromosome
                    chrom['chr.'+species].append(chromosome)
                    # Update coordinates
                    start += 1
                # If the site is a gap
                else:
                    # Add None to both dictionaries
                    pos[species].append(None)
                    chrom['chr.'+species].append(None)
            # If less of 50% of the rows are non-gaps
            elif a[i] == '0':
                # If the site is not a gap
                if lst[count][i] == '1':
                    # Update the coordinate 
                    start += 1


pd.concat([pd.DataFrame.from_dict(pos, dtype='int64').reindex(sorted(list(pos.keys())), axis=1).fillna(-1),
          pd.DataFrame.from_dict(chrom).reindex(sorted(list(chrom.keys())), axis=1),
          posteriors.reset_index(drop=True).drop(['Chunk'], axis=1)], 
          axis = 1)[sp_lst].to_hdf('../results/run_{}.HDF'.format(run), 
                           key='run_{}'.format(run), 
                           mode='w',
                           complevel=9,
                           format='table',
                           data_columns=list(set(info_table['species'])))
