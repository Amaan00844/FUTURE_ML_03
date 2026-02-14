"""
Visualization Examples

Advanced visualization examples for analyzing resume screening results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_score_distributions(ranked_df, role_name):
    """Plot score distributions."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Final Score
    axes[0].hist(ranked_df['Final_Score'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0].axvline(ranked_df['Final_Score'].mean(), color='red', linestyle='--', linewidth=2)
    axes[0].set_title(f'Final Score Distribution - {role_name}', fontweight='bold')
    axes[0].set_xlabel('Final Score')
    axes[0].set_ylabel('Frequency')
    
    # Skill Match Score
    axes[1].hist(ranked_df['Skill_Match_Score'], bins=50, color='green', edgecolor='black', alpha=0.7)
    axes[1].axvline(ranked_df['Skill_Match_Score'].mean(), color='red', linestyle='--', linewidth=2)
    axes[1].set_title('Skill Match Score Distribution', fontweight='bold')
    axes[1].set_xlabel('Skill Match Score')
    axes[1].set_ylabel('Frequency')
    
    # Text Similarity Score
    axes[2].hist(ranked_df['Text_Similarity_Score'], bins=50, color='orange', edgecolor='black', alpha=0.7)
    axes[2].axvline(ranked_df['Text_Similarity_Score'].mean(), color='red', linestyle='--', linewidth=2)
    axes[2].set_title('Text Similarity Distribution', fontweight='bold')
    axes[2].set_xlabel('Text Similarity Score')
    axes[2].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(f'viz_score_distributions_{role_name}.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved: viz_score_distributions_{role_name}.png")
    plt.close()


def plot_top_candidates_comparison(ranked_df, role_name, top_n=20):
    """Plot comparison of top N candidates."""
    top_candidates = ranked_df.head(top_n)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(top_candidates))
    width = 0.25
    
    ax.bar(x - width, top_candidates['Skill_Match_Score'], width, 
           label='Skill Match', color='skyblue', edgecolor='black')
    ax.bar(x, top_candidates['Text_Similarity_Score'], width, 
           label='Text Similarity', color='lightcoral', edgecolor='black')
    ax.bar(x + width, top_candidates['Final_Score'], width, 
           label='Final Score', color='lightgreen', edgecolor='black')
    
    ax.set_xlabel('Candidate Rank', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title(f'Top {top_n} Candidates Comparison - {role_name}', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'#{i+1}' for i in range(len(top_candidates))])
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim([0, 1])
    
    plt.tight_layout()
    plt.savefig(f'viz_top_candidates_{role_name}.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved: viz_top_candidates_{role_name}.png")
    plt.close()


def plot_skill_gap_analysis(ranked_df, role_name, top_n=25):
    """Plot skill gaps for top candidates."""
    top_candidates = ranked_df.head(top_n)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Matched Skills
    axes[0].barh(range(len(top_candidates)), top_candidates['Matched_Skills_Count'], 
                 color='green', alpha=0.7, edgecolor='black')
    axes[0].set_yticks(range(len(top_candidates)))
    axes[0].set_yticklabels([f'Rank #{i+1}' for i in range(len(top_candidates))], fontsize=8)
    axes[0].set_xlabel('Number of Matched Skills', fontsize=11, fontweight='bold')
    axes[0].set_title(f'Matched Skills - Top {top_n} Candidates', fontsize=12, fontweight='bold')
    axes[0].invert_yaxis()
    axes[0].grid(axis='x', alpha=0.3)
    
    # Missing Skills
    axes[1].barh(range(len(top_candidates)), top_candidates['Missing_Skills_Count'], 
                 color='red', alpha=0.7, edgecolor='black')
    axes[1].set_yticks(range(len(top_candidates)))
    axes[1].set_yticklabels([f'Rank #{i+1}' for i in range(len(top_candidates))], fontsize=8)
    axes[1].set_xlabel('Number of Missing Skills', fontsize=11, fontweight='bold')
    axes[1].set_title(f'Missing Skills - Top {top_n} Candidates', fontsize=12, fontweight='bold')
    axes[1].invert_yaxis()
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'viz_skill_gaps_{role_name}.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved: viz_skill_gaps_{role_name}.png")
    plt.close()


def plot_category_performance(ranked_df, role_name):
    """Plot performance by resume category."""
    if 'Category' not in ranked_df.columns:
        print("⚠️  'Category' column not found, skipping category analysis")
        return
    
    category_stats = ranked_df.groupby('Category').agg({
        'Final_Score': 'mean',
        'Resume_ID': 'count'
    }).rename(columns={'Resume_ID': 'Count'}).sort_values('Final_Score', ascending=False)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Top 15 categories by score
    top_categories = category_stats['Final_Score'].head(15)
    axes[0].barh(range(len(top_categories)), top_categories.values, 
                 color='teal', alpha=0.7, edgecolor='black')
    axes[0].set_yticks(range(len(top_categories)))
    axes[0].set_yticklabels(top_categories.index, fontsize=10)
    axes[0].set_xlabel('Average Final Score', fontsize=11, fontweight='bold')
    axes[0].set_title(f'Top 15 Categories by Score - {role_name}', fontsize=12, fontweight='bold')
    axes[0].invert_yaxis()
    axes[0].grid(axis='x', alpha=0.3)
    
    # Top 15 categories by count
    top_counts = category_stats['Count'].head(15)
    axes[1].barh(range(len(top_counts)), top_counts.values, 
                 color='purple', alpha=0.7, edgecolor='black')
    axes[1].set_yticks(range(len(top_counts)))
    axes[1].set_yticklabels(top_counts.index, fontsize=10)
    axes[1].set_xlabel('Number of Candidates', fontsize=11, fontweight='bold')
    axes[1].set_title('Top 15 Categories by Candidate Count', fontsize=12, fontweight='bold')
    axes[1].invert_yaxis()
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'viz_category_performance_{role_name}.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved: viz_category_performance_{role_name}.png")
    plt.close()


def plot_score_percentiles(ranked_df, role_name):
    """Plot percentile distribution."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    percentiles = np.arange(0, 101, 5)
    percentile_values = [np.percentile(ranked_df['Final_Score'], p) for p in percentiles]
    
    ax.fill_between(percentiles, percentile_values, alpha=0.3, color='steelblue')
    ax.plot(percentiles, percentile_values, marker='o', linewidth=2, markersize=6, color='steelblue')
    
    ax.set_xlabel('Percentile', fontsize=12, fontweight='bold')
    ax.set_ylabel('Final Score', fontsize=12, fontweight='bold')
    ax.set_title(f'Score Percentile Distribution - {role_name}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 1])
    
    # Add annotations
    ax.annotate(f'90th: {np.percentile(ranked_df["Final_Score"], 90):.2%}',
                xy=(90, np.percentile(ranked_df['Final_Score'], 90)),
                xytext=(80, np.percentile(ranked_df['Final_Score'], 90) + 0.1),
                arrowprops=dict(arrowstyle='->', color='red'))
    
    plt.tight_layout()
    plt.savefig(f'viz_percentiles_{role_name}.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved: viz_percentiles_{role_name}.png")
    plt.close()


def create_all_visualizations(ranked_df, role_name):
    """Create all available visualizations."""
    print(f"\n📊 Creating visualizations for {role_name}...")
    plot_score_distributions(ranked_df, role_name)
    plot_top_candidates_comparison(ranked_df, role_name, top_n=20)
    plot_skill_gap_analysis(ranked_df, role_name, top_n=25)
    plot_category_performance(ranked_df, role_name)
    plot_score_percentiles(ranked_df, role_name)
    print(f"✅ All visualizations created!")
