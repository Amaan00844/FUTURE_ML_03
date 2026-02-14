"""
Resume Scoring & Ranking Module

Scores resumes against job descriptions using hybrid approach:
- Skill matching (40% weight)
- Text similarity (60% weight)
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResumeScorer:
    """
    Scores and ranks resumes against job descriptions.
    
    Scoring formula:
    Final_Score = (0.4 * Skill_Match_Score) + (0.6 * Text_Similarity_Score)
    
    Where:
    - Skill_Match_Score: % of required skills present in resume
    - Text_Similarity_Score: Cosine similarity of TF-IDF vectors
    """

    def __init__(self):
        """Initialize scorer with TF-IDF vectorizer."""
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))

    def calculate_skill_match_score(self, resume_skills, required_skills):
        """
        Calculate percentage of required skills present in resume.
        
        Args:
            resume_skills (list): Skills found in resume
            required_skills (list): Skills required for job
            
        Returns:
            float: Score between 0.0 and 1.0 (percentage as decimal)
        """
        if not required_skills:
            return 0.0

        resume_skills_set = set(resume_skills)
        required_skills_set = set(required_skills)

        matched_skills = resume_skills_set.intersection(required_skills_set)
        score = len(matched_skills) / len(required_skills_set)

        return score

    def calculate_text_similarity(self, resume_text, job_description):
        """
        Calculate cosine similarity between resume and job description.
        
        Uses TF-IDF vectorization for both documents and computes
        cosine similarity of the resulting vectors.
        
        Args:
            resume_text (str): Preprocessed resume text
            job_description (str): Preprocessed job description
            
        Returns:
            float: Similarity score between 0.0 and 1.0
        """
        try:
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_description])

            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

            return similarity
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0

    def calculate_skill_gap(self, resume_skills, required_skills):
        """
        Identify matched and missing skills.
        
        Args:
            resume_skills (list): Skills found in resume
            required_skills (list): Skills required for job
            
        Returns:
            tuple: (matched_skills_list, missing_skills_list)
        """
        resume_skills_set = set(resume_skills)
        required_skills_set = set(required_skills)

        matched_skills = required_skills_set.intersection(resume_skills_set)
        missing_skills = required_skills_set - resume_skills_set

        return list(matched_skills), list(missing_skills)

    def score_resume(self, resume_text, resume_skills, job_description, required_skills):
        """
        Calculate comprehensive resume score.
        
        Combines skill matching and text similarity with weighted scoring.
        
        Args:
            resume_text (str): Preprocessed resume text
            resume_skills (list): Extracted skills from resume
            job_description (str): Preprocessed job description
            required_skills (list): Required skills for job
            
        Returns:
            dict: Contains 'skill_match_score', 'text_similarity_score', 'final_score'
        """
        # Skill match score (40% weight)
        skill_score = self.calculate_skill_match_score(resume_skills, required_skills)

        # Text similarity score (60% weight)
        text_score = self.calculate_text_similarity(resume_text, job_description)

        # Combined weighted score
        final_score = (0.4 * skill_score) + (0.6 * text_score)

        return {
            'skill_match_score': skill_score,
            'text_similarity_score': text_score,
            'final_score': final_score
        }

    def rank_candidates(self, df, job_role, job_descriptions_cleaned, 
                       job_required_skills, top_n=1000, verbose=True):
        """
        Rank all candidates for a specific job role.
        
        Args:
            df (DataFrame): DataFrame with columns: ID, Resume_Cleaned, Skills, Category
            job_role (str): Target job role to score against
            job_descriptions_cleaned (dict): Dict of role -> cleaned description
            job_required_skills (dict): Dict of role -> required skills list
            top_n (int): Return top N candidates (None for all)
            verbose (bool): Print progress messages
            
        Returns:
            DataFrame: Ranked candidates with scores and skill gaps
        """
        if verbose:
            print(f"🎯 Ranking candidates for: {job_role}")
            print(f"📊 Processing {len(df):,} resumes...\n")

        job_description = job_descriptions_cleaned[job_role]
        required_skills = job_required_skills[job_role]

        results = []

        # Process all candidates
        chunk_size = 5000
        for i in range(0, len(df), chunk_size):
            end_idx = min(i + chunk_size, len(df))
            chunk = df.iloc[i:end_idx]

            for idx, row in chunk.iterrows():
                scores = self.score_resume(
                    row['Resume_Cleaned'],
                    row['Skills'],
                    job_description,
                    required_skills
                )

                matched_skills, missing_skills = self.calculate_skill_gap(
                    row['Skills'],
                    required_skills
                )

                results.append({
                    'Resume_ID': row['ID'],
                    'Category': row['Category'],
                    'Skill_Match_Score': scores['skill_match_score'],
                    'Text_Similarity_Score': scores['text_similarity_score'],
                    'Final_Score': scores['final_score'],
                    'Matched_Skills': matched_skills,
                    'Missing_Skills': missing_skills,
                    'Matched_Skills_Count': len(matched_skills),
                    'Missing_Skills_Count': len(missing_skills)
                })

            if verbose:
                print(f"   Processed {end_idx:,} / {len(df):,} resumes ({(end_idx/len(df))*100:.1f}%)")

        # Create dataframe and sort by final score
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('Final_Score', ascending=False).reset_index(drop=True)
        results_df['Rank'] = range(1, len(results_df) + 1)

        # Return top N results
        if top_n and top_n < len(results_df):
            return results_df.head(top_n).reset_index(drop=True)

        return results_df

    def get_score_statistics(self, ranked_df):
        """
        Get statistical summary of ranking scores.
        
        Args:
            ranked_df (DataFrame): Ranked candidates DataFrame
            
        Returns:
            dict: Statistics including mean, median, min, max for each score
        """
        return {
            'final_score': {
                'mean': ranked_df['Final_Score'].mean(),
                'median': ranked_df['Final_Score'].median(),
                'min': ranked_df['Final_Score'].min(),
                'max': ranked_df['Final_Score'].max(),
                'std': ranked_df['Final_Score'].std()
            },
            'skill_match_score': {
                'mean': ranked_df['Skill_Match_Score'].mean(),
                'median': ranked_df['Skill_Match_Score'].median(),
                'min': ranked_df['Skill_Match_Score'].min(),
                'max': ranked_df['Skill_Match_Score'].max()
            },
            'text_similarity_score': {
                'mean': ranked_df['Text_Similarity_Score'].mean(),
                'median': ranked_df['Text_Similarity_Score'].median(),
                'min': ranked_df['Text_Similarity_Score'].min(),
                'max': ranked_df['Text_Similarity_Score'].max()
            }
        }
