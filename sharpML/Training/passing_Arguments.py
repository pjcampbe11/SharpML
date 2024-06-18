#!/usr/bin/env python

L = [2,3,4,5,3,8,4,2]

def find_maximum(lst, a = 2):
    """
    Calculate the maximum of a list

    Parameters
    ----------
    lst (list of integers): list to calculate the maximum

    Return
    ------
    maximum (int): max value of the list
    """
    maximum = lst[0]
    for i in range(1,len(lst)):
        if(lst[i] > maximum):
            maximum = lst[i]
    return maximum

maximum = find_maximum(lst = L, a = 4)
print(maximum)




