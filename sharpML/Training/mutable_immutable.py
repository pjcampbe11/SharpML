#!/usr/bin/env python

L = [2,3,4,5,3,8,4,2]
number = 2

def find_maximum(l, a):
    """
    Calculate the maximum of a list

    Parameters
    ----------
    lst (list of integers): list to calculate the maximum

    Return
    ------
    maximum (int): max value of the list
    """
    lst = l.copy()
    a = 10
    lst[0]=-1
    print(lst)
    maximum = lst[0]
    for i in range(1,len(lst)):
        if(lst[i] > maximum):
            maximum = lst[i]
    return maximum

print("L before function: ", L)
print("number before function: ", number)
maximum = find_maximum(L, number)
print("number after function: ", number)
print("L after function: ", L)




