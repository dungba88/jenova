"""factory for vectorizers"""

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
        from tinysegmenter import TinySegmenter
        return TinySegmenter().tokenize

    def get_english_tokenizer(self):
        """get english vectorizer"""
        return tokenize_spaces

def tokenize_spaces(text):
    """tokenize by space"""
    return text.split(' ')
