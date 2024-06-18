#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score

class Classifier():
    def __init__(self):
        """
        qui dovrei specificare almeno data = qualcosa, labels = qualcosa
        per costruire una roba utile
        """
        self.data = datasets.load_iris().data
        self.labels = datasets.load_iris().target
        self.data_training = None #always specify here class variables with description
        self.labels_training = None
        self.data_testing = None #portion of data for testing
        self.labels_testing = None
        self.model = None #it will contain the model i use to classify
        self.data_normalized = None
        self.min = None
        self.std = None #li salvo perché se poi voglio fare la funzione che mi riporta indietro i dati e ho rimosso outliers, questi mi servono
        self.outliers = None #contains outliers
        self.predictions = None #will contain predictions. potresti anche dichiararla come variabile lista vuota per far capire il tipo

    def normalize_data(self, mode = 'mean-std'):
        """
        note that in iris dataset all features are expressed in cm. 
        but what would happen if there are cm, kg, light intensity?
        suppose we have no idea of the data composition. 
        si salva anche min e std perché posso voler fare la funzione inversa dove dai
        dati normalizzati mi riporta a quelli raw
        """
        self.min = np.min(self.data)
        self.std = np.std(self.data)
        self.data_normalized = (self.data - self.min)/self.std
        #is it the best normalization? it depends. we need to know something about the data, we could do
        #some gaussian test, which tells us if data are normal distributed. 
        #here there is a lot about statistics, i do not want to give mathematicla details here in this course
        #but think about that: do you want to (esempio del bisteccone MT)
        
    def outliers_removal(self, n_stds = 3):
        """
        n of standard deviations
        to remove outliers, after a Z normalization we consider 'bad' all data with values over 3
        in this case there are no outliers because the set is well built for the example 
        """
        indexes_outliers = np.where(self.data_normalized > n_stds)[0]
        indexes_data_normalized = np.delete(np.arange(len(self.data_normalized)), indexes_outliers) 
        self.outliers = self.data[indexes_outliers]
        self.outliers_labels = self.labels[indexes_outliers]
        self.data_normalized = self.data_normalized[indexes_data_normalized]
        self.data = self.data[indexes_data_normalized]
        self.labels = self.labels[indexes_data_normalized]
        print("Removed ", len(indexes_outliers) ,"outliers")

    def split_data(self, perc_training = 0.5):
        """
        perc_training: percentage of data used as training, default 50%
        """
        len_training = int(len(self.data_normalized)*perc_training) #how many data

        indexes_training = np.random.choice(len(self.data_normalized), size = len_training)
        self.data_training = self.data_normalized[indexes_training]
        self.labels_training = self.labels[indexes_training]

        indexes_testing = np.delete(np.arange(len(self.data_normalized)), indexes_training)
        self.data_testing = self.data_normalized[indexes_testing]
        self.labels_testing = self.labels[indexes_testing]

    def model_selection(self):
        """
        ognuno usica logiche diverse, richiede input diversi e funziona bene su certi tipi di dati e quantità di dati
        per raccogliere quante più informazioni possibili dovete leggervi articoli scientifici
        o almeno la documentazione di sklearn (python)
        altrimenti rischiate di applicare un algoritmo ed ottenere risultati poco precisi
        inoltre cosa succede quando avete 1 milione di dati? Se un algoritmo è preciso ma ha una complessità alta rischiate di non uscirne
        """
        #C = KNeighborsClassifier(n_neighbors=5, weights=’uniform’, algorithm=’auto’, leaf_size=30, p=2, metric=’minkowski’, metric_params=None, n_jobs=None)
        self.model = KNeighborsClassifier()

    def training(self):
        self.model.fit(self.data_training, self.labels_training)

    def testing(self):
        self.predictions = self.model.predict(self.data_testing)

    def score(self):
        print("Score: ", accuracy_score(self.labels_testing, self.predictions))
        print("F1 - Score: ", f1_score(self.labels_testing, self.predictions, average = 'micro'))

    def plot(self):
        """
        plot data in blue and outliers in red
        """
        f = plt.figure()
        ax = f.add_subplot(1,1,1)
        ax.set_title("THIS IS ONLY DIMENSION 1 vs DIMENSION 2")
        ax.scatter(self.data_testing[:,0], self.data_testing[:,1], c = self.predictions)
        ax.set_xlabel('Petal length')
        ax.set_ylabel('Petal width')
        f.savefig('scatter_plot.png')

    def run(self, n_stds = 3, perc_training = 0.5):
        """
        puoi anche usare __call__
        """
        self.normalize_data() #nell'esercitazione inserire queste funzioni una per volta e stampare il risultato
        #self.outliers_removal(n_stds = n_stds)
        self.split_data(perc_training = perc_training)
        self.model_selection()
        self.training()
        self.testing()
        self.score()
        self.plot()


if __name__=="__main__":
    C = Classifier()
    C.run()
