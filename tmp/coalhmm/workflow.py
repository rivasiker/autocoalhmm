from Bio import AlignIO
from Bio.AlignIO import MafIO
import os
import pandas as pd
import sys
from gwf import Workflow
import pickle

gwf = Workflow()

with open('../params.pickle', 'rb') as f:
    [path, species1, species2, species3, species4, target_seqname, big_maf_file] = pickle.load(f)

with open('../slice_lst.pickle', 'rb') as f:
    slice_lst = pickle.load(f)

if not os.path.isdir('../info_tables'):
	os.mkdir('../info_tables')
if not os.path.isdir('../fasta_names'):
	os.mkdir('../fasta_names')
if not os.path.isdir('../inputs'):
	os.mkdir('../inputs')
if not os.path.isdir('../outputs'):
	os.mkdir('../outputs')
if not os.path.isdir('../results/'):
	os.mkdir('../results/')

# For each slice of the maffilter
for run in range(len(slice_lst)):
    
    if not os.path.isdir('../inputs/run_{}'.format(run)):
        # Create temporary directory with coalHMM run index
        os.mkdir('../inputs/run_{}'.format(run))
    if not os.path.isdir('../outputs/run_{}'.format(run)):
        # Create temporary directory with coalHMM run index
        os.mkdir('../outputs/run_{}'.format(run))


    # Create input and output lists for the gwf run
    inputs = ['../filtered.mafindex', '../filtered.maf']
    outputs = ['../inputs/run_{}/fasta_{}.fa'.format(run, j) for j in range(slice_lst[run][2])]
    outputs = outputs + ['../info_tables/run_{}.csv'.format(run), '../fasta_names/run_{}.txt'.format(run)]
    # Save individual fasta files and info df
    gwf.target('run_{}'.format(run), 
                inputs=inputs, 
                outputs=outputs,
                cores=4,
                memory='4g',
                walltime= '02:00:00') << """
    python create_fasta_and_info_table.py {} {} {} {}
    """.format(run, target_seqname, slice_lst[run][0], slice_lst[run][1])


    # Define format of output paths
    out = '../outputs/run_{}/'.format(run)
    results = ['../outputs/run_{}/estimates'.format(run),
                '../outputs/run_{}/posterior_states'.format(run),
                '../outputs/run_{}/posteriors'.format(run), 
                '../outputs/run_{}/hidden_states'.format(run),
                '../outputs/run_{}/divergences'.format(run)]
    # Run coalhmm
    gwf.target('coalhmm_run_{}'.format(run), 
                inputs=outputs, 
                outputs=results,
                cores=4, 
                memory='4g', 
                walltime= '01:00:00',
                account='Primategenomes') << """
    ./coalhmm --noninteractive=yes param=../params.file species1={} species2={} species3={} outgroup={} \
    input.sequence.multiparts=yes input.sequence.format=Fasta input.sequence.list={} input.sequence.multiparts.prefix={} \
    input.sequence.multiparts.reset=yes optimization.profiler={}profiler optimization.message_handler={}messages \
    output.posterior.states={}posterior_states output.hidden_states={}hidden_states output.hidden_states.divergences={}divergences \
    output.posterior.values={}posteriors output.estimated.parameters={}params output.userfriendly.parameters={}estimates \
    input.sequence.sites_to_use=all input.sequence.max_gap_allowed=50%
    """.format(species1, species2, species3, species4, 
                '../fasta_names/run_{}.txt'.format(run), 
                '../inputs/run_{}/'.format(run), 
                out, out, out, out, out, out, out, out)

    # Collect results from each of the runs and combine them with the coordinates
    gwf.target('collect_run_{}'.format(run), 
                inputs=['../info_tables/run_{}.csv'.format(run), '../outputs/run_{}/posteriors'.format(run)], 
                outputs=['../results/run_{}.HDF'.format(run)],
                cores=1,
                memory='4g',
                walltime= '01:00:00',
                account='Primategenomes') << """
    python collect_posteriors.py {}
    """.format(run)


gwf.target('final_table', 
            inputs=['../results/run_{}.HDF'.format(i) for i in range(len(slice_lst))], 
            outputs=['../../final_table.HDF'],
            cores=1,
            memory='32g',
            walltime= '08:00:00',
            account='Primategenomes') << """
python create_big_table.py {}
""".format(target_seqname)


