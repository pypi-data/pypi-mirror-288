import re
import nltk # type: ignore
import pandas as pd # type: ignore
from nltk.corpus import stopwords # type: ignore
#from nltk.stem import PorterStemmer # type: ignore
from nltk.stem import WordNetLemmatizer # type: ignore
from langdetect import detect # type: ignore
from text_preprocess_sanitizer.language_models import get_language_model

# Ensure the required stopwords are available
nltk.download('stopwords')
nltk.download('wordnet')

def sensitive_info_removal(text, nlp_model):
    """
    Remove sensitive information from the text, such as credit card numbers, phone numbers, and personal names.

    :param text: Text to sanitize
    :param nlp_model: spaCy language model
    :return: Sanitized text
    """
    # Patterns to identify and remove sensitive data
    credit_card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
    text = re.sub(credit_card_pattern, '', text)

    phone_pattern = r'\b(?:\+?\d{1,3})?[-.\s]?(?:\(?\d{1,4}\)?)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}\b'
    text = re.sub(phone_pattern, '', text)

    # Use spaCy NER to remove entities such as PERSON, ORG, and GPE
    doc = nlp_model(text)
    for entity in doc.ents:
        if entity.label_ in ['PERSON', 'ORG', 'GPE']:
            text = text.replace(entity.text, '')

    # Fallback regex pattern to remove capitalized words
    capitalized_word_pattern = r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b'
    text = re.sub(capitalized_word_pattern, '', text)

    return text

def text_sanitizer(text_series):
    """
    Clean and sanitize a series of text messages by removing sensitive information and unwanted elements.

    :param text_series: Pandas Series containing text data
    :return: Sanitized and processed Pandas Series
    """
    # Ensure all entries are strings
    text_series = text_series.astype(str)

    # Patterns for timestamps and dates
    date_patterns = [
        r'\d{4}-\d{1,2}-\d{1,2}\s*\d{1,2}:\d{2}(:\d{2})?',  # YYYY-MM-DD HH:MM[:SS]
        r'\d{1,2}/\d{1,2}/\d{4}\s*\d{1,2}:\d{2}(:\d{2})?',  # DD/MM/YYYY HH:MM[:SS]
        r'\d{1,2}\.\d{1,2}\.\d{4}\s*\d{1,2}:\d{2}(:\d{2})?',  # DD.MM.YYYY HH:MM[:SS]
        r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
        r'\d{1,2}/\d{1,2}/\d{4}',  # DD/MM/YYYY
        r'\d{1,2}\.\d{1,2}\.\d{4}',  # DD.MM.YYYY
        r'\d{1,2}-\d{1,2}-\d{4}',  # DD-MM-YYYY
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}',  # Month DD, YYYY
        r'\d{1,2}:\d{2}(:\d{2})?'  # HH:MM[:SS]
    ]

    # Remove timestamps and dates from text
    for pattern in date_patterns:
        text_series = text_series.str.replace(pattern, '', regex=True)

    # Define function to sanitize each text entry
    def process_text(text):
        """
        Detect language and sanitize text by removing sensitive information using NLP and regex.

        :param text: Single text entry
        :return: Sanitized text entry
        """
        try:
            language = detect(text)
            nlp_model = get_language_model(language)
            return sensitive_info_removal(text, nlp_model)
        except Exception as e:
            print(f"Error detecting language: {e}")
            return text

    # Apply sanitization to each text entry
    text_series = text_series.apply(process_text)

    # Patterns to clean URLs, emails, and other unwanted text
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    text_series = text_series.str.replace(url_pattern, '', regex=True)  # Remove URLs
    text_series = text_series.str.replace(r'\bwww\b|\bcom\b', '', regex=True)  # Remove common URL fragments
    text_series = text_series.str.replace(r'\S+@\S+', '', regex=True)  # Remove emails
    text_series = text_series.str.replace(r'\n', ' ', regex=True)  # Replace new lines with space
    text_series = text_series.str.replace(r'\b\w\b', '', regex=True)  # Remove single characters
    char_removal_pattern = r'[<>\+\@]|Ã¢â€”Â'
    text_series = text_series.str.replace(char_removal_pattern, '', regex=True)  # Remove unwanted characters
    text_series = text_series.str.replace(r'\s+', ' ', regex=True).str.strip()  # Normalize whitespace
    text_series = text_series.str.replace(r'(,\s*)+', ', ', regex=True)  # Normalize commas
    text_series = text_series.str.replace(r'\d+', '', regex=True)  # Remove digits
    text_series = text_series.str.replace(r'[^\w\s]|_|\*', " ", regex=True)  # Remove special characters
    text_series = text_series.str.lower()  # Convert to lowercase

    # Remove stopwords and apply stemming
    english_stopwords = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    """ stemmer = PorterStemmer()
    processed_series = text_series.apply(
        lambda x: ' '.join(
            stemmer.stem(term) for term in x.split() if term not in english_stopwords
        )
    ) """
    
    processed_series = text_series.apply(
    lambda x: ' '.join(
        lemmatizer.lemmatize(term) for term in x.split() if term not in english_stopwords
    ))

    return processed_series