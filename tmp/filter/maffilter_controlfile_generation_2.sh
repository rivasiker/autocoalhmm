#!/bin/bash

### This script create a control file for maffiler ###
### It takes six arguments: a maf file to be filtered, four species names
### and the target seqname

echo "input.file=$1" > ../control_file
echo "input.file.compression=gzip" >> ../control_file
echo "input.format=Maf" >> ../control_file
echo "output.log=../maf_filtering.log" >> ../control_file
echo "maf.filter=Subset(species=($2, $3, $4, $5, $6), strict=yes, keep=no, remove_duplicates=yes, verbose=no), \\" >> ../control_file
echo "XFullGap(species=($2, $3, $4, $5, $6), verbose=no), \\" >> ../control_file
echo "Merge(species=($6), dist_max=200, rename_chimeric_chromosomes=yes, verbose=no), \\" >> ../control_file
echo "MinBlockLength(min_length=2000, verbose=no), \\" >> ../control_file
echo "Output(file=../filtered.maf, compression=none, mask=yes)" >> ../control_file
