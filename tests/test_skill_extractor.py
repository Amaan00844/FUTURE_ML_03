"""
Unit Tests for Skill Extractor

Tests skill extraction, categorization, and database functionality.
"""

import unittest
from src.skill_extractor import SkillExtractor


class TestSkillExtractor(unittest.TestCase):
    """Test cases for SkillExtractor class."""
    
    def setUp(self):
        """Initialize skill extractor for tests."""
        self.extractor = SkillExtractor()
    
    def test_extract_programming_skills(self):
        """Test extraction of programming skills."""
        text = "Expert in Python, Java, and JavaScript development"
        skills = self.extractor.extract_skills(text)
        self.assertIn('python', skills)
        self.assertIn('java', skills)
        self.assertIn('javascript', skills)
    
    def test_extract_web_skills(self):
        """Test extraction of web development skills."""
        text = "Proficient in React, Angular, and Node.js"
        skills = self.extractor.extract_skills(text)
        self.assertIn('react', skills)
        self.assertIn('angular', skills)
        self.assertIn('nodejs', skills)
    
    def test_extract_database_skills(self):
        """Test extraction of database skills."""
        text = "SQL, MongoDB, and PostgreSQL experience"
        skills = self.extractor.extract_skills(text)
        self.assertIn('sql', skills)
        self.assertIn('mongodb', skills)
        self.assertIn('postgresql', skills)
    
    def test_extract_ml_skills(self):
        """Test extraction of ML/AI skills."""
        text = "Machine learning with TensorFlow and PyTorch"
        skills = self.extractor.extract_skills(text)
        self.assertIn('machine learning', skills)
        self.assertIn('tensorflow', skills)
        self.assertIn('pytorch', skills)
    
    def test_extract_cloud_skills(self):
        """Test extraction of cloud skills."""
        text = "AWS and Azure cloud computing with Docker"
        skills = self.extractor.extract_skills(text)
        self.assertIn('aws', skills)
        self.assertIn('azure', skills)
        self.assertIn('docker', skills)
    
    def test_extract_soft_skills(self):
        """Test extraction of soft skills."""
        text = "Strong leadership and problem solving abilities"
        skills = self.extractor.extract_skills(text)
        self.assertIn('leadership', skills)
        self.assertIn('problem solving', skills)
    
    def test_case_insensitive(self):
        """Test case-insensitive skill matching."""
        text = "PYTHON JAVA JavaScript python java"
        skills = self.extractor.extract_skills(text)
        # Should have only one instance of each skill
        self.assertEqual(skills.count('python'), 1)
        self.assertEqual(skills.count('java'), 1)
    
    def test_word_boundary(self):
        """Test word boundary matching to avoid partial matches."""
        text = "pythonic development with python"
        skills = self.extractor.extract_skills(text)
        self.assertIn('python', skills)
        self.assertNotIn('pythonic', skills)
    
    def test_categorize_skills(self):
        """Test skill categorization."""
        skills = ['python', 'java', 'react', 'sql', 'aws']
        categorized = self.extractor.categorize_skills(skills)
        
        self.assertIn('python', categorized['programming'])
        self.assertIn('java', categorized['programming'])
        self.assertIn('react', categorized['web'])
        self.assertIn('sql', categorized['database'])
        self.assertIn('aws', categorized['cloud'])
    
    def test_get_skill_category(self):
        """Test getting category for specific skill."""
        self.assertEqual(self.extractor.get_skill_category('python'), 'programming')
        self.assertEqual(self.extractor.get_skill_category('react'), 'web')
        self.assertEqual(self.extractor.get_skill_category('aws'), 'cloud')
        self.assertIsNone(self.extractor.get_skill_category('unknownskill'))
    
    def test_empty_input(self):
        """Test handling of empty/None input."""
        self.assertEqual(self.extractor.extract_skills(""), [])
        self.assertEqual(self.extractor.extract_skills(None), [])
    
    def test_total_skills_count(self):
        """Test getting total skills count."""
        count = self.extractor.get_total_skills_count()
        self.assertGreater(count, 100)  # Should have 150+ skills
    
    def test_categories(self):
        """Test getting all categories."""
        categories = self.extractor.get_categories()
        self.assertGreater(len(categories), 10)  # Should have 14 categories
        self.assertIn('programming', categories)
        self.assertIn('web', categories)


if __name__ == '__main__':
    unittest.main()
