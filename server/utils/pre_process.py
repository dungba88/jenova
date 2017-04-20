"""Pre procesing utilities"""

import re

from nltk import PorterStemmer
from nltk.corpus import stopwords

def vectorize_new_input(text, data_vocab):
    """vectorize new input based on vectorized data"""
    text = clean_text(text)
    word_count = count_words(text)
    vectorized_text = []

    for word in data_vocab:
        if word in word_count:
            vectorized_text.append(word_count[word])
        else:
            vectorized_text.append(0)
    return vectorized_text

def count_words(text):
    """count words in text"""
    word_count = {}
    for word in text.split(' '):
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1
    return word_count

def clean_text(raw_text):
    """Clean raw text for bag-of-words model"""
    # Remove non-letters
    letters_only = re.sub("[^a-zA-Z]", " ", raw_text)

    # Convert to lower case, split into individual words
    words = letters_only.lower().split()

    # Get the stopwords
    stop_words = set(stopwords.words("english"))

    # Remove stop words
    meaningful_words = [w for w in words if not w in stop_words]

    # stem words
    stemmer = PorterStemmer()
    stemmed_words = map(stemmer.stem, meaningful_words)

    # join together
    return " ".join(stemmed_words)

def vectorize(vectorizer, texts):
    """vectorize list of texts"""
    return vectorizer.fit_transform(texts).toarray()

def parse_csv(reader):
    """parse the csv file"""
    input_texts = []
    output_texts = []
    for row in reader:
        input_texts.append(clean_text(row[0]))
        row.pop(0)
        output_texts.append(",".join(row))
    return input_texts, output_texts

def vectorize_data(reader, vectorizer):
    """vectorize the data"""
    input_texts, output_texts = parse_csv(reader)
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
