#!/usr/bin/env python

import sys
import pickle
import numpy as np
import pandas as pd

X = np.arange(0,12).reshape(4,3)
file_out = "data.txt"

method = sys.argv[1]

if method == 'standard':
    with open(file_out, 'w') as fout:
        fout.write(str(X))
elif method == 'pickle':
    with open(file_out, 'wb') as fout:
        pickle.dump(X,fout)
elif method == 'numpy':
    np.savetxt(file_out, X)
elif method == 'pandas':
    df = pd.DataFrame(X, columns = ['a','b','c'])
    df.to_csv(file_out)
else:
    print("Not implemented")

