
# This script can create final_table.HDF files for all those chromosomes
# which have at least one run that did not converge. 

import pandas as pd
import sys
import os
import pickle



def optimize_dataframe(df, down_int='integer'):
    # down_int can also be 'unsigned'
    
    converted_df = pd.DataFrame()

    floats_optim = (df
                    .select_dtypes(include=['float'])
                    .apply(pd.to_numeric,downcast='float')
                   )
    converted_df[floats_optim.columns] = floats_optim

    ints_optim = (df
                    .select_dtypes(include=['int'])
                    .apply(pd.to_numeric,downcast=down_int)
                   )
    converted_df[ints_optim.columns] = ints_optim

    for col in df.select_dtypes(include=['object']).columns:
        num_unique_values = len(df[col].unique())
        num_total_values = len(df[col])
        if num_unique_values / num_total_values < 0.5:
            converted_df[col] = df[col].astype('category')
        else:
            converted_df[col] = df[col]

    unchanged_cols = df.columns[~df.columns.isin(converted_df.columns)]
    converted_df[unchanged_cols] = df[unchanged_cols]

    # keep columns order
    converted_df = converted_df[df.columns]      
            
    return converted_df


# Define the target sequence
target_seqname = sys.argv[1]

slice_lst = pickle.load(open('../slice_lst.pickle', 'rb'))

store = pd.HDFStore('../../final_table.HDF', complib='blosc')

for run in range(len(slice_lst)):
    # Load the info table with the coordinates and the gap information
    info_table = pd.read_csv('../info_tables/run_{}.csv'.format(run))
    df = pd.read_hdf('../results/run_{}.HDF'.format(run))
    df = df[['Homo_sapiens','V0','V1','V2','V3']]
    df = optimize_dataframe(df)
    store.append(key=target_seqname.replace('.', '_'),value=df,
    format='t',data_columns=['Homo_sapiens'],complevel=9)

store.close()