"""
Resume Screening System - Command Line Interface

Main entry point for the resume screening and ranking system.
Usage: python main.py --csv <path> --role <role> --top_n <number>
"""

import argparse
import pandas as pd
from src import ResumePreprocessor, SkillExtractor, ResumeScorer
from config.job_descriptions import JOB_DESCRIPTIONS, AVAILABLE_ROLES


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Resume Screening & Ranking System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py --csv resumes.csv --role "Data Scientist"
  python main.py --csv resumes.csv --role "Web Developer" --top_n 500
  python main.py --csv resumes.csv --list  # Show all available roles
        '''
    )
    
    parser.add_argument(
        '--csv',
        required=False,
        help='Path to CSV file with resumes (columns: ID, Resume_str, Category)'
    )
    
    parser.add_argument(
        '--role',
        default='Data Scientist',
        help=f'Job role to rank for (default: Data Scientist)'
    )
    
    parser.add_argument(
        '--top_n',
        type=int,
        default=1000,
        help='Number of top candidates to return (default: 1000)'
    )
    
    parser.add_argument(
        '--output',
        default=None,
        help='Output CSV filename (default: ranked_candidates_<role>.csv)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available job roles'
    )
    
    args = parser.parse_args()
    
    # Show available roles
    if args.list:
        print("\n📋 Available Job Roles:")
        print("=" * 50)
        for i, role in enumerate(AVAILABLE_ROLES, 1):
            print(f"  {i}. {role}")
        return
    
    # Validate inputs
    if not args.csv:
        print("❌ Error: --csv argument is required")
        parser.print_help()
        return
    
    if args.role not in JOB_DESCRIPTIONS:
        print(f"❌ Error: Invalid role '{args.role}'")
        print(f"\nAvailable roles: {', '.join(AVAILABLE_ROLES)}")
        return
    
    try:
        # Load data
        print(f"\n{'='*80}")
        print("RESUME SCREENING & RANKING SYSTEM")
        print(f"{'='*80}\n")
        
        print(f"📂 Loading CSV: {args.csv}")
        df = pd.read_csv(args.csv)
        print(f"   ✅ Loaded {len(df):,} resumes")
        
        # Initialize components
        print(f"\n⚙️  Initializing components...")
        preprocessor = ResumePreprocessor()
        skill_extractor = SkillExtractor()
        scorer = ResumeScorer()
        print(f"   ✅ Components initialized")
        
        # Preprocess
        print(f"\n🔄 Preprocessing resumes...")
        df['Resume_Cleaned'] = df['Resume_str'].apply(preprocessor.preprocess)
        print(f"   ✅ Preprocessing complete")
        
        # Extract skills
        print(f"\n🔍 Extracting skills...")
        df['Skills'] = df['Resume_str'].apply(skill_extractor.extract_skills)
        df['Skill_Count'] = df['Skills'].apply(len)
        print(f"   ✅ Skills extracted")
        print(f"   Average skills per resume: {df['Skill_Count'].mean():.2f}")
        
        # Rank
        print(f"\n📊 Ranking candidates for: {args.role}")
        ranked = scorer.rank_candidates(
            df,
            job_role=args.role,
            top_n=args.top_n,
            verbose=True
        )
        
        # Display results
        print(f"\n{'='*80}")
        print("TOP 10 CANDIDATES")
        print(f"{'='*80}\n")
        
        for idx, row in ranked.head(10).iterrows():
            print(f"🏆 Rank #{row['Rank']}")
            print(f"   Resume ID: {row['Resume_ID']}")
            print(f"   Final Score: {row['Final_Score']:.2%}")
            print(f"   Skill Match: {row['Skill_Match_Score']:.2%}")
            print(f"   Text Similarity: {row['Text_Similarity_Score']:.2%}")
            print(f"   Matched Skills: {row['Matched_Skills_Count']}")
            print(f"   Missing Skills: {row['Missing_Skills_Count']}")
            print()
        
        # Export
        output_file = args.output or f'ranked_candidates_{args.role.replace(" ", "_")}.csv'
        export_df = ranked.copy()
        export_df['Matched_Skills'] = export_df['Matched_Skills'].apply(lambda x: ', '.join(x))
        export_df['Missing_Skills'] = export_df['Missing_Skills'].apply(lambda x: ', '.join(x))
        export_df.to_csv(output_file, index=False)
        
        print(f"{'='*80}")
        print(f"✅ COMPLETE!")
        print(f"{'='*80}")
        print(f"\n📊 Results Summary:")
        print(f"   Total candidates ranked: {len(ranked):,}")
        print(f"   Average score: {ranked['Final_Score'].mean():.2%}")
        print(f"   Highest score: {ranked['Final_Score'].max():.2%}")
        print(f"\n💾 Results saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find file '{args.csv}'")
    except KeyError as e:
        print(f"❌ Error: Missing required column {e}")
        print("   Required columns: ID, Resume_str, Category (optional)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == '__main__':
    main()
