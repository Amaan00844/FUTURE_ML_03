"""
Unit Tests for Resume Preprocessor

Tests text cleaning, stopword removal, and preprocessing pipeline.
"""

import unittest
from src.preprocessor import ResumePreprocessor


class TestResumePreprocessor(unittest.TestCase):
    """Test cases for ResumePreprocessor class."""
    
    def setUp(self):
        """Initialize preprocessor for tests."""
        self.preprocessor = ResumePreprocessor()
    
    def test_clean_text_urls(self):
        """Test URL removal."""
        text = "Visit https://example.com and www.site.org for info"
        cleaned = self.preprocessor.clean_text(text)
        self.assertNotIn("https", cleaned)
        self.assertNotIn("www", cleaned)
    
    def test_clean_text_emails(self):
        """Test email removal."""
        text = "Contact me at john@example.com or jane.doe@company.org"
        cleaned = self.preprocessor.clean_text(text)
        self.assertNotIn("@", cleaned)
    
    def test_clean_text_special_chars(self):
        """Test special character removal."""
        text = "C++, C#, .NET, $100/hr, 50% complete!"
        cleaned = self.preprocessor.clean_text(text)
        # Should only have letters and spaces
        for char in cleaned:
            self.assertTrue(char.isalpha() or char.isspace())
    
    def test_clean_text_case(self):
        """Test lowercase conversion."""
        text = "PYTHON Java JavaScript"
        cleaned = self.preprocessor.clean_text(text)
        self.assertEqual(cleaned.lower(), cleaned)
    
    def test_clean_text_whitespace(self):
        """Test whitespace normalization."""
        text = "Extra    spaces    and\n\ttabs"
        cleaned = self.preprocessor.clean_text(text)
        self.assertNotIn("  ", cleaned)
        self.assertNotIn("\n", cleaned)
        self.assertNotIn("\t", cleaned)
    
    def test_remove_stopwords(self):
        """Test stopword removal."""
        text = "the quick brown fox jumps over the lazy dog"
        result = self.preprocessor.remove_stopwords(text)
        # Common stopwords should be removed
        self.assertNotIn("the", result)
        self.assertNotIn("over", result)
    
    def test_preprocess_complete(self):
        """Test complete preprocessing pipeline."""
        text = """
            Expert Python developer with 5+ years at https://company.com
            Email: john@example.com | Skills: C++, Django, SQL
            Experience: $50K-$100K, 85% positive reviews!
        """
        result = self.preprocessor.preprocess(text)
        
        # Should be lowercase
        self.assertEqual(result.lower(), result)
        # No URLs
        self.assertNotIn("https", result)
        # No emails
        self.assertNotIn("@", result)
        # No special chars
        self.assertNotIn("$", result)
        self.assertNotIn("!", result)
    
    def test_empty_input(self):
        """Test handling of empty/None input."""
        self.assertEqual(self.preprocessor.preprocess(""), "")
        self.assertEqual(self.preprocessor.preprocess(None), "")
        self.assertEqual(self.preprocessor.clean_text(None), "")


if __name__ == '__main__':
    unittest.main()
