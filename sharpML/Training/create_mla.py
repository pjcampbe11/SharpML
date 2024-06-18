#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score

class Classifier():
    def __init__(self):
        """
        Constructor for Iris classification
        """
        self.data = datasets.load_iris().data
        self.labels = datasets.load_iris().target
        self.min = None
        self.std = None
        self.data_normalized = None
        self.data_training = None
        self.data_testing = None
        self.labels_training = None
        self.labels_testing = None
        self.model = None
        self.predictions = None
    def normalize_data(self):
        """
        Normalize data using Z norm
        """
        self.min = np.min(self.data)
        self.std = np.std(self.data)
        self.data_normalized = (self.data - self.min)/self.std
    def split_data(self, perc_training = 0.5):
        """
        Split data into training set and testing set

        Parameters
        ----------
        perc_training (float between 0 and 1): percentage of data used as training, default 0.5 (50%)
        """
        len_training = int(len(self.data_normalized)*perc_training)
        indexes_training = np.random.choice(len(self.data_normalized), size = len_training, replace = False)
        self.data_training = self.data_normalized[indexes_training]
        self.labels_training = self.labels[indexes_training]
        indexes_testing = np.delete(np.arange(len(self.data_normalized)), indexes_training)
        self.data_testing = self.data_normalized[indexes_testing]
        self.labels_testing = self.labels[indexes_testing]
    def model_selection(self):
        """
        KNN setup for classification
        """
        self.model = KNeighborsClassifier()
    def training(self):
        """
        Apply model to training dataset to learn the rules
        """
        self.model.fit(self.data_training, self.labels_training)
    def testing(self):
        """
        Test the rules on the new dataset
        """
        self.predictions = self.model.predict(self.data_testing)
    def score(self):
        """
        Compute and print the f-score 
        """
        print("F-Score: ", f1_score(self.labels_testing, self.predictions, average = 'micro'))
    def plot_data(self):
        """
        Plot data from dataset
        """
        f = plt.figure()
        ax = f.add_subplot(1,1,1)
        ax.set_title("PLOT DIM 1 VS DIM 2")
        ax.scatter(self.data_testing[:,0], self.data_testing[:,1], c = self.predictions, labels = self.predictions)
        ax.set_xlabel('Petal length')
        ax.set_ylabel('Petal width')
        ax.legend()
        f.savefig('scatter_plot.png')
    def run(self, perc_training = 0.5):
        """
        Run istances of Classifier

        Parameters
        ----------
        perc_training (float between 0 and 1): percentage of data used as training, default 0.5 (50%)
        """
        self.normalize_data()
        self.split_data(perc_training = perc_training)
        self.model_selection()
        self.training()
        self.testing()
        self.score()
        self.plot_data()
        

if __name__ == '__main__':
    C = Classifier()
    C.run(perc_training = 0.5)