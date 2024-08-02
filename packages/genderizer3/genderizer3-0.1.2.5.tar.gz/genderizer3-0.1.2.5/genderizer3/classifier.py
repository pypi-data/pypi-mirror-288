from __future__ import division
import operator
from functools import reduce


class NotSeen(Exception):
    """
    Exception for tokens which are not indexed
    because never seen in the trainin data
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Token '{}' is never seen in the training set.".format(self.value)


class TrainedDataUtils:
    @staticmethod
    def getDocCount(data):
        """
        returns all documents count
        """
        return sum(data["docCountOfClasses"].values())

    @staticmethod
    def getClasses(data):
        """
        returns the names of the available classes as list
        """
        return data["docCountOfClasses"].keys()

    @staticmethod
    def getClassDocCount(data, className):
        """
        returns document count of the class.
        If class is not available, it returns None
        """
        return data["docCountOfClasses"].get(className, None)

    @staticmethod
    def getFrequency(data, token, className):
        try:
            foundToken = data["frequencies"][token]
        except KeyError:
            raise NotSeen(token)

        return foundToken.get(className, None)


class Classifier(object):
    """docstring for Classifier"""

    def __init__(self, trainedData, tokenizer):
        super(Classifier, self).__init__()
        self.data = trainedData
        self.tokenizer = tokenizer
        self.defaultProb = 0.000000001

    def classify(self, text):
        documentCount = TrainedDataUtils.getDocCount(self.data)
        classes = TrainedDataUtils.getClasses(self.data)
        tokens = self.tokenizer.tokenize(text)
        probsOfClasses = {}

        for className in classes:
            tokensProbs = [self.getTokenProb(token, className) for token in tokens]
            try:
                tokenSetProb = reduce(lambda a, b: a * b, (i for i in tokensProbs if i))
            except:
                tokenSetProb = 0

            probsOfClasses[className] = tokenSetProb / self.getPrior(className)

        return sorted(probsOfClasses.items(), key=operator.itemgetter(1), reverse=True)

    def getPrior(self, className):
        return TrainedDataUtils.getClassDocCount(
            self.data, className
        ) / TrainedDataUtils.getDocCount(self.data)

    def getTokenProb(self, token, className):
        classDocumentCount = TrainedDataUtils.getClassDocCount(self.data, className)

        try:
            tokenFrequency = TrainedDataUtils.getFrequency(self.data, token, className)
        except NotSeen as e:
            return None

        if tokenFrequency is None:
            return self.defaultProb

        probablity = tokenFrequency / classDocumentCount
        return probablity
