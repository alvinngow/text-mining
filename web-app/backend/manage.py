#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import nltk

def preprocess_text(text):
        stop_list = nltk.corpus.stopwords.words('english')
        stemmer = nltk.stem.porter.PorterStemmer()
        
        # Tokenize
        sent = nltk.word_tokenize(text)
        
        # We do not need this step below because the UICReviewData is already all in lowercase.
        sent = [w.lower() for w in sent]

        # Stop word removal. Optional!
    #     sent = [w for w in sent if w not in stop_list]

        # Stemming. Optional!
        sent = [stemmer.stem(w) for w in sent]
        
        
        
        return sent

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
