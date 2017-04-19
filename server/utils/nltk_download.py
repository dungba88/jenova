"""Script for downloading NLTK data"""

import ssl
import nltk

def download():
    """skip unverified certificate and show download dialog"""
    try:
        create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = create_unverified_https_context

    nltk.download()

download()
