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


gwf.target('Maffilter_control_file', 
           inputs=[big_maf_file], 
		   outputs=['../filtered.maf', '../maf_filtering.log'],
		   cores=1,
    	   memory='10g',
		   walltime= '12:00:00',
		   account='Primategenomes') << """
./maffilter_controlfile_generation.sh {} {} {} {} {}
./coalhmm_paramfile_generation.sh {} {} {} {}
./maffilter param=../control_file
python3 start_end.py
cd ../coalhmm/
gwf config set backend slurm
gwf run
""".format(big_maf_file, species1, species2, species3, species4, species1, species2, species3, species4)