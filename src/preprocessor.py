"""
Resume Text Preprocessing Module

Handles all text cleaning, normalization, and preprocessing operations.
Removes URLs, emails, special characters, and stopwords.
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class ResumePreprocessor:
    """
    Preprocesses resume text for NLP analysis.
    
    Handles:
    - Text cleaning (URLs, emails, special characters)
    - Stopword removal
    - Normalization (lowercase, whitespace)
    """

    def __init__(self):
        """Initialize preprocessor with stopwords."""
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords', quiet=True)
            nltk.download('punkt', quiet=True)
            self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        """
        Clean and normalize resume text.
        
        Operations:
        - Convert to lowercase
        - Remove URLs (http://, https://, www.)
        - Remove email addresses
        - Remove special characters and digits
        - Remove extra whitespace
        
        Args:
            text (str): Raw resume text
            
        Returns:
            str: Cleaned text
        """
        if not isinstance(text, str):
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)

        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)

        # Remove special characters and digits (keep letters and spaces)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)

        # Remove extra whitespace
        text = ' '.join(text.split())

        return text

    def remove_stopwords(self, text):
        """
        Remove common English stopwords from text.
        
        Also filters out words with length <= 2 characters.
        
        Args:
            text (str): Cleaned text
            
        Returns:
            str: Text without stopwords
        """
        try:
            tokens = word_tokenize(text)
        except LookupError:
            nltk.download('punkt_tab', quiet=True)
            tokens = word_tokenize(text)
            
        filtered_tokens = [
            word for word in tokens 
            if word not in self.stop_words and len(word) > 2
        ]
        return ' '.join(filtered_tokens)

    def preprocess(self, text):
        """
        Complete preprocessing pipeline.
        
        Applies cleaning and stopword removal in sequence.
        
        Args:
            text (str): Raw resume text
            
        Returns:
            str: Fully preprocessed text ready for NLP analysis
        """
        text = self.clean_text(text)
        text = self.remove_stopwords(text)
        return text
