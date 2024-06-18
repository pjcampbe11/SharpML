import math
import numpy as np
import pandas as pd
import pickle

class Testing():
    def __init__(self, file_data, file_rules, file_users = None, file_common_passwords = None):
        """ 
        Parameters
        ----------------------
        file_data (str): file to analyze
        file_rules (str): file output of Rules.py
        file_users (str): file containing users list
        file_common_passwords (str): file containing common passwords
        """
        self.data = []                  #array of words containing all data 
        self.data_line = []             #contains data line by line 
        self.user_line = []             #contains [index line ,user line, data line] 
        self.likelihood = None          #data likelihood to be a password
        self.likelihood_norm = None     #normalized likelihood
        self.user_pass = {}             #contains user: pass of pairs (user, pass) inside the document
        self.pass_score = {}            #contains pass: score of single passwords inside the document
        self.load_rules(file_rules)
        if file_users is not None:
            self.users = self.load_line(file_users) #contains all users 
        else:
            self.users = None 
        if file_common_passwords is not None:
            self.common_passwords = self.load_line(file_common_passwords)   #contains known common passwords
        else:
            self.common_passwords = None
        self.load_data(file_data)       
        self.length_min = math.floor(self.db["mean_length"]-self.db["std_length"])  #min length for passwords
        self.length_max = math.ceil(self.db["mean_length"]+self.db["std_length"])   #max length for passwords   
    
    """
    LOAD
    """
    
    def load_rules(self, file_name):
        """
        Load rules (output of training.py) from file.

        Parameters
        ----------------------
        file_name (str): file path 
        """
        with open(file_name, "rb") as handle:
            self.db = pickle.load(handle)

    def load_line(self, file_name):
        """
        Load data line by line.

        Parameters
        ----------------------
        file_name (str): file path
        
        Return 
        ----------------------
        data (np.array): each element is a line
        """
        data = []
        with open(file_name, "r", encoding='utf-8') as fin:
            for line in fin.readlines():
                data.append(line.strip())
        return np.array(data)

    def load_data(self, file_name):
        """
        Load data document to analyze

        Parameters
        ----------------------
        file_name (str): file path
        """
        with open(file_name, "r", encoding='utf-8') as fin:
            for i_line, line in enumerate(fin.readlines()): 
                if self.users is not None:
                    for user in self.users:
                        if user in line:
                            self.user_line.append([i_line, user, line.strip().split()]) 
                self.data_line.append(line.strip().split())  
                elements = line.strip().split()
                for e in elements:
                    self.data.append(e)

    """
    CREATE OUTPUT STRUCTURES
    """

    def create_user_pass(self, strong_pass = False, sensibility = 0.25, deep_line = 1): 
        """
        Create the user: pass dictionary seeking password in given lines

        Parameters
        ----------------------
        strong_pass (bool): if yes, suppose that a password has at least a lowercase, an uppercase, a symbol and a number
        sensibility (float): threshold over which a word is considered to be a password. 
            From literature, when you normalize enough data from a gaussian distribution with mean-std, 
                values above 3.0 are considered outliers (or password in this case). In our case, 
                even if distrib is not gaussian, it works well with default value 2.5.
            If you normalize a few elements max-min (like in line research), set this to the first quartile (0.25)
        deep_line (int): if password is not found on the user line, it will check deep_line additional lines
        """
        for i_line, line in enumerate(self.user_line):
            i_user = line[2].index(self.user_line[i_line][1])
            try:
                password = self.find_common_passwords(line[2][i_user+1:])
                i_deep_line = 1 
                if(password is None):
                    i_password, password = self.find_passwords(line[2][i_user+1:], strong_pass, 'line', sensibility)
                while(len(password) == 0 and i_deep_line < deep_line+1):
                    if(len(self.data_line[line[0] + i_deep_line])>0):
                        i_password, password = self.find_passwords(self.data_line[line[0] + i_deep_line], strong_pass, 'line', sensibility)
                    i_deep_line+=1
            except IndexError:
                password = [] 
            if len(password) == 0:
                password = ["(NOT FOUND)"] + line[2][i_user+1:]
            self.user_pass[line[1]] = password

    def create_pass_score(self, i_candidates):
        """
        Create pass: score dictionary for all the candidates passwords found in the document

        Parameters
        ----------------------
        i_candidates (np array of int): indexes of all candidates
        """
        for i_candidate in i_candidates:
            self.pass_score[self.data[i_candidate]] = self.likelihood_norm[i_candidate]

    """
    FIND PASSWORDS
    """

    def find_common_passwords(self, line):
        """
        Check if word belongs to a common list of passwords

        Parameters
        ----------------------
        line (np array of str): line to examine

        Return
        ----------------------
        None if password is not in common_passwords
        password (str) otherwise
        """
        if self.common_passwords is not None:
            for word in line:
                if word in self.common_passwords:
                    return word
        return None

    def find_passwords(self, line, strong_pass = True, mode = 'line', sensibility = 0.25):
        """
        Find user and password in a given line

        Parameters
        ----------------------
        strong_pass (bool): if yes, suppose that a password has at least a lowercase, an uppercase, a symbol and a number
        mode ('line', 'global'): research mode
            line: research passwords in the same line as a given username
            global: research passwords in the entire document
        sensibility (float): threshold over which a word is considered to be a password.
            From literature, when you normalize enough data with mean-std, values above 2.5 are considered outliers (or password in this case)
            If you normalize a few elements max-min (like in line research), set this to the first quartile (0.25)
        Return
        ------
        i_pass (int): index password in line
        pass (str): password
        """
        self.likelihood = np.zeros(np.shape(line))
        for i_word, word in enumerate(line):
            #consecutive numbers or uppercases does not increase the likelihood of the word to be a password 
            self.consecutive_numbers = False 
            self.consecutive_uppercase = False 
            #to be a password, it must have at least one of the following
            self.count_lower = False
            self.count_upper = False
            self.count_digit = False
            self.count_special = False
            if self.check_length(word) and not self.check_website(word):
                for i_character, character in enumerate(word):
                    self.check_lower(character)
                    self.check_upper(i_word, character)
                    self.check_digit(i_word, character)
                    self.check_special(i_word, character)
                if(strong_pass):
                    self.check_validation(i_word)
        if mode == 'line':
            if len(line) == 1:
                #need to compare the unique word with other words
                self.likelihood = np.append(self.likelihood,0)
                self.likelihood = np.append(self.likelihood,0)
                self.likelihood = np.append(self.likelihood,0)
            self.normalize_likelihood("max-min") 
            i_pass = np.where(self.likelihood_norm > sensibility)[0]   
        elif mode == 'global':
            self.normalize_likelihood("mean-std") 
            i_pass = np.where(self.likelihood_norm > sensibility)[0]  
        if len(i_pass)==1:
            return i_pass, np.array(line)[i_pass][0]
        else:
            i_pass_sorted = np.argsort(self.likelihood_norm[i_pass])[::-1]
            i_pass = i_pass[i_pass_sorted]
            return i_pass, np.array(line)[i_pass] 
        
    """
    CONTROLS
    """

    def check_length(self, word):
        """
        Check length inside valid range

        Parameters
        ----------------------
        word (str)

        Return
        ----------------------
        True if the word is in a valid length range
        False otherwise
        """
        if (len(word)>self.length_min and len(word)<self.length_max):
            return True
        return False

    def check_website(self, word):
        """
        Check if word is a website 

        Parameters
        ----------------------
        word (str)

        Return
        ----------------------
        True if the word is a website
        False otherwise
        """
        if "https://" in word or "http://" in word or "www." in word:
            return True
        return False

    def check_lower(self, character):
        """
        Check if character is lowercase

        Parameters
        ----------------------
        character (char): character
        """
        if character.islower():
            self.count_lower = True

    def check_upper(self, i_word, character):
        """
        Check if character is uppercase, if there are consecutive uppercases
        and set the likelihood accordingly to the results

        Parameters
        ----------------------
        i_word (int): index of the word in the numpy array being analyzed
        character (char): character
        """
        if character.isupper() :
            self.likelihood[i_word]+=(1-self.consecutive_uppercase) * self.db["uppercase"]
            self.consecutive_uppercase = True
            self.count_upper = True 
        else:
            self.consecutive_uppercase = False

    def check_digit(self, i_word, character):
        """
        Check if character is a digit, if there are consecutive digits
        and set the likelihood accordingly to the results
        
        Parameters
        ----------------------
        i_word (int): index of the word in the numpy array being analyzed
        character (char): character
        """
        if character.isdigit():
            self.likelihood[i_word]+=(1 - self.consecutive_numbers) * self.db["number"]
            self.consecutive_numbers = True
            self.count_digit = True
        elif character == '.' or character == '-':
            pass
        else:
            consecutive_numbers = False

    def check_special(self, i_word, character):
        """
        Check if character is a special character
        and set the likelihood accordingly to the results

        Parameters
        ----------------------
        i_word (int): index of the word in the numpy array being analyzed
        character (char): character
        """
        if character in self.db.keys():
            self.likelihood[i_word]+=self.db[character]
            self.count_special = True

    def check_validation(self, i_word):
        """
        Check if a word is a strong password (contains at least
        1 lowercase, 1 uppercase, 1 digit and 1 special character)

        Parameters
        ----------------------
        i_word (int): index of the word in the numpy array being analyzed
        """
        if not self.count_lower*self.count_upper*self.count_special*self.count_digit:
            self.likelihood[i_word] = 0

    """
    NORMALIZATION
    """

    def normalize_likelihood(self, mode = 'mean-std'):
        """
        Normalize likelihood to be able to determine and print outliers (passwords)

        Parameters
        ----------------------
        mode ('max-min' or 'mean-std'): normalization choices
            Use max-min if you have only few results because in this way it is possible to well see differences between scores
            Use mean-std if you have lots of results because outliers have a big score
        """
        np.seterr(divide = 'ignore', invalid = 'ignore') #only not to print on screen runtime warning of zero-divisions
        if mode == 'max-min':
            self.likelihood_norm = (self.likelihood - np.min(self.likelihood))/ (np.max(self.likelihood) - np.min(self.likelihood))
        elif mode == 'mean-std':
            self.likelihood_norm = (self.likelihood - np.mean(self.likelihood)) / np.std(self.likelihood)
        else:
            print("This normalization does not exist or it is not implemented here")
            self.likelihood_norm = self.likelihood

    """
    SAVE RESULTS
    """

    def save_data(self, pass_mode, file_name):
        """
        Save results on file

        Parameters
        ----------------------
        pass_mode (str): 'user' for pairs user-pass, 'global' for isolated passwords and 'all' for both 
        file_name (str): file path
        """
        with open(file_name, "w") as fout:
            if pass_mode == 'all' or pass_mode == 'user':
                fout.write("USER-PASS dictionary\n")
                fout.write("Each user is associated at one or more words\nIf it is a single word, it is the calculated password\n")
                fout.write("If it is a list, it means that more than one word might be a password. They are displayed in likelihood order\n")
                fout.write("If it is a list with (NOT FOUND) keyword, no words are recognized to be passwords and the entire line -after user word- is displayed\n\n")
                for key, value in self.user_pass.items():
                    fout.write(str(key) + ': ' + str(value)+'\n')
            if pass_mode == 'all' or pass_mode == 'global':
                fout.write("\n\nPASS-SCORE dictionary\n")
                fout.write("Each password is followed by its normalized likelihood score\n\n")
                for key, value in self.pass_score.items():
                    fout.write(str(key) + ': ' + str(value)+'\n')


    """
    PRINT RESULTS
    """

    def print_user_pass(self):
        """
        Print user: pass dictionary
        """
        for key, value in self.user_pass.items():
            print(key, ":", value)

    def print_pass_score(self):
        """
        Print pass: score dictionary
        """
        for candidate in self.pass_score.keys():
            print("(Score: ", "{:.2f}".format(self.pass_score[candidate]) , ") ",candidate)

    """
    RUN ALGORITHM
    """

    def run(self, pass_mode = 'all', strong_pass = False, sensibility_line = 0.25, sensibility_global = 2.5, fout = "../output/output.txt", deep_line = 0, verbose = True):
        """
        Run the algorithm

        Parameters
        ----------------------
        pass_mode (str): 'user' to find only pairs user-pass, 'global' to find isolated passwords and 'all' for both  
        strong_pass (bool): if you want to find strong passwords (at least 1 lowercase, 1 uppercase, 1 digit and 1 special character), set this to True
        sensibility_line (float, default 0.25): words over this threshold of max-min normalized likelihood are considered passwords
        sensibility_gloabl (float, default 2.5): by literature, outliers (in our case, passwords) are above Z-value=2.5 when mean-std norm
        fout (str): file path in which the results are saved
        deep_line(int): if password is not found on the user line, it will check deep_line additional lines. it makes sense if strong_pass is set to True,
                        because if not, the algorithm will find the most probable password in the line
        verbose (bool): indicates if the results are printed on screen
        """
        if pass_mode != 'all' and pass_mode != 'user' and pass_mode != 'global':
            print("ERROR pass_mode: mode not implemented")
            exit()
        print("\nLength password from", self.length_min,"to", self.length_max)
        if pass_mode == 'all' or pass_mode == 'user':
            if self.users is None:
                print("ERROR: missing users list")
                exit()
            print("\nCreating user-pass dictionary...")
            self.create_user_pass(strong_pass = strong_pass, sensibility = sensibility_line, deep_line = deep_line)
            if verbose:
                self.print_user_pass()
        if pass_mode == 'all' or pass_mode == 'global':
            print("\nCreating pass-score dictionary...")
            i_candidates, candidates = self.find_passwords(line = self.data, strong_pass = strong_pass, mode = 'global', sensibility = sensibility_global)
            self.create_pass_score(i_candidates) 
            if verbose:
                self.print_pass_score()
        print("Saving dictionaries on file...")
        self.save_data(pass_mode = pass_mode, file_name = fout)
        print("End")


