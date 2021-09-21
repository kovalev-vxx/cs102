from math import log as ln
from collections import Counter
from string import punctuation, digits


def clear(doc):
    translator = str.maketrans("", "", punctuation)
    doc = doc.translate(translator)
    translator = str.maketrans("", "", digits)
    return doc.translate(translator)


def flatten(array):
    return [y for x in array for y in x]


def lower(array):
    return [i.lower() for i in array if i != ""]


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.fitted_words = {}
        self.pb_of_classes = {}

    def fit(self, X, y):
        counter_classes = Counter(y)
        for cl in counter_classes:
            self.pb_of_classes[cl] = counter_classes[cl] / len(y)

        docs_sorted_by_class = {}
        classes = list(set(y))
        for cl in classes:
            docs_sorted_by_class[cl] = []
            for doc, label in zip(X, y):
                if label == cl:
                    doc = lower((clear(doc)).split(" "))
                    docs_sorted_by_class[cl].append(doc)

        words_sorted_by_class = {}
        pb_of_words = {"words": []}
        counter_words = {}

        for cl in classes:
            words_sorted_by_class[cl] = []
            filt = docs_sorted_by_class[cl]
            for doc in filt:
                for word in doc:
                    words_sorted_by_class[cl].append(word)
                    if not word in pb_of_words["words"]:
                        pb_of_words["words"].append(word)

        d = len(pb_of_words["words"])

        for cl in words_sorted_by_class:
            counter_words[cl] = Counter(words_sorted_by_class[cl])

        for cl in words_sorted_by_class:
            pb_of_words[cl] = []
            for word in pb_of_words["words"]:
                if word in words_sorted_by_class[cl]:
                    pb = (counter_words[cl][word] + self.alpha) / (
                        len(words_sorted_by_class[cl]) + d * self.alpha
                    )
                    pb_of_words[cl].append(pb)
                else:
                    pb = (self.alpha) / (len(words_sorted_by_class[cl]) + d * self.alpha)
                    pb_of_words[cl].append(pb)

        self.fitted_words = pb_of_words
        return self.fitted_words

    def predict(self, X):
        predicted_docs = dict(docs=[], pred_class=[])

        for doc in X:
            predicted_class = {}
            for cl in self.pb_of_classes:
                predicted_class[cl] = []
                for word in lower((clear(doc)).split(" ")):
                    try:
                        index = self.fitted_words["words"].index(word)
                        predicted_class[cl].append(ln(self.fitted_words[cl][index]))
                    except ValueError:
                        predicted_class[cl].append(0)
                predicted_class[cl].append(ln(self.pb_of_classes[cl]))

            for cl in predicted_class:
                predicted_class[cl] = sum(predicted_class[cl])

            predicted_class = max(predicted_class, key=predicted_class.get)

            predicted_docs["docs"].append(doc)
            predicted_docs["pred_class"].append(predicted_class)

        return predicted_docs

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        predicted_classes = self.predict((X_test))["pred_class"]
        score = 0
        for predicted, real in zip(predicted_classes, y_test):
            if predicted == real:
                score += 1
        return score / len(y_test)
