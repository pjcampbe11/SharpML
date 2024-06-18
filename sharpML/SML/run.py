#!/usr/bin/env python

from lib import training, testing
file_settings = "./settings.txt"

settings = []
with open(file_settings,"r") as fin:
    for line in fin.readlines():
        if len(line.split('"')) > 1:
            settings.append(line.strip().split('"')[1])

#REQUIREMENTS
#modify them in file "settings.txt"
#TRAINING
train = settings[0] 
if train == 'False': train = False
else: train = True                
file_password = settings[1]            
file_conf = settings[2]                
if file_conf == 'None':
    file_conf = None
#INTERMEDIATE OUTPUT
file_rules = settings[3]            
#TESTING
file_data = settings[4]                
file_users = settings[5]  
pass_mode = settings[6]              
file_common_passwords = settings[7]    
if file_common_passwords == 'None':
    file_common_passwords = None  
strong_pass = settings[8]
if strong_pass == 'False': strong_pass = False
else: strong_pass = True 
sensibility_line = float(settings[9])  
sensibility_global= float(settings[10]) 
deep_line = int(settings[11])
#OUTPUT
file_output = settings[12]    

#############################################################
####################    ALGORITHM   #########################
#############################################################

#TRAINING
if train:
    Tr = training.Training(file_password = file_password, file_conf = file_conf)
    Tr.run(fout = file_rules, verbose = False)

#TESTING
Te = testing.Testing(file_data=file_data, file_rules=file_rules, file_users=file_users, file_common_passwords=file_common_passwords)
Te.run(pass_mode = pass_mode, strong_pass = strong_pass, sensibility_line = sensibility_line, sensibility_global = sensibility_global, fout = file_output, deep_line = deep_line, verbose = True)

