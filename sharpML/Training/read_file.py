#!/usr/bin/env python

import sys
import pickle
import numpy as np
import pandas as pd

file_in = "data.txt"

method = sys.argv[1]

if method == 'standard':
    X = []
    with open(file_in, 'r') as fin:
        for line in fin.readlines():
            X.append(line.strip().split())
elif method == 'pickle':
    with open(file_in, 'rb') as fin:
        X = pickle.load(fin)
elif method == 'numpy':
    X = np.loadtxt(file_in)
elif method == 'pandas':
    X = pd.read_csv(file_in)
else:
    print("Not implemented")

print (X)

