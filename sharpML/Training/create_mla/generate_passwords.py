#!/usr/bin/env python

import numpy as np
import string

file_out = "testing_5.txt"
N = 5
rules = list(string.punctuation + string.ascii_letters*5 + string.digits) 
label = "1"

#training

with open(file_out, "w") as fout:
    for i in range(N):
        len_word = np.random.randint(6,20)
        word=""
        for j in range(len_word):
            word+=np.random.choice(rules)
            word_label = [word, label]            
        fout.write("{0}\t{1}\n".format(word, label))


