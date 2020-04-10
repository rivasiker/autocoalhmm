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
echo -e "maf.filter=Subset(species=($2, $3, $4, $5), strict=yes, keep=no, remove_duplicates=yes), XFullGap(species=($2, $3, $4, $5)), Merge(species=($2, $3, $4, $5)), MaskFilter(species=($2, $3, $4, $5), window.size=100, window.step=1, max.masked=80), Merge(species=($2, $3, $4, $5), dist_max=100, rename_chimeric_chromosomes=yes), MinBlockLength(min_length=500), SequenceStatistics(statistics=(BlockLength,AlnScore,BlockCounts),ref_species=$2,file=../data.statistics.csv,compression=none), Output(file=../filtered.maf, compression=none, mask=yes)" >> ../control_file

