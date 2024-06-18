#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0. , 10., 0.4)

plt.plot(x,x**2, 'g', x,x**3, 'b', x,x**4, 'r')
plt.savefig("tmp.png")