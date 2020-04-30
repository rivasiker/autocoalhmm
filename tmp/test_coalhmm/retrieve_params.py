# This script can be used to retrieve the parameter information and the 
# general information for each of the runs in an autocoalHMM computation.
# The inputs are the estimated parameter files for each of the runs, and the
# output will contain the following in a csv file:
#   - The start and end position of each run.
#   - The number of chunks for each run.
#   - The estimates tau1, tau2, tau3, theta1, theta2, theta3, c2 and rho per run.

import pandas as pd
import sys
import pickle

# Collect parameters
dct = {'tau1':[], 'tau2':[], 'theta1':[], 'theta2':[], 'c2':[], 'rho':[]}
for i in [0, 1, 2]:
    with open('../outputs_test/run_{}/estimates'.format(i), 'r') as new:
        for tree in new:
            if 'tau1' in tree:
                dct['tau1'].append(float(tree[7:]))
            if 'tau2' in tree:
                dct['tau2'].append(float(tree[7:]))
            if 'theta1' in tree:
                dct['theta1'].append(float(tree[9:]))
            if 'theta2' in tree:
                dct['theta2'].append(float(tree[9:]))
            if 'c2' in tree:
                dct['c2'].append(float(tree[5:]))
            if 'rho' in tree:
                dct['rho'].append(float(tree[6:]))
                break

# Save new parameter file
with open('../params_test.file', 'r') as old:
    with open('../params.file', 'w') as new:
        for line in old:
            if 'tau1=0.001' in line:
                new.write(line.replace('tau1=0.001', 'tau1={}'.format(sum(dct['tau1'])/3)))
            elif 'tau2=0.001' in line:
                new.write(line.replace('tau2=0.001', 'tau2={}'.format(sum(dct['tau2'])/3)))
            elif 'c2=0.03' in line:
                new.write(line.replace('c2=0.03', 'c2={}'.format(sum(dct['c2'])/3)))
            elif 'theta1=0.001' in line:
                new.write(line.replace('theta1=0.001', 'theta1={}'.format(sum(dct['theta1'])/3)))
            elif 'theta2=0.001' in line:
                new.write(line.replace('theta2=0.001', 'theta2={}'.format(sum(dct['theta2'])/3)))
            elif 'rho=0.5' in line:
                new.write(line.replace('rho=0.5', 'rho={}'.format(sum(dct['rho'])/3)))
            else:
                new.write(line)

