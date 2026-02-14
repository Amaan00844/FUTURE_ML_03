"""
Basic Usage Example

Simple example showing how to use the resume screening system
with a minimal dataset.
"""

import pandas as pd
from src import ResumePreprocessor, SkillExtractor, ResumeScorer
from config.job_descriptions import JOB_DESCRIPTIONS


def main():
    """Basic usage example."""
    
    # Sample resumes for demonstration
    sample_resumes = [
        {
            'ID': 1,
            'Resume_str': '''
                Senior Data Scientist with 5 years of experience.
                Expert in Python, Machine Learning, TensorFlow, PyTorch.
                Strong background in statistical analysis and data visualization.
                Experience with Tableau and Power BI dashboards.
                Proficient in SQL, Pandas, NumPy, and scikit-learn.
                Cloud experience with AWS and Azure.
            ''',
            'Category': 'IT'
        },
        {
            'ID': 2,
            'Resume_str': '''
                Full Stack Web Developer with 3 years experience.
                Proficient in JavaScript, React, Node.js, and Angular.
                HTML, CSS expert with Bootstrap knowledge.
                Database experience: MySQL, MongoDB, PostgreSQL.
                Git, Docker, CI/CD pipeline experience.
                RESTful API development and Agile methodology.
            ''',
            'Category': 'IT'
        },
        {
            'ID': 3,
            'Resume_str': '''
                HR Manager with 6 years in talent acquisition.
                Expertise in recruitment, employee relations, performance management.
                Compensation and benefits administration.
                HRIS and payroll management experience.
                Leadership and organizational development.
            ''',
            'Category': 'HR'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_resumes)
    
    print("=" * 80)
    print("RESUME SCREENING SYSTEM - BASIC EXAMPLE")
    print("=" * 80)
    
    # Step 1: Initialize components
    print("\n1️⃣ Initializing components...")
    preprocessor = ResumePreprocessor()
    skill_extractor = SkillExtractor()
    scorer = ResumeScorer()
    print("   ✅ Components initialized")
    
    # Step 2: Preprocess resumes
    print("\n2️⃣ Preprocessing resumes...")
    df['Resume_Cleaned'] = df['Resume_str'].apply(preprocessor.preprocess)
    print("   ✅ Resumes cleaned and normalized")
    
    # Step 3: Extract skills
    print("\n3️⃣ Extracting skills...")
    df['Skills'] = df['Resume_str'].apply(skill_extractor.extract_skills)
    for idx, row in df.iterrows():
        print(f"   Resume {row['ID']}: {len(row['Skills'])} skills found")
    
    # Step 4: Rank candidates
    print("\n4️⃣ Ranking candidates for 'Data Scientist' role...")
    ranked_df = scorer.rank_candidates(
        df,
        job_role='Data Scientist',
        top_n=None,
        verbose=False
    )
    
    # Step 5: Display results
    print("\n" + "=" * 80)
    print("RANKING RESULTS")
    print("=" * 80)
    
    for idx, row in ranked_df.iterrows():
        print(f"\n🏆 Rank #{row['Rank']}")
        print(f"   Resume ID: {row['Resume_ID']}")
        print(f"   Final Score: {row['Final_Score']:.2%}")
        print(f"   Skill Match: {row['Skill_Match_Score']:.2%}")
        print(f"   Text Similarity: {row['Text_Similarity_Score']:.2%}")
        print(f"   Matched Skills ({row['Matched_Skills_Count']}): {', '.join(row['Matched_Skills'][:5])}")
        print(f"   Missing Skills ({row['Missing_Skills_Count']}): {', '.join(row['Missing_Skills'][:5])}")
    
    # Step 6: Export results
    print("\n" + "=" * 80)
    export_df = ranked_df.copy()
    export_df['Matched_Skills'] = export_df['Matched_Skills'].apply(lambda x: ', '.join(x))
    export_df['Missing_Skills'] = export_df['Missing_Skills'].apply(lambda x: ', '.join(x))
    export_df.to_csv('results_basic_example.csv', index=False)
    print("✅ Results exported to 'results_basic_example.csv'")


if __name__ == '__main__':
    main()
