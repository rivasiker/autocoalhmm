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
dct = {'tau1':[], 'tau2':[], 'theta1':[], 'theta2':[], 'c2':[], 'rho':[], 'GTR_a':[], 'GTR_b':[], 'GTR_c':[], 'GTR_d':[], 'GTR_e':[], 'GTR_theta':[], 'GTR_theta1':[], 'GTR_theta2':[], 'GTR_alpha':[]}
for i in [0, 1, 2]:
    with open('../outputs_test/run_{}/estimates'.format(i), 'r') as new:
        for tree in new:
            if 'GTR.a' in tree:
                dct['GTR_a'].append(float(tree[8:]))
            elif 'GTR.b' in tree:
                dct['GTR_b'].append(float(tree[8:]))
            elif 'GTR.c' in tree:
                dct['GTR_c'].append(float(tree[8:]))
            elif 'GTR.d' in tree:
                dct['GTR_d'].append(float(tree[8:]))
            elif 'GTR.e' in tree:
                dct['GTR_e'].append(float(tree[8:]))
            elif 'GTR.theta ' in tree:
                dct['GTR_theta'].append(float(tree[13:]))
            elif 'GTR.theta1' in tree:
                dct['GTR_theta1'].append(float(tree[12:]))
            elif 'GTR.theta2' in tree:
                dct['GTR_theta2'].append(float(tree[12:]))
            elif 'Gamma.alpha' in tree:
                dct['GTR_alpha'].append(float(tree[13:]))
                break
            elif 'tau1' in tree:
                dct['tau1'].append(float(tree[7:]))
            elif 'tau2' in tree:
                dct['tau2'].append(float(tree[7:]))
            elif 'theta1' in tree:
                dct['theta1'].append(float(tree[9:]))
            elif 'theta2' in tree:
                dct['theta2'].append(float(tree[9:]))
            elif 'c2' in tree:
                dct['c2'].append(float(tree[5:]))
            elif 'rho' in tree:
                dct['rho'].append(float(tree[6:]))

# Save new parameter file
with open('../params_test.file', 'r') as old:
    with open('../params.file', 'w') as new:
        for line in old:
            if 'tau1=0.001' in line:
                new.write(line.replace('tau1=0.001', 'tau1={}'.format(round(sum(dct['tau1'])/len(dct['tau1']), 5))))
            elif 'tau2=0.001' in line:
                new.write(line.replace('tau2=0.001', 'tau2={}'.format(round(sum(dct['tau2'])/len(dct['tau2']), 5))))
            elif 'c2=0.03' in line:
                new.write(line.replace('c2=0.03', 'c2={}'.format(round(sum(dct['c2'])/len(dct['c2']), 5))))
            elif 'theta1=0.001' in line:
                new.write(line.replace('theta1=0.001', 'theta1={}'.format(round(sum(dct['theta1'])/len(dct['theta1']), 5))))
            elif 'theta2=0.001' in line:
                new.write(line.replace('theta2=0.001', 'theta2={}'.format(round(sum(dct['theta2'])/len(dct['theta2']), 5))))
            elif 'rho=0.5' in line:
                new.write(line.replace('rho=0.5', 'rho={}'.format(round(sum(dct['rho'])/len(dct['rho']), 5))))
            elif 'model=GTR(a=1.0, b=1.0, c=1.0, d=1.0, e=1.0, theta=0.5, theta1 = 0.5, theta2 = 0.5)' in line:
                line = line.replace('a=1.0', 'a={}'.format(round(sum(dct['GTR_a'])/len(dct['GTR_a']), 5)))
                line = line.replace('b=1.0', 'b={}'.format(round(sum(dct['GTR_b'])/len(dct['GTR_b']), 5)))
                line = line.replace('c=1.0', 'c={}'.format(round(sum(dct['GTR_c'])/len(dct['GTR_c']), 5)))
                line = line.replace('d=1.0', 'd={}'.format(round(sum(dct['GTR_d'])/len(dct['GTR_d']), 5)))
                line = line.replace('e=1.0', 'e={}'.format(round(sum(dct['GTR_e'])/len(dct['GTR_e']), 5)))
                line = line.replace('theta=0.5', 'theta={}'.format(round(sum(dct['GTR_theta'])/len(dct['GTR_theta']), 5)))
                line = line.replace('theta1 = 0.5', 'theta1={}'.format(round(sum(dct['GTR_theta1'])/len(dct['GTR_theta1']), 5)))
                line = line.replace('theta2 = 0.5', 'theta2={}'.format(round(sum(dct['GTR_theta2'])/len(dct['GTR_theta2']), 5)))
                new.write(line)
            elif 'rate_distribution=Gamma(n=4, alpha=1.0)' in line:
                new.write(line.replace('alpha=1.0', 'alpha={}'.format(round(sum(dct['GTR_alpha'])/len(dct['GTR_alpha']), 5))))
            elif 'optimization.ignore_parameter=GTR.a,GTR.b,GTR.c,GTR.d,GTR.e,GTR.theta,GTR.theta1,GTR.theta2' in line:
                continue
            else:
                new.write(line)
        new.write('optimization.ignore_parameter=GTR.a,GTR.b,GTR.c,GTR.d,GTR.e,GTR.theta,GTR.theta1,GTR.theta2')

