from textblob.classifiers import NaiveBayesClassifier
import random
from nltk.corpus import movie_reviews

global train
import csv

class SentimentClassifier(object):
    def __init__(self, sender, training_data):
        self.train = []
        self.sender = sender
        self.training_path = training_data
        self.trainData()
        self.classificator = NaiveBayesClassifier(self.train)


    def trainData(self):
        with open(self.training_path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                self.train.append((row['text'].lower(), row['classification']))

    def classify(self, text):
        return self.classificator.classify(text)




if __name__ == '__main__':
    classifier = SentimentClassifier(None, "/home/alvaro/Documents/Universitat/TesisProject/Python/BaxterPythonServer/training.csv")
    print classifier.classify("A couple of months ago I went to China with my parents")
    print classifier.classify("Well, I have been in China and Italy is not a good memory")
    print classifier.classify("No, Actually I haven't")
    print classifier.classify("I have been in lessoto")
    print classifier.classify("I went to Paris")
    print classifier.classify("yes I actually travel a lot ")
