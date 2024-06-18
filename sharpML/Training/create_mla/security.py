#!/usr/bin/env python

import numpy as np
from string import punctuation
from sklearn.metrics import classification_report

class Security():
    def __init__(self, file_training, file_testing):
        """
        questa volta il file training è un file contenente solo password
        """
        self.data_training, self.labels_training = self.load_data(file_training)
        self.data_testing, self.labels_testing = self.load_data(file_testing)
        self.likelihood = np.zeros(len(self.data_testing)) #likelihood of a word to be a password
        self.likelihood_norm = np.zeros(np.shape(self.likelihood))
        self.rules = {}
        self.predictions = None

    def load_data(self, file_name):
        data = []
        labels = []
        with open(file_name, 'r') as fin:
            for line in fin.readlines():
                data.append(line.strip('\n').split()[0])
                labels.append(line.strip('\n').split()[1])
        return np.array(data), np.array(labels).astype(int)
    
    def load_rules(self):
        for symbol in punctuation:
            self.rules[symbol] = 0.0
        self.rules['uppercase'] = 0.0
        self.rules['number'] = 0.0

    def training(self):
        """
        Assign a score for each symbol, basing on the training set
        """
        len_document = len(self.data_training)
        for word in self.data_training:
            for letter in word:
                try:
                    self.rules[letter]+=1.0/len_document
                except KeyError:
                    self.rules[letter]=1.0/len_document
                if(letter.isupper()):
                    self.rules["uppercase"]+=1.0/len_document
                if(letter.isdigit()):
                    self.rules["number"]+=1.0/len_document
    
    def testing(self, Z_value = 2.5):
        for i_word, word in enumerate(self.data_testing):
            for character in word:
                self.check_upper(i_word, character)
                self.check_digit(i_word, character)
                self.check_special(i_word, character)
        self.normalize_likelihood()
        self.predictions = 1*(self.likelihood_norm > Z_value)

    def check_upper(self, i_word, character):
        if character.isupper() :
            self.likelihood[i_word]+=self.rules["uppercase"] 
            #per esempio qui potrei assegnare un peso se ci sono maiuscole consecutive 
    
    def check_digit(self, i_word, character):
        if character.isdigit():
            self.likelihood[i_word]+=self.rules["number"]

    def check_special(self, i_word, character):
        if character in self.rules.keys():
            self.likelihood[i_word]+=self.rules[character]
    
    def normalize_likelihood(self):
        #np.seterr(divide = 'ignore', invalid = 'ignore') #only not to print on screen runtime warning of zero-divisions
        self.likelihood_norm = (self.likelihood - np.mean(self.likelihood)) / np.std(self.likelihood)
        #self.likelihood_norm = (self.likelihood - np.min(self.likelihood)) / (np.max(self.likelihood) - np.min(self.likelihood))
    
    def score(self):
        score = np.sum(1.0*(self.predictions == self.labels_testing))/len(self.labels_testing)
        wrong_data = self.data_testing[np.where(self.predictions!=self.labels_testing)[0]]
        predicted_passwords = self.data_testing[np.where(self.predictions==1)[0]]
        true_passwords = self.data_testing[np.where(self.labels_testing==1)[0]]
        print("Score: \n", classification_report(self.labels_testing, self.predictions))
        print("\nPredicted Passwords: ", predicted_passwords)
        print("\nTrue Passwords: ", true_passwords)
        if len(wrong_data):
            print("\nI was wrong with this words: ", wrong_data)

    def run(self):
        self.load_rules()
        self.training()
        self.testing()
        self.score()

if __name__=='__main__':
    S = Security("training.txt", "testing.txt")
    S.run()

