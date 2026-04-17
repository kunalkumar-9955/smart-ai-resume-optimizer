import re
from collections import Counter
from io import BytesIO

import spacy
from docx import Document
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy.cli import download as spacy_download


def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        spacy_download("en_core_web_sm")
        return spacy.load("en_core_web_sm")


nlp = load_spacy_model()

CUSTOM_SKILLS = [
    "python",
    "machine learning",
    "deep learning",
    "data analysis",
    "data science",
    "nlp",
    "natural language processing",
    "computer vision",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "keras",
    "pytorch",
    "sql",
    "nosql",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "cloud",
    "api",
    "rest",
    "microservices",
    "javascript",
    "html",
    "css",
    "git",
    "agile",
    "scrum",
    "leadership",
    "project management",
    "problem solving",
    "communication",
    "teamwork",
    "presentation",
    "business analysis",
    "regression",
    "classification",
    "forecasting",
    "modeling",
    "feature engineering",
    "data visualization",
    "tableau",
    "power bi",
    "spark",
    "hadoop",
    "etl",
    "automation",
    "optimization",
    "sql server",
    "postgresql",
    "mongodb",
    "linux",
    "unix",
    "cicd",
]

SKILLS_DB = [
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "node.js",
    "express",
    "django",
    "flask",
    "fastapi",
    "sql",
    "postgresql",
    "mysql",
    "sqlite",
    "mongodb",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "linux",
    "bash",
    "powershell",
    "machine learning",
    "data science",
    "deep learning",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "data visualization",
    "tableau",
    "power bi",
    "spark",
    "hadoop",
    "etl",
    "rest api",
    "graphql",
    "ci/cd",
    "jenkins",
    "azure devops",
    "project management",
    "ui/ux",
]


def extract_text_from_pdf(file_bytes):
    pdf_reader = PdfReader(BytesIO(file_bytes))
    text = []
    for page in pdf_reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text)


def extract_text_from_docx(file_bytes):
    document = Document(BytesIO(file_bytes))
    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return "\n".join(text)


def extract_text_from_file(uploaded_file):
    uploaded_file.stream.seek(0)
    file_bytes = uploaded_file.read()
    filename = uploaded_file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    if filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    raise ValueError("Unsupported file type. Use PDF or DOCX.")


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9\s\.\-]+", " ", text)
    return text.strip()


def preprocess_text(text):
    cleaned = clean_text(text)
    doc = nlp(cleaned)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(tokens)


def extract_skills(text):
    cleaned = clean_text(text)
    found_skills = set()
    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, cleaned):
            found_skills.add(skill)
    return sorted(found_skills)


def enhance_jd(jd_text):
    if not jd_text or len(jd_text.split()) < 10:
        original = jd_text.strip()
        enhanced_lines = ["Enhanced Job Description:"]
        if original:
            enhanced_lines.append(f"Original description: {original}")
        enhanced_lines.extend([
            "",
            "Required Skills:",
            "- Python",
            "- SQL",
            "- Data analysis",
            "- Machine learning",
            "- AWS",
            "- Docker",
            "- Git",
            "- REST APIs",
            "",
            "Responsibilities:",
            "- Design and implement scalable software solutions.",
            "- Collaborate with cross-functional teams to deliver features.",
            "- Maintain and optimize data pipelines and services.",
            "- Translate business requirements into technical solutions.",
        ])
        return "\n".join(enhanced_lines)
    return jd_text


def extract_skills_and_keywords(text):
    text = text.lower()
    found_skills = []
    for skill in CUSTOM_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)
    return sorted(set(found_skills))


def compute_similarity_score(text_a, text_b):
    corpus = [text_a, text_b]
    vectorizer = TfidfVectorizer(max_features=500)
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return float(similarity_matrix[0][0])
    except Exception:
        return 0.0


def compute_resume_score(matched_skills, missing_skills, similarity_score):
    total_relevant = len(matched_skills) + len(missing_skills)
    if total_relevant == 0:
        return int(similarity_score * 100 * 0.8)

    skill_match_ratio = len(matched_skills) / total_relevant
    score = (skill_match_ratio * 0.6 + similarity_score * 0.4) * 100
    score = max(0, min(100, int(score)))
    return score


def build_suggestions(missing_skills, resume_text, job_description, resume_score):
    suggestions = []

    if resume_score < 50:
        suggestions.append(
            "Your resume can be better tailored to the job description. Add more relevant keywords and skills from the job listing."
        )

    if missing_skills:
        suggestions.append(
            "Add the following missing skills to your resume if you have experience with them: "
            + ", ".join(missing_skills[:10])
        )

    if len(resume_text.split()) < 120:
        suggestions.append(
            "Your resume text is short; consider expanding descriptions of your projects, tools, and outcomes."
        )

    if "summary" not in resume_text.lower() and resume_score < 70:
        suggestions.append(
            "Add a concise professional summary at the top of your resume to clearly state your strengths and expertise."
        )

    if "project" not in resume_text.lower() and "experience" in job_description.lower():
        suggestions.append(
            "Include at least one project or accomplishment statement that demonstrates your experience."
        )

    if not suggestions:
        suggestions.append(
            "Your resume looks aligned. Keep refining with real examples and measurable results."
        )

    return suggestions


def rewrite_resume_statement(statement):
    """Turn a weak resume line into a stronger professional statement."""
    statement = statement.strip()
    replacements = {
        "i worked on": "Developed",
        "worked on": "Delivered",
        "i managed": "Led",
        "i created": "Built",
        "i did": "Executed",
        "i assisted": "Supported",
        "i helped": "Collaborated",
        "responsible for": "Owned",
        "helped": "Collaborated",
    }
    lower = statement.lower()
    for keyword, phrase in replacements.items():
        if keyword in lower:
            return re.sub(re.escape(keyword), phrase, statement, flags=re.IGNORECASE)
    if len(statement.split()) <= 6:
        return f"Improved {statement.lower()} with measurable results."
    return statement


def improve_resume_text(resume_text):
    """Generate a small set of rewritten resume suggestions."""
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    suggestions = []
    for line in lines[:6]:
        if len(line.split()) < 12:
            suggestions.append(rewrite_resume_statement(line))
    return suggestions or ["Resume language is already strong and concise."]


def compute_keyword_density(text, skills):
    """Count how often each skill appears in resume text."""
    cleaned = clean_text(text)
    density = {}
    for skill in sorted(set(skills)):
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        density[skill] = len(re.findall(pattern, cleaned))
    return density


def detect_resume_sections(text):
    """Detect main resume sections and identify which ones are missing."""
    lower = text.lower()
    sections = {
        "Education": any(keyword in lower for keyword in ["education", "degree", "university", "bachelor", "master"]),
        "Skills": any(keyword in lower for keyword in ["skills", "technical skills", "technologies"]),
        "Projects": any(keyword in lower for keyword in ["project", "projects", "portfolio"]),
        "Experience": any(keyword in lower for keyword in ["experience", "work history", "professional experience"]),
    }
    missing = [name for name, present in sections.items() if not present]
    return {"sections": sections, "missing_sections": missing}


def predict_job_roles(skills, jd_text=""):
    """Predict likely roles based on job description text and resume skills."""
    if jd_text:
        jd_lower = jd_text.lower()
        jd_role_map = {
            "Web Developer": [
                "web developer",
                "frontend developer",
                "backend developer",
                "full stack developer",
                "full-stack developer",
                "web dev",
            ],
            "Data Analyst": [
                "data analyst",
                "business analyst",
                "analytics engineer",
            ],
            "Data Scientist": [
                "data scientist",
                "machine learning scientist",
                "ml scientist",
            ],
            "ML Engineer": [
                "ml engineer",
                "machine learning engineer",
                "machine learning developer",
            ],
            "DevOps Engineer": [
                "devops engineer",
                "site reliability engineer",
                "sre",
            ],
            "Product Manager": [
                "product manager",
                "product owner",
                "growth manager",
            ],
        }
        for role, aliases in jd_role_map.items():
            if any(alias in jd_lower for alias in aliases):
                return [role]

    role_map = {
        "Data Analyst": {
            "sql", "excel", "tableau", "power bi", "data analysis", "pandas", "numpy", "business intelligence", "data visualization"
        },
        "Data Scientist": {
            "python", "machine learning", "deep learning", "pandas", "numpy", "tensorflow", "pytorch", "scikit-learn", "data science", "statistics"
        },
        "ML Engineer": {
            "python", "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "aws", "docker", "model deployment"
        },
        "Web Developer": {
            "javascript", "html", "css", "react", "angular", "vue", "node.js", "nodejs", "express", "django", "flask", "web development"
        },
        "DevOps Engineer": {
            "docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "jenkins", "azure devops", "terraform", "infrastructure"
        },
        "Product Manager": {
            "product management", "roadmap", "stakeholder", "agile", "scrum", "user research", "business analysis"
        },
    }
    normalized = {skill.lower() for skill in skills}

    scored_roles = []
    for role, role_skills in role_map.items():
        score = len(normalized.intersection(role_skills))
        if score > 0:
            scored_roles.append((score, role, len(role_skills)))

    if not scored_roles:
        return ["General Software Professional"]

    # Prefer roles with highest overlap, then higher percentage of matched role keywords.
    scored_roles.sort(key=lambda item: (item[0], item[0] / item[2]), reverse=True)
    top_score = scored_roles[0][0]
    recommendations = [role for score, role, _ in scored_roles if score == top_score]
    return recommendations


def build_ideal_candidate_skills(jd_skills):
    """Build an ideal skill set for the job description."""
    ideal_skills = set(jd_skills)
    priority_skills = {"communication", "project management", "teamwork", "python", "sql"}
    return sorted(ideal_skills.union(priority_skills))


def compare_with_ideal(resume_skills, ideal_skills):
    """Compare resume skills against an ideal candidate skill set."""
    resume_set = {skill.lower() for skill in resume_skills}
    ideal_set = {skill.lower() for skill in ideal_skills}
    missing = sorted(ideal_set.difference(resume_set))
    return sorted(ideal_skills), missing


def generate_smart_suggestions(missing_skills, role_predictions, section_report):
    """Create human-like suggestions based on missing skills and sections."""
    suggestions = []
    if missing_skills:
        suggestions.append(
            "Add missing skills such as " + ", ".join(missing_skills[:5]) + " to align better with the job." 
        )
    if section_report["missing_sections"]:
        suggestions.append(
            "Include the following sections to strengthen your resume: "
            + ", ".join(section_report["missing_sections"]) + "."
        )
    suggestions.append(
        "Consider emphasizing roles like " + ", ".join(role_predictions[:2]) + " based on your technical strengths."
    )
    return suggestions


def compute_score_breakdown(matched_skills, missing_skills, keyword_density, section_report):
    """Return a breakdown of the resume score components."""
    skills_score = int(min(100, len(matched_skills) * 12 + 10))
    density_score = int(min(100, sum(min(count, 3) for count in keyword_density.values()) * 8))
    section_score = int(max(0, 100 - len(section_report["missing_sections"]) * 18))
    overall_score = int((skills_score * 0.4) + (density_score * 0.3) + (section_score * 0.3))
    return {
        "skills_score": skills_score,
        "keyword_density_score": density_score,
        "section_score": section_score,
        "overall_score": overall_score,
    }


def optimize_resume_text(resume_text, missing_skills):
    """Generate an optimized resume draft by adding missing keywords and improving phrasing."""
    rewritten = improve_resume_text(resume_text)
    appended_skills = ", ".join(missing_skills[:6])
    optimization_note = "\n\nOptimized keywords added: " + appended_skills if appended_skills else ""
    return "\n".join(rewritten) + optimization_note
