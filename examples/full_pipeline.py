"""
Full Pipeline Example

Complete example showing all features of the resume screening system.
Assumes you have a CSV file with resumes.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src import ResumePreprocessor, SkillExtractor, ResumeScorer
from config.job_descriptions import JOB_DESCRIPTIONS

# Set visualization style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 7)


def load_data(csv_path):
    """Load resume data from CSV."""
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df):,} resumes")
    print(f"   Columns: {', '.join(df.columns)}")
    return df


def preprocess_resumes(df):
    """Preprocess all resumes."""
    print("\n🔄 Preprocessing resumes...")
    preprocessor = ResumePreprocessor()
    
    df['Resume_Cleaned'] = df['Resume_str'].apply(preprocessor.preprocess)
    print(f"✅ Preprocessing complete")
    return df, preprocessor


def extract_skills_batch(df):
    """Extract skills from all resumes."""
    print("\n🔍 Extracting skills...")
    skill_extractor = SkillExtractor()
    
    df['Skills'] = df['Resume_str'].apply(skill_extractor.extract_skills)
    df['Skill_Count'] = df['Skills'].apply(len)
    
    print(f"✅ Skills extracted")
    print(f"   Average skills per resume: {df['Skill_Count'].mean():.2f}")
    print(f"   Max skills: {df['Skill_Count'].max()}")
    print(f"   Min skills: {df['Skill_Count'].min()}")
    
    return df, skill_extractor


def rank_for_multiple_roles(df, scorer, job_descriptions, top_n=500):
    """Rank candidates for multiple job roles."""
    print("\n📊 Ranking candidates for all roles...")
    
    results_by_role = {}
    
    for role in job_descriptions.keys():
        print(f"\n   Processing: {role}...")
        ranked = scorer.rank_candidates(
            df,
            job_role=role,
            top_n=top_n,
            verbose=False
        )
        results_by_role[role] = ranked
        print(f"      Top score: {ranked['Final_Score'].iloc[0]:.2%}")
    
    print("\n✅ Ranking complete for all roles")
    return results_by_role


def analyze_results(results_by_role, role):
    """Analyze results for a specific role."""
    ranked = results_by_role[role]
    
    print(f"\n" + "=" * 80)
    print(f"ANALYSIS FOR: {role.upper()}")
    print("=" * 80)
    
    print(f"\n📊 Score Statistics:")
    print(f"   Average Score: {ranked['Final_Score'].mean():.2%}")
    print(f"   Median Score: {ranked['Final_Score'].median():.2%}")
    print(f"   Min Score: {ranked['Final_Score'].min():.2%}")
    print(f"   Max Score: {ranked['Final_Score'].max():.2%}")
    
    print(f"\n🏆 Top 5 Candidates:")
    for idx, row in ranked.head(5).iterrows():
        print(f"\n   #{row['Rank']} - Resume ID: {row['Resume_ID']}")
        print(f"      Final Score: {row['Final_Score']:.2%}")
        print(f"      Skill Match: {row['Skill_Match_Score']:.2%}")
        print(f"      Matched Skills: {len(row['Matched_Skills'])}")
        print(f"      Missing Skills: {len(row['Missing_Skills'])}")
    
    return ranked


def visualize_results(ranked, role):
    """Create visualizations for ranking results."""
    print(f"\n📈 Creating visualizations for {role}...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Score Distribution
    axes[0, 0].hist(ranked['Final_Score'], bins=30, color='steelblue', alpha=0.7)
    axes[0, 0].axvline(ranked['Final_Score'].mean(), color='red', linestyle='--',
                       label=f'Mean: {ranked["Final_Score"].mean():.2f}')
    axes[0, 0].set_title(f'Final Score Distribution - {role}', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Score')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].legend()
    
    # 2. Top 20 Candidates Comparison
    top_20 = ranked.head(20)
    x = range(len(top_20))
    axes[0, 1].plot(x, top_20['Final_Score'], marker='o', label='Final Score', linewidth=2)
    axes[0, 1].plot(x, top_20['Skill_Match_Score'], marker='s', label='Skill Match', linewidth=2)
    axes[0, 1].plot(x, top_20['Text_Similarity_Score'], marker='^', label='Text Similarity', linewidth=2)
    axes[0, 1].set_title('Top 20 Candidates Score Comparison', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Rank')
    axes[0, 1].set_ylabel('Score')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Skill Gap Analysis
    top_25 = ranked.head(25)
    axes[1, 0].barh(range(len(top_25)), top_25['Matched_Skills_Count'], 
                    color='green', alpha=0.7, label='Matched')
    axes[1, 0].set_yticks(range(len(top_25)))
    axes[1, 0].set_yticklabels([f'#{i+1}' for i in range(len(top_25))], fontsize=8)
    axes[1, 0].set_title('Skills Match - Top 25 Candidates', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Number of Matched Skills')
    axes[1, 0].invert_yaxis()
    axes[1, 0].grid(True, alpha=0.3, axis='x')
    
    # 4. Category-wise Average Score
    if 'Category' in ranked.columns:
        category_avg = ranked.groupby('Category')['Final_Score'].mean().sort_values(ascending=True).tail(10)
        axes[1, 1].barh(range(len(category_avg)), category_avg.values, color='teal', alpha=0.7)
        axes[1, 1].set_yticks(range(len(category_avg)))
        axes[1, 1].set_yticklabels(category_avg.index, fontsize=9)
        axes[1, 1].set_title('Top 10 Categories by Average Score', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel('Average Final Score')
        axes[1, 1].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(f'visualization_{role.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: visualization_{role.replace(' ', '_')}.png")
    plt.close()


def export_results(results_by_role):
    """Export all results to CSV."""
    print("\n📤 Exporting results...")
    
    for role, ranked in results_by_role.items():
        export_df = ranked.copy()
        export_df['Matched_Skills'] = export_df['Matched_Skills'].apply(lambda x: ', '.join(x))
        export_df['Missing_Skills'] = export_df['Missing_Skills'].apply(lambda x: ', '.join(x))
        
        filename = f'ranked_candidates_{role.replace(" ", "_")}.csv'
        export_df.to_csv(filename, index=False)
        print(f"   ✅ {filename}")


def main():
    """Run complete pipeline."""
    print("=" * 80)
    print("RESUME SCREENING SYSTEM - FULL PIPELINE")
    print("=" * 80)
    
    # TODO: Update with your CSV path
    CSV_PATH = 'your_resumes.csv'  # Change this to your file
    TARGET_ROLES = ['Data Scientist', 'Web Developer', 'Java Developer']  # Select roles
    
    try:
        # Load and preprocess
        df = load_data(CSV_PATH)
        df, preprocessor = preprocess_resumes(df)
        df, skill_extractor = extract_skills_batch(df)
        
        # Initialize scorer
        scorer = ResumeScorer()
        
        # Rank candidates for multiple roles
        results = rank_for_multiple_roles(
            df,
            scorer,
            {role: JOB_DESCRIPTIONS[role] for role in TARGET_ROLES},
            top_n=1000
        )
        
        # Analyze and visualize
        for role in TARGET_ROLES:
            ranked = analyze_results(results, role)
            visualize_results(ranked, role)
        
        # Export results
        export_results(results)
        
        print("\n" + "=" * 80)
        print("✅ PIPELINE COMPLETE!")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find {CSV_PATH}")
        print("   Please update CSV_PATH with your resume file location")


if __name__ == '__main__':
    main()
