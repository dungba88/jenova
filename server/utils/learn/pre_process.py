"""Pre procesing utilities"""

import re

from nltk import PorterStemmer
from nltk.corpus import stopwords

from utils.learn import persist

def vectorize_new_input(text, data_vocab):
    """vectorize new input based on vectorized data"""
    word_count = count_words(text)
    vectorized_text = []

    for word in data_vocab:
        if word in word_count:
            vectorized_text.append(word_count[word])
        else:
            vectorized_text.append(0)
    return vectorized_text

def predict(text, data_name):
    """predict the intent of a text"""
    vocab = persist.load_vocab_file(data_name)
    model = persist.load_model_file(data_name)

    vectorized_text = vectorize_new_input(text, vocab.get('data_vocab'))
    ypred = model.predict([vectorized_text])[0]
    proba = model.predict_proba([vectorized_text])[0]

    result_proba = proba[ypred]
    result_word = vocab.get('target_vocab')[ypred]
    return result_word, result_proba

def count_words(text):
    """count words in text"""
    word_count = {}
    for word in text:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1
    return word_count

def clean_text(raw_text, remove_stop_words):
    """Clean raw text for bag-of-words model"""
    # Remove non-letters
    letters_only = re.sub("[^a-zA-Z]", " ", raw_text)

    # Convert to lower case, split into individual words
    words = letters_only.lower().split()

    # stem words
    stemmer = PorterStemmer()
    stemmed_words = map(stemmer.stem, words)

    # Remove stop words if requested
    if remove_stop_words:
        stop_words = set(stopwords.words("english"))
        stemmed_words = [w for w in stemmed_words if not w in stop_words]

    # join together
    return " ".join(stemmed_words)

def vectorize(vectorizer, texts):
    """vectorize list of texts"""
    return vectorizer.fit_transform(texts).toarray()

def vectorize_data(input_texts, output_texts, vectorizer):
    """vectorize the data"""
    input_vectorized_texts = vectorize(vectorizer, input_texts)
    output_vectorized_texts = []
    output_vocab = []

    for text in output_texts:
        if text not in output_vocab:
            output_vocab.append(text)
            output_vectorized_texts.append(len(output_vocab) - 1)
        else:
            index = output_vocab.index(text)
            output_vectorized_texts.append(index)

    return {
        'data': input_vectorized_texts.tolist(),
        'target': output_vectorized_texts,
        'data_vocab': vectorizer.get_feature_names(),
        'target_vocab': output_vocab
    }
