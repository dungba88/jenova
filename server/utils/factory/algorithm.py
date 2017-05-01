"""factory for algorithms"""

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

class AlgorithmFactory(object):
    """factory class for algorithms"""

    @classmethod
    def get_algorithm(cls, name):
        """get the algorithm based on name"""
        factory = AlgorithmFactory()
        factory_method = getattr(factory, 'get_' + name)
        if factory_method is None:
            raise ValueError('algorithm ' + name + ' is not defined')
        return factory_method()

    def get_naive_bayes(self):
        """get naive bayes algorithm"""
        return GaussianNB()

    def get_naive_bayes_mm(self):
        """get naive bayes algorithm"""
        return MultinomialNB()

    def get_logistic(self):
        """get logistic regression algorithm"""
        return LogisticRegression(solver='lbfgs', multi_class='multinomial')

    def get_svm(self):
        """get support vector machine algorithm"""
        return SGDClassifier(loss='log', penalty='l2',
                             alpha=1e-3, n_iter=5, random_state=42)
