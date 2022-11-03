# autoCoalHMM

[![DOI](https://zenodo.org/badge/254589955.svg)](https://zenodo.org/badge/latestdoi/254589955)

This script can be used to run coalHMM given a specific set of arguments. It performs
the filtering of the input maf file, such that a temporary filtered maf file is
generated. This filtered maf file will only contain those species that were specified
in the script call. Using the filtered maf file, autocoalhmm.py also divides the 
alignment into roughly 1 Mb windows and performs coalHMM on them. Finally, it also
collects all the results and saves them into a user-friendly HDF5 table with the
coordinates of the maf file. 

Note that the workflow will only run with slurm backends. In order to run it, 
manual modification of the gwf workflows might be necessary.

IMPORTANT: when cloning the GitHub repo, the permissions for all files need to be
changed. You can do so by running `chmod -R 777 ./`.

The way autocoalhmm.py is invoked:
```
python autocoalhmm.py sp1 sp2 sp3 sp4 target_seqname maf_path
```
If the 1-species unclock model needs to be run, then use:
```
python autocoalhmm.py sp1 sp2 sp3 sp4 target_seqname maf_path error_sp1
```
If the 2-species unclock model needs to be run, then use:
```	
python autocoalhmm.py sp1 sp2 sp3 sp4 target_seqname maf_path error_sp1 error_sp2
```
Where:
- `sp1`, `sp2` and `sp3` are the species of the analyzed branch.
- `sp4` is the outrgroup species.
- `target_seqname` is the reference sequence, in the form of `species.chr`.
- `maf_path` is the path to the unfiltered maf file. 

The workflow steps are executed as follows:
1. autocoalhmm.py saves the variables and copies the temporary directories that contain all the machinery into the working directory.
2. autocoalhmm.py calls the filtering workflow, which will
    1. filter the maf file: only specified species, merging...
    2. compute the mafindex of the filtered maf file.
    3. calculate the 1Mb window breakpoints and save the slicing coordinates.
3. The filtering workflow will finish by executing the testing workflow, which will:
		1. take a sample from the slicing of the filtered maf file (1st, 2nd and 3rd quantile).
		2. generate the necessary files for running coalHMM and mapping the result back to the coordinate system. 
		3. run coalHMM on these three 1Mb regions with default starting params.
		4. compute the mean of the estimated params and save them into new param file.
4. The testing workflow will finish by executing the coalHMM workflow, which will:
		1. split the filtered maf file into the 1 Mb slices computed before
		2. generate the necessary files for running coalHMM and mapping the result back to the coordinate system. 
		3. run coalHMM for each of the previously calculated slices.
		4. save the posterior probabilities into individual HDF5 files. 
		5. collect all individual HDF5 files.

Depending on whether target_seqname is part of the three species in the trio + outrgoup
or not, it will behave differently:
- If the target is within the other species, then the intermediate info tables and the final HDF table will contain the coordinates of those four species. 
- If the target is not within the other species, then the intermediate info tables and the final HDF table will contain the coordinates of all five species. However, for the coalHMM run only the trio + outgroup species will be kept. 
