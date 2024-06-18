#! /usr/bin/env python

import numpy as np
import pickle
from string import punctuation
from copy import deepcopy

class Training():
    def __init__(self, file_password, file_conf = None):
        """
        Parameters
        ----------------------
        file_password (txt): contains passwords for training, one per line.
        file_conf (txt): important symbols commonly used to define a password (es. #!£$).  
        """
        self.data, self.n_characters = self.load_data(file_password)    #data structure with passwords and number of characters per line 
        self.n_words = len(self.data)                                   #count words in the document
        if file_conf is not None:
            self.rules = self.load_data(file_conf)[0][0]
        else:
            self.rules = punctuation                                    #if no rules are specified, it takes string punctuation 
        self.keywords=["uppercase","number","mean_length","std_length"] #other factors to describe passwords 
        self.db ={}                                                     #database containing symbols count 
        for key in self.keywords:
            self.db[key] = 0

    def load_data(self, file_name):
        """
        Load password from file

        Parameters
        ----------------------
        file_name (str): file path

        Return
        ----------------------
        data (np array of str): array of passwords
        n_characters (np array of int): number of characters per line
        """
        data = []
        n_characters = []
        with open(file_name, "r", encoding='utf-8') as fin:
            for line in fin.readlines():
                elements = line.strip().split()
                for e in elements:
                    data.append(e)
                    n_characters.append(len(e))
        return np.array(data), np.array(n_characters)

    def assign_score(self):
        """
        Assign a score for each symbol, basing on the training set. Here it is possible to 
        discover policies used by different companies. For instance, about the length, the use 
        of a certain symbol or a certain number of digits/uppercases.
        For this reason it is important to specify a good training set. By default, it is used 
        a training set based on Microsoft policies (but without Unicode Asian characters)
        Ref: https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements 
        """
        n_characters_document = np.sum(self.n_characters)
        for word in self.data:
            for letter in word:
                try:
                    self.db[letter]+=1.0/n_characters_document
                except KeyError:
                    self.db[letter]=1.0/n_characters_document
                if(letter.isupper()):
                    self.db["uppercase"]+=1.0/n_characters_document
                if(letter.isdigit()):
                    self.db["number"]+=1.0/n_characters_document
        self.db["mean_length"] = 1.0*n_characters_document/self.n_words
        self.db["std_length"] = 1.0*np.std(self.n_characters)

    def print_score(self):
        """
        Print database of symbols
        """
        print(self.db)

    def filter_database(self):
        """
        From all the calculated symbols, it filters the database depending on the specified input rules 
        """
        temp = deepcopy(self.db)
        self.db = {}
        for key in temp.keys():
            if key in self.rules or key in self.keywords:
                self.db[key] = temp[key]
    
    def save(self, fout = "../input/rules.txt"):
        """
        Save rules on file

        Parameters
        ----------------------
        file_name (str): file path
        """
        with open(fout, "wb") as handle:
            pickle.dump(self.db, handle)

    def run(self, fout = "../input/rules.txt", verbose = True):
        """
        Run the algorithm

        Parameters
        ----------------------
        fout (str): file path in which the results are saved
        verbose (bool): indicates if the results are printed on screen
        """
        print("Start Training...")
        self.assign_score()
        self.filter_database()
        if verbose:
            self.print_score()
        print("Saving rules on file...")
        self.save(fout = fout)
        print("End")

if __name__ == "__main__":
    T = Training("../input/password.txt", "../input/conf.txt")
    T.run()
