import spacy

# Load spaCy language models for English and major European languages
nlp_en = spacy.load('en_core_web_md')  # English model
nlp_de = spacy.load('de_core_news_md')  # German model
nlp_fr = spacy.load('fr_core_news_md')  # French model
nlp_es = spacy.load('es_core_news_md')  # Spanish model
nlp_it = spacy.load('it_core_news_md')  # Italian model
nlp_pt = spacy.load('pt_core_news_md')  # Portuguese model
nlp_nl = spacy.load('nl_core_news_md')  # Dutch model

def get_language_model(lang):
    """
    Retrieve the appropriate spaCy language model based on the language code.
    Default to the English model if the language is unsupported.
    
    :param lang: Language code (e.g., 'en' for English)
    :return: spaCy language model
    """
    nlp_models = {
        'en': nlp_en,
        'de': nlp_de,
        'fr': nlp_fr,
        'es': nlp_es,
        'it': nlp_it,
        'pt': nlp_pt,  
        'nl': nlp_nl  
    }
    
    # Return the appropriate model, defaulting to English if unsupported
    return nlp_models.get(lang, nlp_models['en'])
