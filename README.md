# Resume Screening & Ranking System

A comprehensive **ML-based resume screening and ranking system** that automatically evaluates, scores, and ranks resumes against job descriptions.

## 🎯 Features

✅ **Resume Preprocessing** - Clean and normalize resume text (remove URLs, emails, special characters)  
✅ **Skill Extraction** - Extract 150+ technical and professional skills using NLP  
✅ **Job Description Parsing** - Parse and analyze job requirements  
✅ **Resume Scoring** - Hybrid scoring combining skill matching (40%) and text similarity (60%)  
✅ **Candidate Ranking** - Automatically rank candidates by job role fit  
✅ **Skill Gap Analysis** - Identify matched skills and missing skills for each candidate  
✅ **Comprehensive Visualizations** - Score distributions, comparisons, category analysis  
✅ **Export Results** - Save ranked candidates to CSV for further use

## 📊 System Overview

### Scoring Methodology

The system uses a **hybrid scoring approach** to evaluate each resume:

```
Final_Score = (0.4 × Skill_Match_Score) + (0.6 × Text_Similarity_Score)
```

#### 1. Skill Match Score (40% weight)

- Extracts skills from resume text
- Compares against required skills for the job role
- Score = (Matched Skills) / (Total Required Skills)
- **Why 40%?** Skills are important but not always mentioned explicitly in resumes

#### 2. Text Similarity Score (60% weight)

- Uses TF-IDF vectorization of both resume and job description
- Calculates cosine similarity between vectors
- Score ranges from 0 to 1
- **Why 60%?** Captures overall content alignment and context that skill matching might miss

### Example Score Calculation

```
Resume: "Expert Python developer with 5 years experience in machine learning"
Job: "Seeking Python developer with machine learning expertise"

Skill Match Score: 0.8 (has 4/5 required skills)
Text Similarity: 0.85 (strong content overlap)
Final Score = (0.4 × 0.8) + (0.6 × 0.85) = 0.32 + 0.51 = 0.83 (83%)
```

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Resume-Screening-System.git
cd Resume-Screening-System

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Basic Usage

```python
import pandas as pd
from src import ResumePreprocessor, SkillExtractor, ResumeScorer
from config.job_descriptions import JOB_DESCRIPTIONS

# Load your resume dataset
df = pd.read_csv('your_resumes.csv')  # Columns: ID, Resume_str, Category

# Initialize components
preprocessor = ResumePreprocessor()
skill_extractor = SkillExtractor()
scorer = ResumeScorer()

# Preprocess resumes
df['Resume_Cleaned'] = df['Resume_str'].apply(preprocessor.preprocess)

# Extract skills
df['Skills'] = df['Resume_str'].apply(skill_extractor.extract_skills)

# Rank candidates for a job role
ranked_candidates = scorer.rank_candidates(
    df,
    job_role='Data Scientist',
    top_n=100
)

print(ranked_candidates.head(10))
```

## 📁 Project Structure

```
Resume-Screening-System/
├── src/
│   ├── __init__.py                 # Package initialization
│   ├── preprocessor.py             # Text preprocessing class
│   ├── skill_extractor.py          # Skill extraction class
│   └── scorer.py                   # Resume scoring & ranking class
├── config/
│   └── job_descriptions.py         # Job descriptions & configuration
├── examples/
│   ├── basic_usage.py              # Basic usage example
│   ├── full_pipeline.py            # Complete pipeline example
│   └── visualization_example.py    # Visualization examples
├── tests/
│   ├── test_preprocessor.py        # Preprocessor tests
│   ├── test_skill_extractor.py     # Skill extractor tests
│   └── test_scorer.py              # Scorer tests
├── requirements.txt                 # Dependencies
├── README.md                        # This file
└── .gitignore                       # Git ignore rules
```

## 💡 Key Components

### 1. ResumePreprocessor

Cleans and normalizes resume text for NLP analysis.

```python
preprocessor = ResumePreprocessor()

# Removes:
# - URLs (http://, https://, www.)
# - Email addresses
# - Special characters and numbers
# - Stopwords (the, a, is, etc.)

cleaned_text = preprocessor.preprocess(raw_resume_text)
```

### 2. SkillExtractor

Extracts technical and professional skills from resume text.

```python
skill_extractor = SkillExtractor()

# Supports 150+ skills across 14 categories:
categories = skill_extractor.get_categories()
# ['programming', 'web', 'database', 'ml_ai', 'cloud', 'data',
#  'soft_skills', 'mobile', 'testing', 'tools', 'finance', 'hr', 'marketing', 'design']

# Extract skills from text
skills = skill_extractor.extract_skills("Python expert with AWS and SQL experience")
# Returns: ['python', 'aws', 'sql']

# Categorize skills
categorized = skill_extractor.categorize_skills(skills)
# Returns: {'programming': ['python'], 'cloud': ['aws'], 'database': ['sql']}
```

### 3. ResumeScorer

Scores and ranks resumes against job descriptions.

```python
scorer = ResumeScorer()

# Score a single resume
scores = scorer.score_resume(
    resume_text="...",
    resume_skills=['python', 'sql'],
    job_description="...",
    required_skills=['python', 'sql', 'spark']
)
# Returns: {
#     'skill_match_score': 0.67,
#     'text_similarity_score': 0.75,
#     'final_score': 0.72
# }

# Rank all resumes for a job
ranked = scorer.rank_candidates(
    df=resumes_dataframe,
    job_role='Data Scientist',
    top_n=100
)
```

## 📚 Dataset Requirements

Your resume CSV should have these columns:

| Column     | Type    | Description                  |
| ---------- | ------- | ---------------------------- |
| ID         | int/str | Unique resume identifier     |
| Resume_str | str     | Raw resume text content      |
| Category   | str     | Job category/role (optional) |

Example:

```
ID,Resume_str,Category
1,"Expert Python developer with 5 years...",IT
2,"Experienced accountant with CPA...",Finance
```

## 📊 Output Columns

The ranking results DataFrame includes:

| Column                | Type    | Description                     |
| --------------------- | ------- | ------------------------------- |
| Rank                  | int     | Candidate ranking position      |
| Resume_ID             | int/str | Resume identifier               |
| Category              | str     | Resume category                 |
| Final_Score           | float   | Combined ranking score (0-1)    |
| Skill_Match_Score     | float   | Skill matching percentage (0-1) |
| Text_Similarity_Score | float   | Content similarity score (0-1)  |
| Matched_Skills        | list    | Skills candidate has            |
| Missing_Skills        | list    | Skills candidate lacks          |
| Matched_Skills_Count  | int     | Number of matched skills        |
| Missing_Skills_Count  | int     | Number of missing skills        |

## 🎓 Skill Categories

The system recognizes skills across 14 categories:

1. **Programming**: Python, Java, JavaScript, C++, C#, Ruby, PHP, Swift, Kotlin, Go, Rust, Scala, R, MATLAB, Perl, TypeScript

2. **Web**: HTML, CSS, React, Angular, Vue, Node.js, Django, Flask, Spring, ASP.NET, Express, Bootstrap, jQuery, Webpack

3. **Database**: SQL, MySQL, PostgreSQL, MongoDB, Oracle, Redis, Cassandra, DynamoDB, Elasticsearch, SQLite, MariaDB

4. **ML/AI**: Machine Learning, Deep Learning, Neural Networks, TensorFlow, PyTorch, Keras, scikit-learn, NLP, Computer Vision, OpenCV, Artificial Intelligence, Data Science

5. **Cloud**: AWS, Azure, GCP, Docker, Kubernetes, Jenkins, Terraform, Ansible, CI/CD, DevOps, Cloud Computing

6. **Data**: Pandas, NumPy, Spark, Hadoop, Tableau, Power BI, Excel, Data Analysis, Statistics, ETL, Data Mining

7. **Soft Skills**: Leadership, Communication, Teamwork, Problem Solving, Analytical, Creative, Agile, Scrum, Project Management, Time Management, Customer Service

8. **Mobile**: Android, iOS, React Native, Flutter, Xamarin, Mobile Development

9. **Testing**: JUnit, Selenium, Pytest, Testing, QA, Automation, Quality Assurance

10. **Tools**: Git, GitHub, Jira, Confluence, Postman, Visual Studio, Eclipse, IntelliJ, VSCode, Slack

11. **Finance**: Accounting, Financial Analysis, Auditing, Budgeting, Taxation, QuickBooks, SAP, Financial Modeling, Payroll

12. **HR**: Human Resources, Recruitment, Talent Acquisition, Employee Relations, Performance Management, Compensation, Benefits, HR Management

13. **Marketing**: Digital Marketing, SEO, Social Media, Content Marketing, Marketing Strategy, Branding, Advertising, Google Analytics

14. **Design**: Photoshop, Illustrator, Figma, Sketch, UI/UX, Graphic Design, User Experience, Wireframing, Prototyping

## 🔍 Example Use Cases

### 1. Candidate Screening

```python
# Screen 10,000 candidates for Senior Data Scientist role
ranked = scorer.rank_candidates(df, 'Data Scientist', top_n=10000)
top_100 = ranked.head(100)  # Get top 100 candidates
```

### 2. Skill Gap Analysis

```python
# Find what skills candidates are missing
for idx, candidate in ranked.head(20).iterrows():
    print(f"Rank {candidate['Rank']}: Missing {', '.join(candidate['Missing_Skills'])}")
```

### 3. Category Performance

```python
# See which resume categories match best
category_performance = ranked.groupby('Category')['Final_Score'].mean().sort_values(ascending=False)
```

### 4. Batch Processing

```python
# Rank candidates for multiple roles
for role in ['Data Scientist', 'Web Developer', 'Java Developer']:
    ranked = scorer.rank_candidates(df, role, top_n=500)
    ranked.to_csv(f'ranked_{role}.csv', index=False)
```

## 📈 Performance Metrics

The system has been tested on:

- **66,017 resumes** from diverse job categories
- **7 job roles** with pre-defined descriptions
- **150+ technical and professional skills**
- **Average processing time**: ~5 seconds per 1000 resumes

## 🔧 Configuration

Modify scoring weights and parameters in `config/job_descriptions.py`:

```python
DEFAULT_CONFIG = {
    'skill_weight': 0.4,           # Adjust skill importance (0-1)
    'similarity_weight': 0.6,      # Adjust content importance (0-1)
    'max_features': 500,           # TF-IDF features
    'ngram_range': (1, 2),        # Word groupings
    'top_n_candidates': 1000,     # Default candidates to return
    'min_word_length': 2,         # Minimum word size
}
```

## 📝 Adding Custom Job Roles

Edit `config/job_descriptions.py` and add new roles:

```python
JOB_DESCRIPTIONS = {
    # ... existing roles ...
    'Your Custom Role': """
        Description of your custom role...
        Include required skills, experience level, etc.
    """
}
```

Then use it:

```python
ranked = scorer.rank_candidates(df, 'Your Custom Role', top_n=100)
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_preprocessor.py -v

# Run with coverage
python -m pytest tests/ --cov=src
```

## 📦 Dependencies

- **spacy** (3.5.0+) - NLP processing
- **scikit-learn** (1.2.0+) - Machine learning & vectorization
- **pandas** (1.5.0+) - Data manipulation
- **numpy** (1.23.0+) - Numerical operations
- **nltk** (3.8.0+) - Natural language toolkit
- **matplotlib** (3.6.0+) - Visualization
- **seaborn** (0.12.0+) - Statistical visualization

## 🎯 Why This Approach?

### Hybrid Scoring (Why 40/60 Split?)

**Skill Matching Alone (40% only):**

- ❌ Misses candidates with transferable skills
- ❌ Doesn't capture industry experience
- ❌ Penalizes unconventional resume formats

**Text Similarity Alone (60% only):**

- ❌ Matches generic phrases that don't indicate competence
- ❌ Can rate unqualified candidates high

**Combined Approach (40/60):**

- ✅ Captures both explicit skills and implicit context
- ✅ Balances precision (skills) with recall (content match)
- ✅ More robust to resume format variations

### TF-IDF + Cosine Similarity

- **Why TF-IDF?** Weights important words higher while reducing common words
- **Why Cosine Similarity?** Measures angle between documents (semantic distance)
- **Result:** Captures overall resume-job alignment beyond keyword matching

## 📊 Visualization Features

The system provides:

1. **Score Distribution Charts** - Understand candidate quality distribution
2. **Candidate Comparison** - Side-by-side score comparison of top candidates
3. **Skill Gap Analysis** - Visual breakdown of matched vs missing skills
4. **Category Performance** - Which resume categories match best for each role

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙋 Support

For issues, questions, or suggestions:

1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include sample data if applicable

## 🎊 Summary

| Aspect                  | Details                           |
| ----------------------- | --------------------------------- |
| **Resumes Processed**   | 66,017+                           |
| **Skills Recognized**   | 150+                              |
| **Job Roles Supported** | 7 predefined + custom             |
| **Scoring Accuracy**    | Hybrid approach (skill + content) |
| **Export Formats**      | CSV, DataFrame                    |
| **Processing Speed**    | ~5 sec per 1000 resumes           |
| **Code Quality**        | Fully documented, tested          |

---

**Built for recruiters, HR managers, and HR-tech startups** 🚀

Perfect for screening, ranking, and analyzing large candidate pools efficiently!
#   F U T U R E _ M L _ 0 3  
 