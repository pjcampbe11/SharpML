# SharpML

INSTRUCTIONS
This is the Machine Learning module used by SharpML software, 
and can be used to retrieve the following information:

1)Pairs user-password: 
The algorithm analyses the lines where the username is present, 
trying to find the associated password (from the username until the end of the line). 

2)Isolated passwords: 
The algorithm will try to extract isolated passwords analyzing the entire document. 

PRE-REQUISITES
To run this module you need python3 on your laptop.

PREPARATION
From the module directory, open a Ubuntu terminal and type:
pip install -r requirements.txt
This will install all the necessary dependencies. 

USAGE
Launch the file run.py by typing ./run.py on a Ubuntu terminal.
To specify input variables, open the file settings.txt

SETTINGS.TXT
It is loaded by the module run.py and contains the program input variables. 
Among all the specifications, be sure to provide the data you want to analyse (default: ./input/input.txt)

TRAINING
As a Machine Learning algorithm, it needs to be trained to recognize which words are passwords. 
We have provided a sample training file, which may be inadequate in some cases. 
Basing on the problem, especially in particular cases, be sure to provide a good training file. The more data
you provide, the more precise the algorithm will be when learning the rules. 

If you want to train the model with your personal dataset, open settings.txt and:
--> set the training variable to "True"
--> set the file_password as the name of your file

When you don't want to train the model anymore, set the training variable to "False"

OUTPUT
By default, the output will be displayed on screen and saved in ./output/output.txt.
You can specify another name in settings.txt

Password Hunting with ML (blog covers this repo)
REF: https://www.atlan.digital/lab/machine-learning-for-red-teams

Future State: 

Maldev Testing Env
https://www.atlan.digital/lab/maldev-testing-environment

Malware GAN & APT
https://www.atlan.digital/lab/malware-gan-and-atp-detailed-introduction

Malware GAN Part 2: Into EDR & MDR
https://www.atlan.digital/lab/malwaregan-part-2-deeper-into-killchain
