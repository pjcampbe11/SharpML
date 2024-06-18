#!/usr/bin/env python

import time
import sys
import numpy as np

n_elements = int(sys.argv[1])

start = time.time()
l = list(range(n_elements))
total_time_l = time.time() - start
print ("time list: ",total_time_l)

start = time.time()
a= np.arange(n_elements)
total_time_a = time.time() - start
print ("time numpy array: ",total_time_a)

print("efficiency: ", total_time_l/total_time_a)