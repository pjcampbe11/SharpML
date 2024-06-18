# SharpML

//Will keep private on personal GitHub until the code is fully understood. Goal would be to mv to CodeCommit. I think if we can get to a place where we can leverage custom AI models built to carry out various attacks, many of mics will be dropped \0/

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

Turul C2 Framework
https://turul.atlan.digital

// SharpML is based on the 'Machine Learning for Red Teams' course

Table of Contents

Chapter 1: Introduction

Overview of the proof of concept tool combining a custom Machine Learning algorithm and a C# wrapper.
Watch Introduction Video

Chapter 2: Python

Install Required Software
Setting a Workspace
Basic Program - Hello World
Scalar Types, Strings, Variables
Tuples, Lists, Sets, Dictionaries
Indentation, If Elif Else, For Loop, While Loop
Break Continue, Defining a Function, Methods, Structure
Using Instances, Arguments Passing, Mutable and Immutable
Standard Library, Numpy, Scipy, Matplotlib Pyplot, Pandas, I/O

Chapter 3: Machine Learning Theory and Designing an Algorithm

Basics - Theory
Workflow of an ML Algorithm - Theory
(K-mean) & Distances - Theory
Class Definition - Practical
Normalization - Practical
Outliers Removal - Practical
Split Data - Training & Test Data - Practical
Model Selection - Practical
Score - Practical
Plot Data - Practical
Why Not Neural Networks - Theory

Chapter 4: Building SharpML

SharpML Python Model Code
Organization of SharpML Code
Class Set Up, Load Data, Load Rules
Training, Testing, Results
Final Considerations, Init, Save Output, Run, Examples
C# Code Overview, Next Steps

Chapter 5: Build a CMS Web Analyzer

Intro, Further, Instructions
Develop a model to identify and classify web component technologies.
Translate the solution into features, scrape data, and compile a dataset.
Create a high-performance ML model and integrate into security tools.
Final project submission includes a comprehensive explanation and code.

Chapter 6: Build a Macaronic Obfuscator

Intro, Further, Instructions
Create a Python tool for obfuscating C# project files to evade ATP detection.
Set up an ATP E5 lab, interface with AMSI, generate wordlists.
Develop a static obfuscator pipeline and junk code generation function.
Final project submission includes detailed documentation and obfuscation code.

Chapter 7 (LLM BONUS): Build an LLM Infused SAST Tool

Intro, Further, Instructions, Final Words
Deploy a local LLM and integrate with a secure code regex tool.
Highlight vulnerable code using Control Flow Graph generators.
Integrate the workflow into a web app with an HTML dashboard.
Final project documentation and code tested against specified repositories.

Each chapter provides a structured overview of the topics and practical steps involved, designed to guide learners through the process of utilizing advanced technologies and methods effectively.

https://www.atlan.digital/train/machine-learning-for-red-teams


Other:
https://github.com/HunnicCyber/SharpML
https://www.atlan.digital/lab/red-team-information-gathering
https://github.com/HunnicCyber/SharpSniper
https://github.com/HunnicCyber/SharpDomainSpray
