
# Text Sanitizer Suite

Text Sanitizer Suite is a robust Python package designed for data scientists and machine learning professionals to efficiently clean and sanitize text data by removing sensitive PII information along with make it processed to further consumable by various NLP based use cases. 

## Key Points
- Text sanitization/preprocessing is essential for converting raw text into structured data for analysis and modeling. This includes tasks like tokenization, stopword removal, lemmatization, and sanitizing sensitive information to improve data quality and model performance.
- Applicable Use Cases: Text Classification/Sentiment Analysis/Topic Modeling/Named Entity Recognition
- Scope and Audience: This package is tailored for data science professionals engaged in data preprocessing workflows. It focuses on preparing text for analysis and modeling rather than serving end-users aiming to remove personally identifiable information (PII) solely for privacy reasons. Future versions will address broader use cases, including end-user needs for PII and sensitive data cleaning.


## Features

- Multi-language Support:Processes text in English, German, French, Spanish, Portuguese, Dutch and Italian ensuring comprehensive language coverage for data sanitization.
- Sensitive Data Removal:Effectively removes personal names, credit card numbers, and phone numbers using advanced patterns and natural language processing.

## Installation

To install the package, clone the repository and run:

```bash
pip install -e .
```

This command installs the package in editable mode, allowing you to make changes and have them reflected immediately.

## Requirements

Ensure you have the following Python packages installed:

- `pandas`
- `nltk`
- `spacy`
- `langdetect`

These dependencies are specified in the `requirements.txt` file. Install them using:

```bash
pip install -r requirements.txt
```

## Usage

Here's how to use the `text_sanitizer` function to sanitize text data:

```python
import pandas as pd
from text_preprocess_sanitizer.preprocess import text_sanitizer

# Sample data
data = pd.Series([
    "ITSM Ticket ID: TKT-0001 - User: John Doe reported a system outage. Contact: 987-654-3210.",
    "Ticket: TKT-0002 - Jane Smith's phone 1234-5678-9123-4567 is unresponsive. Visit www.example.com for more info."
])

# Process the data
processed_data = text_sanitizer(data)

# Print processed data
for i, text in enumerate(processed_data, start=1):
    print(f"Entry {i}: {text}")
```

## Running Tests

Unit tests are included to ensure the functionality of the package. To run the tests, execute:

```bash
python -m unittest discover tests
```

This command runs all tests in the `tests` directory and outputs the results, helping you verify that the package works correctly.

## Contributing

We welcome contributions from the community! To contribute, please fork the repository, create a new branch, and submit a pull request. Ensure your code adheres to the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or suggestions, please contact [Gaurav Singh](mailto:gauravdsmailbox@gmail.com) , [Amit Kumar](mailto:credamit@gmail.com).

## Acknowledgements

- [spaCy](https://spacy.io/) for providing robust NLP models.
- [NLTK](https://www.nltk.org/) for natural language processing tools.
- [Pandas](https://pandas.pydata.org/) for data manipulation.
- [Langdetect](https://pypi.org/project/langdetect/) for language detection capabilities.

