from Bio import AlignIO
from Bio.AlignIO import MafIO
import os
import pandas as pd
import sys
from gwf import Workflow
import pickle

gwf = Workflow()

if len(pickle.load(open('../params.pickle', 'rb'))) == 7:
    with open('../params.pickle', 'rb') as f:
        [path, species1, species2, species3, species4, target_seqname, big_maf_file] = pickle.load(f)
ifelse len(pickle.load(open('../params.pickle', 'rb'))) == 8:
    with open('../params.pickle', 'rb') as f:
        [path, species1, species2, species3, species4, target_seqname, big_maf_file, error_sp1] = pickle.load(f)
ifelse len(pickle.load(open('../params.pickle', 'rb'))) == 9:
    with open('../params.pickle', 'rb') as f:
        [path, species1, species2, species3, species4, target_seqname, big_maf_file, error_sp1, error_sp2] = pickle.load(f)

with open('../slice_lst.pickle', 'rb') as f:
    slice_lst = pickle.load(f)
indices = [len(slice_lst)//4, len(slice_lst)//2, (len(slice_lst)//4)*3]
slice_lst = [slice_lst[i] for i in indices]

if not os.path.isdir('../info_tables_test'):
	os.mkdir('../info_tables_test')
if not os.path.isdir('../fasta_names_test'):
	os.mkdir('../fasta_names_test')
if not os.path.isdir('../inputs_test'):
	os.mkdir('../inputs_test')
if not os.path.isdir('../outputs_test'):
	os.mkdir('../outputs_test')


# For each slice of the maffilter
for run in range(len(slice_lst)):
    
    if not os.path.isdir('../inputs_test/run_{}'.format(run)):
        # Create temporary directory with coalHMM run index
        os.mkdir('../inputs_test/run_{}'.format(run))
    if not os.path.isdir('../outputs_test/run_{}'.format(run)):
        # Create temporary directory with coalHMM run index
        os.mkdir('../outputs_test/run_{}'.format(run))


    # Create input and output lists for the gwf run
    inputs_test = ['../filtered.mafindex', '../filtered.maf']
    outputs_test = ['../inputs_test/run_{}/fasta_{}.fa'.format(run, j) for j in range(slice_lst[run][2])]
    outputs_test = outputs_test + ['../info_tables_test/run_{}.csv'.format(run), '../fasta_names_test/run_{}.txt'.format(run)]
    # Save individual fasta files and info df
    gwf.target('run_{}'.format(run), 
                inputs=inputs_test, 
                outputs=outputs_test,
                cores=4,
                memory='4g',
                walltime= '02:00:00') << """
    python create_fasta_and_info_table.py {} {} {}
    """.format(run, slice_lst[run][0], slice_lst[run][1])


    # Define format of output paths
    out = '../outputs_test/run_{}/'.format(run)
    results = ['../outputs_test/run_{}/estimates'.format(run),
                '../outputs_test/run_{}/posterior_states'.format(run),
                '../outputs_test/run_{}/posteriors'.format(run), 
                '../outputs_test/run_{}/hidden_states'.format(run),
                '../outputs_test/run_{}/divergences'.format(run)]
    # Run coalhmm
    gwf.target('coalhmm_run_{}'.format(run), 
                inputs=outputs_test, 
                outputs=results,
                cores=4, 
                memory='4g', 
                walltime= '04:00:00',
                account='Primategenomes') << """
    export LD_LIBRARY_PATH=.
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/local/bpp/dev/lib64
    export LD_LIBRARY_PATH=/home/iker/Programs/anaconda3/lib:$LD_LIBRARY_PATH
    ./coalhmm --noninteractive=yes param=../params_test.file species1={} species2={} species3={} outgroup={} \
    input.sequence.multiparts=yes input.sequence.format=Fasta input.sequence.list={} input.sequence.multiparts.prefix={} \
    input.sequence.multiparts.reset=yes optimization.profiler={}profiler optimization.message_handler={}messages \
    output.posterior.states={}posterior_states output.hidden_states={}hidden_states output.hidden_states.divergences={}divergences \
    output.posterior.values={}posteriors output.estimated.parameters={}params output.userfriendly.parameters={}estimates \
    input.sequence.sites_to_use=all input.sequence.max_gap_allowed=50%
    """.format(species1, species2, species3, species4, 
                '../fasta_names_test/run_{}.txt'.format(run), 
                '../inputs_test/run_{}/'.format(run), 
                out, out, out, out, out, out, out, out)



gwf.target('new_params', 
            inputs=['../outputs_test/run_{}/estimates'.format(run) for run in [0, 1, 2]], 
            outputs=['../params.file'],
            cores=1,
            memory='4g',
            walltime= '00:10:00') << """
python retrieve_params.py
"""

gwf.target('send_coalhmm', 
            inputs=['../params.file'], 
            outputs=['../final_table.HDF'],
            cores=1,
            memory='1g',
            walltime= '01:00:00') << """
cd ../coalhmm/
gwf config set backend slurm
gwf run
"""

