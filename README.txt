################################## AUTOCOALHMM ##################################

This script can be used to run coalHMM given a specific set of arguments. It performs
the filtering of the input maf file, such that a temporary filtered maf file is
generated. This filtered maf file will only contain those species that were specified
in the script call. Using the filtered maf file, autocoalhmm.py also divides the 
alignment into roughly 1 Mb windows and performs coalHMM on them. Finally, it also
collects all the results and saves them into a user-friendly HDF5 table with the
coordinates of the maf file. 

The way autocoalhmm.py is invoked:
	python autocoalhmm.py sp1 sp2 sp3 sp4 target_seqname maf_path
Where:
	- sp1, sp2 and sp3 are the species of the analyzed branch.
	- sp4 is the outrgroup species.
	- target_seqname is the reference sequence, in the form of species.chr.
	- maf_path is the path to the unfiltered maf file. 

The workflow steps are executed as follows:
	1)	autocoalhmm.py saves the variables and copies the temporary directories 
		that contain all the machinery into the working directory.
	2)	autocoalhmm.py calls the filtering workflow, which will
		a)	filter the maf file: only specified species, merging...
		b)	compute the mafindex of the filtered maf file.
		c)	calculate the window breakpoints and save the slicing coordinates.
	3)	The filtering workflow will finish by executing the coalHMM workflow, which
		will:
		a)	split the filtered maf file into the 1 Mb slices computed before, and 
			generate the necessary files for running coalHMM and mapping the result
			back to the coordinate system. 
		b) 	run coalHMM for each of the previously calculated slices.
		c)	save the posterior probabilities into individual HDF5 files. 
		d)	collect all individual HDF5 files