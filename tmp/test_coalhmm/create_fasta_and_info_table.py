# This script is used for saving the individual fasta files and the info table for a certain 
# coalHMM run. The run number is specified as the first argument of the call, and the start 
# end coordinated for the maf slicing are supplied by the second and third arguments respectively.
# All in all, this script can be run using:
#       python create_fasta_and_info_table.py run_number start_coord end_coord 
# Moreover, this script will act differently if the target_seqname species is part of the
# trio + outgroup or not. If the target_seqname does not appear as part of the analysis, the
# sequence belonging to this species will be removed before saving the fasta files for running
# coalHMM, but its coordinates will be saved in the info table together with the four other
# species. In the case that the target_seqname is part of the trio + outgroup, then no species
# will be filtered for the coalHMM run, and the coordinates of all four species will be kept in
# the info table. 

from Bio import AlignIO
from Bio.AlignIO import MafIO
import pandas as pd
import sys
import pickle


# Save the run index
run = int(sys.argv[1])
# Load parameters
with open('../params.pickle', 'rb') as f:
    [path, species1, species2, species3, species4, target_seqname, big_maf_file] = pickle.load(f)
# Load mafindex
idx = MafIO.MafIndex('../filtered.mafindex', '../filtered.maf', target_seqname)
# Parse the alignment
results = idx.search([int(sys.argv[2])], [int(sys.argv[3])])

# Save whether the target_seqname is part of the trio + outgroup
is_target = target_seqname.split('.')[0] in [species1, species2, species3, species4]
# Create empty dictionary
idx = {}
# If the target is not part of the trio + outgroup
if not is_target:
    # For each species in the trio + outgroup
    for i, name in enumerate([species1, species2, species3, species4]):
        # Add a mapping index to the dictionary
        idx[name] = i
    # Add a mapping index of 4 to the target_seqname species
    idx[target_seqname.split('.')[0]] = 4

# Create an empty dataframe
df = pd.DataFrame(columns = ['file', 'species', 'chr', 'start', 'gaps'])
with open('../fasta_names_test/run_{}.txt'.format(run), 'w') as f:
    # For each of the alignments
    for i, align in enumerate(results):
        f.write('fasta_{}.fa\n'.format(i))
        # Create empty dictionary
        dct = {'species':[], 'chr':[], 'start':[],'gaps':[]}
        # For each of the records
        for record in align:
            record.id = record.name.split('.')[0]
            record.description = record.name.split('.')[0]
            # Retrieve species
            dct['species'].append(record.name.split('.')[0])
            # Retrieve chromosome/contig
            dct['chr'].append('.'.join(record.name.split('.')[1:]))
            # Retrieve start coordinate
            dct['start'].append(record.annotations['start'])
            # Retrieve gaps encoded in a binary format
            dct['gaps'].append(''.join([str(0) if n=='-' else str(1) for n in record.seq]))
        # If the target species is not in the trio + outgroup
        if not is_target:
            # Order the aligned sequences according to the index dictionary
            align.sort(key = lambda record: idx[record.name.split('.')[0]])
            # Get rid of the target_seqname sequence
            align = align[:4,:]
        # Save individual fasta file
        AlignIO.write(align, '../inputs_test/run_{}/fasta_{}.fa'.format(run, i), "fasta")
        # Convert dictionary to data frame
        file_df = pd.DataFrame.from_dict(dct)
        # Insert column mapping to the file
        file_df.insert(0, 'file', i, True)
        # Append rows to overall data frame
        df = df.append(file_df)

# Save the csv file
df.to_csv('../info_tables_test/run_{}.csv'.format(run), index=False)

















