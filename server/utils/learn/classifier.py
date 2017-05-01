"""utility for classifying document"""

from utils.learn import persist

def predict(text, data_name):
    """predict the intent of a text"""
    vocab = persist.load_vocab_file(data_name)
    model = persist.load_model_file(data_name)
    vectorizer = persist.load_vectorizer(data_name)

    vectorized_text = vectorizer.transform([text]).toarray()

    ypred = model.predict(vectorized_text)[0]
    result_proba = 0

    if probabilistic_model(model):
        proba = model.predict_proba(vectorized_text)[0]
        result_proba = proba[ypred]

    result_word = vocab.get('target_vocab')[ypred]
    return result_word, result_proba

def probabilistic_model(model):
    """check if the model is a probablistic model"""
    return callable(getattr(model, 'predict_proba', None))

def predict_list(texts, data_name):
    """predict the intent of texts"""
    model = persist.load_model_file(data_name)
    vectorizer = persist.load_vectorizer(data_name)
    vectorized_texts = vectorizer.transform(texts).toarray()
    return model.predict(vectorized_texts)
