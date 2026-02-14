"""
Resume Screening & Ranking System
ML-based system for automated resume screening, skill extraction, and candidate ranking.
"""

__version__ = "1.0.0"
__author__ = "HR Tech Team"

from .preprocessor import ResumePreprocessor
from .skill_extractor import SkillExtractor
from .scorer import ResumeScorer

__all__ = [
    'ResumePreprocessor',
    'SkillExtractor',
    'ResumeScorer',
]
