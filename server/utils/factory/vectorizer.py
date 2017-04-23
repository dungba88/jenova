"""factory for vectorizers"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

class VectorizerFactory(object):
    """factory class for vectorizers"""

    @classmethod
    def get_vectorizer(cls, name, tokenizer):
        """get the vectorizer based on name"""
        factory = VectorizerFactory()
        factory_method = getattr(factory, 'get_' + name)
        if factory_method is None:
            raise ValueError('vectorizer ' + name + ' is not defined')
        return factory_method(tokenizer)

    def get_bag_of_word(self, tokenizer):
        """get bag of word vectorizer"""
        return CountVectorizer(analyzer="word",
                               tokenizer=tokenizer,
                               preprocessor=None,
                               stop_words=None,
                               max_features=5000)

    def get_tf_idf(self, tokenizer):
        """get tf-idf vectorizer"""
        return TfidfVectorizer(analyzer="word",
                               tokenizer=tokenizer,
                               preprocessor=None,
                               stop_words=None,
                               max_features=5000)
