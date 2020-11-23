#!/bin/bash

### This script create a file containing the parameters for coalhmm
### It takes five arguments: a maf file to be filtered and four species names

species1=$1
species2=$2
species3=$3
species4=$4
errorsp1=$5
errorsp2=$6

echo "coalmethod=Unclock(species1=$5, error1=0.01, species2=$6, error2=0.01, model=ILS(\\" > ../params_test.file
echo "    implementation=09,\\" >> ../params_test.file
echo "    nbSpecies=3,\\" >> ../params_test.file
echo "    species1=$1,\\" >> ../params_test.file
echo "    species2=$2,\\" >> ../params_test.file
echo "    species3=$3,\\" >> ../params_test.file
echo "    outgroup=$4,\\" >> ../params_test.file
echo "    tau1=0.001,\\" >> ../params_test.file
echo "    tau2=0.001,\\" >> ../params_test.file
echo "    c2=0.03,\\" >> ../params_test.file
echo "    theta1=0.001,\\" >> ../params_test.file
echo "    theta2=0.001,\\" >> ../params_test.file
echo "    median=no,\\" >> ../params_test.file
echo "    rho=0.5,\\" >> ../params_test.file
echo "    tau.min = 0.00001,\\" >> ../params_test.file
echo "    theta.min = 0.00001,\\" >> ../params_test.file
echo "    rho.min = 0.0001,\\" >> ../params_test.file
echo "    rho.max = 1000\\" >> ../params_test.file
echo "  )" >> ../params_test.file

echo "alphabet=DNA" >> ../params_test.file
echo "input.sequence.multiparts=yes" >> ../params_test.file

echo "input.sequence.multiparts.reset=yes" >> ../params_test.file

echo "input.sequence.format=Fasta" >> ../params_test.file

echo "input.sequence.sites_to_use=all" >> ../params_test.file
echo "input.sequence.max_gap_allowed=50%" >> ../params_test.file
echo "model=GTR(a=1.0, b=1.0, c=1.0, d=1.0, e=1.0, theta=0.5, theta1 = 0.5, theta2 = 0.5)" >> ../params_test.file
echo "rate_distribution=Gamma(n=4, alpha=1.0)" >> ../params_test.file

echo "analysis=estimate" >> ../params_test.file

echo "optimize=yes" >> ../params_test.file
echo "optimization.method=fullD" >> ../params_test.file
echo "optimization.reparametrization=no" >> ../params_test.file
echo "optimization.verbose=2" >> ../params_test.file
echo "optimization.tolerance=0.0001" >> ../params_test.file
echo "optimization.max_number_f_eval=1000000" >> ../params_test.file
echo "optimization.max_number_iterations=2000" >> ../params_test.file
echo "optimization.pre=yes" >> ../params_test.file
echo "optimization.ignore_parameter=GTR.a,GTR.b,GTR.c,GTR.d,GTR.e,GTR.theta,GTR.theta1,GTR.theta2" >> ../params_test.file
echo "optimization.final=no" >> ../params_test.file
