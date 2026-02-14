"""
Job Descriptions Configuration

Predefined job descriptions with required skills for different roles.
Add more job roles by following the same format.
"""

JOB_DESCRIPTIONS = {
    'Data Scientist': """
        We are looking for a Data Scientist with strong skills in Python, machine learning,
        and statistical analysis. Experience with TensorFlow, PyTorch, and scikit-learn is required.
        Must have expertise in data visualization using Tableau or Power BI. Knowledge of SQL,
        Pandas, and NumPy is essential. Cloud experience with AWS or Azure is a plus.
        Strong communication and problem-solving skills required.
    """,

    'Web Developer': """
        Seeking a Full Stack Web Developer proficient in JavaScript, React, and Node.js.
        Experience with HTML, CSS, and modern web frameworks (Angular or Vue) required.
        Must have strong database skills including MySQL and MongoDB. Familiarity with
        Git, Docker, and CI/CD pipelines. RESTful API development experience essential.
        Good teamwork and agile methodology experience preferred.
    """,

    'Java Developer': """
        Seeking a Java Developer with strong expertise in Java, Spring framework, and
        microservices architecture. Experience with SQL databases (Oracle, MySQL) and
        RESTful web services required. Knowledge of Git, Maven, and JUnit essential.
        Familiarity with Agile/Scrum methodologies. Good analytical and debugging skills.
        Cloud experience (AWS/Azure) is a plus.
    """,

    'HR Manager': """
        Looking for an experienced HR Manager with expertise in talent acquisition,
        employee relations, and performance management. Strong knowledge of compensation,
        benefits, and HR policies required. Experience with recruitment, training, and
        leadership development. Excellent communication, problem-solving, and organizational
        skills essential. HRIS and payroll management experience preferred.
    """,

    'Accountant': """
        Seeking a qualified Accountant with strong knowledge of accounting principles,
        financial analysis, and auditing. Experience with QuickBooks, SAP, or similar
        accounting software required. Must have expertise in budgeting, taxation, and
        financial reporting. Strong analytical skills and attention to detail essential.
        CPA certification or working towards it preferred.
    """,

    'Marketing Manager': """
        Looking for a Marketing Manager with expertise in digital marketing, SEO, and
        social media marketing. Experience with content marketing, branding, and marketing
        strategy development required. Knowledge of Google Analytics, advertising, and
        campaign management essential. Strong communication, creativity, and leadership
        skills needed. Experience with marketing automation tools is a plus.
    """,

    'DevOps Engineer': """
        Looking for a DevOps Engineer with expertise in AWS, Docker, and Kubernetes.
        Strong experience with CI/CD tools like Jenkins, GitLab CI, or CircleCI required.
        Knowledge of infrastructure as code using Terraform or Ansible essential.
        Scripting skills in Python or Bash. Experience with monitoring tools and
        containerization. Strong problem-solving and automation mindset needed.
    """
}

# Available job roles
AVAILABLE_ROLES = list(JOB_DESCRIPTIONS.keys())

# Default configuration
DEFAULT_CONFIG = {
    'skill_weight': 0.4,           # Weight for skill matching (40%)
    'similarity_weight': 0.6,       # Weight for text similarity (60%)
    'max_features': 500,            # Max features for TF-IDF
    'ngram_range': (1, 2),         # N-gram range for TF-IDF
    'top_n_candidates': 1000,      # Default number of top candidates to return
    'min_word_length': 2,          # Minimum word length for preprocessing
}
