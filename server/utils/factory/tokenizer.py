"""factory for vectorizers"""

from tinysegmenter import TinySegmenter

class TokenizerFactory(object):
    """factory class for vectorizers"""

    @classmethod
    def get_tokenizer(cls, name):
        """get the vectorizer based on name"""
        factory = TokenizerFactory()
        factory_method = getattr(factory, 'get_' + name)
        if factory_method is None:
            raise ValueError('tokenizer ' + name + ' is not defined')
        return factory_method()

    def get_tiny_segmenter(self):
        """get japan vectorizer"""
        return TinySegmenter().tokenize

    def get_english_tokenizer(self):
        """get english vectorizer"""
        def tokenize(text):
            """tokenize by space"""
            return text.split(' ')
        return tokenize
