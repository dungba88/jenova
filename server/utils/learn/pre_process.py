"""Pre procesing utilities"""

import re

import nltk
from nltk import PorterStemmer

from utils.learn import persist

def parse_csv(reader, config, filtered_word_types):
    """parse the csv file"""
    input_texts = []
    output_texts = []

    for row in reader:
        text = row[0]
        if config.get('clean_text'):
            text = clean_text(row[0], filtered_word_types)
        input_texts.append(text)
        row.pop(0)
        output_texts.append(",".join(row))
    return input_texts, output_texts

def vectorize_target(outputs, data_name):
    """vectorize outputs"""
    vocab = persist.load_vocab_file(data_name)
    target_vocab = vocab.get('target_vocab')

    target_map = {v: k for k, v in enumerate(target_vocab)}

    return [target_map.get(output) for output in outputs], target_vocab

def clean_text(raw_text, filtered_word_types):
    """Clean raw text for bag-of-words model"""
    # Remove non-letters
    letters_only = re.sub("[^a-zA-Z]", " ", raw_text)

    # Convert to lower case, split into individual words
    words = letters_only.lower().split()

    # stem words
    stemmer = PorterStemmer()
    stemmed_words = list(map(stemmer.stem, words))

    # Remove stop words if requested
    if filtered_word_types is not None:
        tagged_text = nltk.pos_tag(stemmed_words)
        stemmed_words = [w for w, wtype in tagged_text if not wtype in filtered_word_types]

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
