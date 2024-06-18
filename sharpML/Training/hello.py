#!/usr/bin/env python

"""
I have a farm, named “PrettyFarm”.
In this farm there are 15 horses and 3 cows.
Each horse has a value of 8 and each cow a value of 3.

Print the value of the farm.
"""

farm_name = "PrettyFarm"
n_horses = 15
n_cows = 3
value_horse = 8
value_cow = 3

farm_value = n_horses * value_horse + n_cows*value_cow

print("The value of the farm", farm_name, "is", farm_value)
