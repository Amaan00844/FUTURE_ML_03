"""
Skill Extraction Module

Extracts technical and professional skills from resume text.
Uses predefined comprehensive skill database with 150+ skills.
"""

import re


class SkillExtractor:
    """
    Extracts and categorizes skills from resume text.
    
    Supports 150+ skills across 14 categories:
    - Programming languages (Python, Java, JavaScript, etc.)
    - Web technologies (React, Angular, Node.js, etc.)
    - Databases (SQL, MongoDB, PostgreSQL, etc.)
    - ML/AI (TensorFlow, PyTorch, scikit-learn, etc.)
    - Cloud platforms (AWS, Azure, GCP, etc.)
    - Data tools (Pandas, Spark, Tableau, etc.)
    - Soft skills (Leadership, Communication, etc.)
    - And more...
    """

    def __init__(self):
        """Initialize with comprehensive skill database."""
        # Comprehensive skill database organized by category
        self.skill_database = {
            'programming': [
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php',
                'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab', 'perl', 'typescript'
            ],

            'web': [
                'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'django',
                'flask', 'spring', 'asp.net', 'express', 'bootstrap', 'jquery', 'webpack'
            ],

            'database': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'redis',
                'cassandra', 'dynamodb', 'elasticsearch', 'sqlite', 'mariadb'
            ],

            'ml_ai': [
                'machine learning', 'deep learning', 'neural networks', 'tensorflow',
                'pytorch', 'keras', 'scikit-learn', 'nlp', 'computer vision', 'opencv',
                'artificial intelligence', 'data science'
            ],

            'cloud': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
                'terraform', 'ansible', 'ci/cd', 'devops', 'cloud computing'
            ],

            'data': [
                'pandas', 'numpy', 'spark', 'hadoop', 'tableau', 'power bi',
                'excel', 'data analysis', 'statistics', 'etl', 'data mining'
            ],

            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving',
                'analytical', 'creative', 'agile', 'scrum', 'project management',
                'time management', 'customer service'
            ],

            'mobile': [
                'android', 'ios', 'react native', 'flutter', 'xamarin', 'mobile development'
            ],

            'testing': [
                'junit', 'selenium', 'pytest', 'testing', 'qa', 'automation', 'quality assurance'
            ],

            'tools': [
                'git', 'github', 'jira', 'confluence', 'postman', 'visual studio',
                'eclipse', 'intellij', 'vscode', 'slack'
            ],

            'finance': [
                'accounting', 'financial analysis', 'auditing', 'budgeting', 'taxation',
                'quickbooks', 'sap', 'financial modeling', 'payroll'
            ],

            'hr': [
                'human resources', 'recruitment', 'talent acquisition', 'employee relations',
                'performance management', 'compensation', 'benefits', 'hr management'
            ],

            'marketing': [
                'digital marketing', 'seo', 'social media', 'content marketing',
                'marketing strategy', 'branding', 'advertising', 'google analytics'
            ],

            'design': [
                'photoshop', 'illustrator', 'figma', 'sketch', 'ui/ux', 'graphic design',
                'user experience', 'wireframing', 'prototyping'
            ]
        }

        # Flatten all skills for quick lookup
        self.all_skills = set()
        for skills in self.skill_database.values():
            self.all_skills.update(skills)

    def extract_skills(self, text):
        """
        Extract skills from text using word boundary matching.
        
        Uses regex with word boundaries to avoid partial matches.
        Example: "python" won't match "pythonic"
        
        Args:
            text (str): Resume text to analyze
            
        Returns:
            list: List of extracted skills found in text
        """
        if not isinstance(text, str):
            return []

        text_lower = text.lower()
        found_skills = []

        for skill in self.all_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)

        return found_skills

    def categorize_skills(self, skills):
        """
        Categorize a list of skills by type.
        
        Args:
            skills (list): List of skill names
            
        Returns:
            dict: Skills organized by category
                Example: {
                    'programming': ['python', 'java'],
                    'web': ['react', 'nodejs'],
                    ...
                }
        """
        categorized = {category: [] for category in self.skill_database.keys()}

        for skill in skills:
            for category, skill_list in self.skill_database.items():
                if skill in skill_list:
                    categorized[category].append(skill)

        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}

    def get_skill_category(self, skill):
        """
        Get the category of a specific skill.
        
        Args:
            skill (str): Skill name
            
        Returns:
            str: Category name, or None if skill not found
        """
        for category, skill_list in self.skill_database.items():
            if skill in skill_list:
                return category
        return None

    def get_total_skills_count(self):
        """Get total number of skills in database."""
        return len(self.all_skills)

    def get_categories(self):
        """Get all skill categories."""
        return list(self.skill_database.keys())
