from Bio import AlignIO
from Bio.AlignIO import MafIO
import os
import pandas as pd
import sys
from gwf import Workflow
import pickle

gwf = Workflow()

# Load the parameters
with open('../params.pickle', 'rb') as f:
    [path, species1, species2, species3, species4, target_seqname, big_maf_file] = pickle.load(f)

is_target = target_seqname.split('.')[0] in [species1, species2, species3, species4]
if is_target:
	# Run maf filtering
	gwf.target('Maffilter', 
			inputs=[big_maf_file], 
			outputs=['../filtered.maf', '../maf_filtering.log'],
			cores=8,
			memory='16g',
			walltime= '12:00:00',
			account='Primategenomes') << """
	./maffilter_controlfile_generation.sh {} {} {} {} {} {}
	./coalhmm_paramfile_generation.sh {} {} {} {}
	./maffilter param=../control_file
	""".format(big_maf_file, species1, species2, species3, species4, target_seqname.split('.')[0], species1, species2, species3, species4)
else:
	# Run maf filtering
	gwf.target('Maffilter_2', 
			inputs=[big_maf_file], 
			outputs=['../filtered.maf', '../maf_filtering.log'],
			cores=8,
			memory='16g',
			walltime= '12:00:00',
			account='Primategenomes') << """
	./maffilter_controlfile_generation_2.sh {} {} {} {} {} {}
	./coalhmm_paramfile_generation.sh {} {} {} {}
	./maffilter param=../control_file
	""".format(big_maf_file, species1, species2, species3, species4, target_seqname.split('.')[0], species1, species2, species3, species4)

# Divide alignment in 1Mb regions
gwf.target('Start_end', 
           inputs=['../filtered.maf', '../maf_filtering.log'], 
		   outputs=['../slice_lst.pickle', '../filtered.mafindex'],
		   cores=4,
    	   memory='16g',
		   walltime= '04:00:00',
		   account='Primategenomes') << """
python3 start_end.py
"""

# Run the testing coalHMM runs
gwf.target('coalHMM_test', 
           inputs=['../filtered.maf', '../slice_lst.pickle', '../filtered.mafindex'], 
		   outputs=['../params.file'],
		   cores=1,
    	   memory='1g',
		   walltime= '00:10:00',
		   account='Primategenomes') << """
cd ../test_coalhmm/
gwf config set backend slurm
gwf run
"""
