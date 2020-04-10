#!/bin/bash

### This script create a file containing the parameters for coalhmm
### It takes five arguments: a maf file to be filtered and four species names

species1=$1
species2=$2
species3=$3
species4=$4

echo "coalmethod=ILS(\\" > ../params.file
echo "    implementation=09,\\" >> ../params.file
echo "    nbSpecies=3,\\" >> ../params.file
echo "    species1=$1,\\" >> ../params.file
echo "    species2=$2,\\" >> ../params.file
echo "    species3=$3,\\" >> ../params.file
echo "    outgroup=$4,\\" >> ../params.file
echo "    tau1=0.004,\\" >> ../params.file
echo "    tau2=0.0015,\\" >> ../params.file
echo "    c2=0.010,\\" >> ../params.file
echo "    theta1=0.002,\\" >> ../params.file
echo "    theta2=0.002,\\" >> ../params.file
echo "    median=no,\\" >> ../params.file
echo "    rho=0.2,\\" >> ../params.file
echo "    tau.min = 0.0001,\\" >> ../params.file
echo "    theta.min = 0.0001,\\" >> ../params.file
echo "    rho.min = 0.0001,\\" >> ../params.file
echo "    rho.max = 1000\\" >> ../params.file
echo "  )" >> ../params.file

echo "alphabet=DNA" >> ../params.file
echo "input.sequence.multiparts=yes" >> ../params.file

echo "input.sequence.multiparts.reset=yes" >> ../params.file

echo "input.sequence.format=Fasta" >> ../params.file

echo "input.sequence.sites_to_use=all" >> ../params.file
echo "input.sequence.max_gap_allowed=50%" >> ../params.file
echo "model=GTR(a=1.0, b=1.0, c=1.0, d=1.0, e=1.0, theta=0.5, theta1 = 0.5, theta2 = 0.5)" >> ../params.file
echo "rate_distribution=Gamma(n=4, alpha=1.0)" >> ../params.file

echo "analysis=estimate" >> ../params.file

echo "optimize=yes" >> ../params.file
echo "optimization.method=fullD" >> ../params.file
echo "optimization.reparametrization=no" >> ../params.file
echo "optimization.verbose=2" >> ../params.file
echo "optimization.tolerance=0.0001" >> ../params.file
echo "optimization.max_number_f_eval=1000000" >> ../params.file
echo "optimization.max_number_iterations=2000" >> ../params.file
echo "optimization.pre=yes" >> ../params.file
echo "optimization.ignore_parameter=GTR.a,GTR.b,GTR.c,GTR.d,GTR.e,GTR.theta,GTR.theta1,GTR.theta2" >> ../params.file
echo "optimization.final=no" >> ../params.file

