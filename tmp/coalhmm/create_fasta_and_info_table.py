# This script is used for saving the individual fasta files and the info table for a certain 
# coalHMM run. The start and end coordinated for the maf slicing are supplied by the first
# two areguments respectively, and the run number is specified as a third argument. All
# in all, this script can be run using:
#       
#       python create_fasta_and_info_table.py start_coord end_coord run_number

from Bio import AlignIO
from Bio.AlignIO import MafIO
import pandas as pd
import sys


# Save the run index
run = int(sys.argv[1])
target_seqname = sys.argv[2]
# Load mafindex
idx = MafIO.MafIndex('../filtered.mafindex', '../filtered.maf', target_seqname)
# Parse the alignment
results = idx.search([int(sys.argv[3])], [int(sys.argv[4])])


# Create an empty dataframe
df = pd.DataFrame(columns = ['file', 'species', 'chr', 'start', 'gaps'])
with open('../fasta_names/run_{}.txt'.format(run), 'w') as f:
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
        # Save individual fasta file
        AlignIO.write(align, '../inputs/run_{}/fasta_{}.fa'.format(run, i), "fasta")
        # Convert dictionary to data frame
        file_df = pd.DataFrame.from_dict(dct)
        # Insert column mapping to the file
        file_df.insert(0, 'file', i, True)
        # Append rows to overall data frame
        df = df.append(file_df)

# Save the csv file
df.to_csv('../info_tables/run_{}.csv'.format(run), index=False)

















