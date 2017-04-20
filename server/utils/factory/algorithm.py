"""factory for algorithms"""

from sklearn.naive_bayes import GaussianNB

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
