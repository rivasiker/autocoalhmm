#!/bin/bash

### This script create a control file for maffiler ###
### It takes five arguments: a maf file to be filtered and four species names

maffile=$1
species1=$2
species2=$3
species3=$4
species4=$5

echo "input.file=$1" > ../control_file
echo "input.file.compression=gzip" >> ../control_file
echo "input.format=Maf" >> ../control_file
echo "output.log=../maf_filtering.log" >> ../control_file
echo "maf.filter=Subset(species=($2, $3, $4, $5), strict=yes, keep=no, remove_duplicates=yes), \\" >> ../control_file
echo "XFullGap(species=($2, $3, $4, $5)), \\" >> ../control_file
echo "Merge(species=(Homo_sapiens), dist_max=500, rename_chimeric_chromosomes=yes), \\" >> ../control_file
echo "MinBlockLength(min_length=2500), \\" >> ../control_file
echo "Output(file=../filtered.maf, compression=none, mask=yes)" >> ../control_file
