from setuptools import setup, find_packages

setup(
    #name='text-preprocess-sanitizer',
    name='text_sanitization_suite',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'nltk',
        'spacy',
        'langdetect',
    ],
    description=(
    "Text Sanitization Suite is a robust Python package designed for personas who work in Data Science Domain i.e "
    "Data Scientists, Data Analysts, AI Engineers, Machine learning professionals to efficiently clean and prepare text data. "
    ),
    long_description=(
    "Text Sanitization Suite is a powerful Python package designed for data scientists and machine learning professionals to enhance data quality and model performance through comprehensive preprocessing. "
    "It supports multiple languages i.e English, French, German, Spanish, Italian. \n\n"
    "It is tailored for data preprocessing workflows, focusing on transforming raw text into "
    "structured data for analysis and modeling."
    "Ideal for tasks like Text Classification, Sentiment Analysis, Topic Modeling, and Named Entity Recognition. "
    "Also it efficiently removes sensitive PII Information (PII)."
    ),

    long_description_content_type='text/markdown',
    author='Gaurav Singh',
    author_email='gauravdsmailbox@gmail.com',
    url='https://github.com/gauravds1984/text_sanitizer_suite',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    python_requires='>=3.6',
)
