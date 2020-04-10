# This script collects all individual HDF5 tables and appends them to a bigger HDF5 file
# whose key is the species.chr that the maffiltering is based on. 

import pandas as pd
import sys
import os
import pickle

target_seqname = sys.argv[1]

slice_lst = pickle.load(open('../slice_lst.pickle', 'rb'))

store = pd.HDFStore('../../final_table.HDF', complib='blosc')

for run in range(len(slice_lst)):
    # Load the info table with the coordinates and the gap information
    info_table = pd.read_csv('../info_tables/run_{}.csv'.format(run))
    chrom = {}
    # Add species as keys to the dictionaries
    for species in list(set(info_table['species'])):
        chrom['chr.'+species] = 30
    df = pd.read_hdf('../results/run_{}.HDF'.format(run))
    store.append(key=target_seqname,value=df,format='t',data_columns=list(set(info_table['species'])),
                 min_itemsize=chrom, complevel=9)

store.close()