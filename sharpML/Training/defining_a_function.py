#!/usr/bin/env python

def find_maximum(lst):
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





