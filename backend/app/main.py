from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from pydantic import BaseModel
import re


SKILLS = [
    "Python",
    "JavaScript",   
    "Java",
    "C++",      
    "SQL",
    "mySQL",
    "postgreSQL",
    "mongoDB",
    "fastAPI",
    "pandas",
    "numpy",
    "git",
    "github",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Django",
    "Flask",
    "Machine Learning",
    "Data Analysis",
    "Data Visualization",
    "AWS",
    "Docker",
]
PROJECT_CATEGORIES = {
    "AI/ML": [
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "nlp",
        "natural language processing",
        "computer vision",
        "neural network",
        "neural networks",
        "generative ai",
        "gen ai",
        "llm",
        "large language model",
        "transformers"
    ],

    "Data Analytics": [
        "data analysis",
        "data analytics",
        "data visualization",
        "statistics",
        "data cleaning",
        "data preprocessing"
    ],
    "Data Engineering": [
        "data engineering",
        "data pipeline",
        "data pipelines",
        "etl",
        "extract transform load",
        "data extraction",
        "data transformation",
        "data cleaning",
        "data validation",
        "data processing",
        "batch processing",
        "real-time data",
        "real time data",
        "streaming data",
        "streaming data",
        "data warehouse",
        "data warehousing",
        "star schema",
        "snowflake schema",
        "fact table",
        "fact tables",
        "dimension table",
        "dimension tables",
        "data lake",
        "oltp",
        "olap"
    ],

    "Web Development": [
        "web development",
        "rest api",
        "api development",
        "frontend",
        "backend",
        "full stack",
        "web application"
    ],

    "Cybersecurity": [
        "cybersecurity",
        "cyber security",
        "network security",
        "ethical hacking",
        "penetration testing",
        "penetration test",
        "osint",
        "siem",
        "vulnerability assessment",
        "malware analysis",
        "digital forensics",
        "cryptography",
        "intrusion detection",
        "firewall",
        "security auditing",
        "security assessment",
        "incident response"
    ],
    "Cloud/DevOps": [
        "cloud computing",
        "cloud deployment",
        "cloud infrastructure",
        "devops",
        "continuous integration",
        "continuous deployment",
        "ci/cd",
        "infrastructure as code",
        "cloud architecture"
    ],
    "Database": [
        "database",
        "database management",
        "database design",
        "relational database",
        "relational databases",
        "database normalization",
        "database indexing",
        "data modeling",
        "data warehouse",
        "data warehousing",
        "nosql database"
    ]
}

class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str


def extract_skills(text):
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills

def extract_experience_requirement(job_description):
    text = job_description.lower()

    result = {
        "minimum_years": None,
        "maximum_years": None,
        "requirement_type": "Not specified",
        "fresher_eligible": None
    }

    if (
        "fresher" in text
        or "fresh graduate" in text
        or "fresh graduates" in text
        or "entry level" in text
    ):
        result["fresher_eligible"] = True

    range_match = re.search(
        r'(\d+)\s*[-–]\s*(\d+)\s*(?:years?|yrs?)',
        text
    )

    if range_match:
        result["minimum_years"] = int(range_match.group(1))
        result["maximum_years"] = int(range_match.group(2))

        if result["minimum_years"] == 0:
            result["fresher_eligible"] = True

        result["requirement_type"] = "Required"

    plus_match = re.search(
        r'(\d+)\s*\+\s*(?:years?|yrs?)',
        text
    )

    if plus_match and result["minimum_years"] is None:
        result["minimum_years"] = int(plus_match.group(1))

    if "preferred" in text or "preferably" in text:
        result["requirement_type"] = "Preferred"

    if (
        "required" in text
        or "minimum" in text
        or "must have" in text
    ):
        result["requirement_type"] = "Required"

    return result

def extract_resume_experience(resume_text):
    text = resume_text.lower()

    experience_matches = re.search(
        r'(\d+)\+?\s*(years?|yrs?)\s*(of\s*)?experience',
        text
    )

    if experience_matches:
        return int(experience_matches.group(1))

    return 0

def suggest_career_path(skills, project_categories=None):
    career_scores = {}

    for career, required_skills in CAREER_PATHS.items():
        score = 0

        for skill in required_skills:
            if skill in skills:
                score += 1

        if project_categories and career in CAREER_CATEGORY_MAP:
            career_category = CAREER_CATEGORY_MAP[career]

            if career_category in project_categories:
                score += 3

        career_scores[career] = score

    best_career = max(career_scores, key=career_scores.get)

    return best_career

def get_career_scores(skills, project_categories=None):
    career_scores = {}

    for career, required_skills in CAREER_PATHS.items():
        score = 0

        for skill in required_skills:
            if skill in skills:
                score += 1

        if project_categories and career in CAREER_CATEGORY_MAP:
            career_category = CAREER_CATEGORY_MAP[career]

            if career_category in project_categories:
                score += 3

        max_score = len(required_skills) + 3

        percentage = round((score / max_score) * 100)

        career_scores[career] = percentage

    career_scores = dict(
        sorted(
            career_scores.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    return career_scores

def get_career_reason(career, skills, project_categories):
    matched_skills = []

    for skill in CAREER_PATHS[career]:
        if skill in skills:
            matched_skills.append(skill)

    reasons = []

    if matched_skills:
        reasons.append("skills in " + ", ".join(matched_skills))

    if career in CAREER_CATEGORY_MAP:
        career_category = CAREER_CATEGORY_MAP[career]

    if career_category in project_categories:
        reasons.append("projects related to " + career_category)

    if reasons:
        return "Your resume shows relevant " + " and ".join(reasons) + "."

    return "Your resume has some relevant skills for this career path."

def extract_project_categories(text):
    text_lower = text.lower()

    found_categories = []

    for category, keywords in PROJECT_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                found_categories.append(category)
                break

    return found_categories

PROJECT_COMPLEXITY_KEYWORDS = [
    "api",
    "etl",
    "pipeline",
    "real-time",
    "streaming",
    "database",
    "cloud",
    "deployment",
    "authentication",
    "machine learning",
    "deep learning",
    "data warehouse",
    "kafka",
    "spark"
]

class project_categories:
    def __init__(self, category_map=None):
        self.category_map = category_map or PROJECT_CATEGORIES

    def extract_categories(self, text):
        if not text:
            return []

        text_lower = text.lower()
        found_categories = []

        for category, keywords in self.category_map.items():
            if any(keyword.lower() in text_lower for keyword in keywords):
                found_categories.append(category)

        return found_categories

    def get_category_keywords(self, category):
        return list(self.category_map.get(category, []))

    def classify_project(self, text):
        categories = self.extract_categories(text)
        return categories if categories else ["General"]


def extract_individual_projects(project_text):
    projects = []

    lines = project_text.splitlines()

    current_project = None

    for line in lines:
        line = line.strip()

        if re.match(r'^\s*\d+[.)]\s+', line):
            if current_project:
                projects.append(current_project)

            project_name = re.sub(r'^\d+\.\s+', '', line)
            current_project = {
                "name": project_name,
                "text": line
            }

        elif current_project:
            current_project["text"] += " " + line

    if current_project:
        projects.append(current_project)

    return projects

def extract_projects_section(text):
    project_headings = [
        "projects",
        "academic projects",
        "personal projects",
        "project experience",
        "projects & research",
        "projects and research"
    ]

    start = -1
    for heading in project_headings:
        match = re.search(r'(?im)^\s*' + re.escape(heading) + r'\s*$', text)
        if match:
            start = match.start()
            break

    if start == -1:
        return ""

    project_text = text[start:]

    end_headings = [
        "certifications",
        "education",
        "technical skills",
        "skills",
        "experience",
        "soft skills",
        "achievements",
        "additional information"
    ]

    end_positions = []
    for heading in end_headings:
        position = project_text.lower().find(heading, len("projects"))
        if position != -1:
            end_positions.append(position)

    if end_positions:
        project_text = project_text[:min(end_positions)]

    return project_text

app = FastAPI(
    title="AI Resume Analyzer",
    description="AI-Powered Resume Analysis & Career Intelligence System",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer API is running!"
    }

@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()

    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)

    reader = PdfReader("temp_resume.pdf")

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    text_lower = text.lower()
    experience_years = 0
    experience_matches = re.search(r'(\d+)\+?\s*(years|year)\s*(of\s*)?experience',text_lower)

    if experience_matches:
       experience_years = int(experience_matches.group(1))


    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    project_text = extract_projects_section(text)
    project_categories = extract_project_categories(project_text)
    career_path = suggest_career_path(found_skills,project_categories)
    career_scores = get_career_scores(found_skills, project_categories)
    top_careers = list(career_scores.items())[:3] 
    other_careers = list(career_scores.items())[3:]
    projects = extract_individual_projects(project_text)
    career_reason = get_career_reason(career_path, found_skills, project_categories) 

    for project in projects:
        project["categories"] = extract_project_categories(project["text"])
        project["skills"] = extract_skills(project["text"])
        project["complexity_features"] = [] 

        for keyword in PROJECT_COMPLEXITY_KEYWORDS:
            if keyword.lower() in project["text"].lower():
                project["complexity_features"].append(keyword)

        project["score"]=min(len(project["skills"]) * 5 + len(project["categories"]) * 10 + len(project["complexity_features"]) * 3, 100)
        if project["score"] <= 30:
                project["level"] = "Beginner"
        elif project["score"] <= 60:
                project["level"] = "Intermediate"   
        elif project["score"] <= 80:
                project["level"] = "Advanced"
        else:
                project["level"] = "Expert"            

    skills_score = min(len(found_skills) * 5, 40)
    score = skills_score

    education_score = 0

    if "phd" in text_lower or "doctorate" in text_lower:
       education_score = 15

    elif "master" in text_lower or "m.tech" in text_lower or "mba" in text_lower:
      education_score = 15

    elif "bachelor" in text_lower or "b.tech" in text_lower or "b.e." in text_lower:
       education_score = 15

    elif "associate" in text_lower or "a.a." in text_lower:
       education_score = 10

    elif "degree" in text_lower:
       education_score = 10

    score += education_score

    project_score = 0

    if "project" in text_lower:
      project_score = 15

    score += project_score

    experience_score = 0

    if experience_years >= 5:
      experience_score = 15
    elif experience_years >= 3:
      experience_score = 12
    elif experience_years >= 2:
      experience_score = 10
    elif experience_years >= 1:
      experience_score = 8
    elif "internship" in text_lower:
      experience_score = 5

    score += experience_score



    suggestions = []

    if len(found_skills) < 5:
        suggestions.append("Add more relevant technical skills.")

    if "project" not in text_lower:
        suggestions.append("Add a Projects section.")

    if "experience" not in text_lower and "internship" not in text_lower:
        suggestions.append("Add internship or work experience if available.")

    if "education" not in text_lower:
        suggestions.append("Add an Education section.")

    return {
        "filename": file.filename,

        "skills": found_skills,

        "project_categories": project_categories,

        "projects": projects,

        "project_count": len(projects),

    "experience_years": experience_years,

    "total_score": score,

    "top_careers": [
        {
            "rank": index + 1,
            "career": career,
            "score": f"{percentage}%",
            "reason": get_career_reason(
                career,
                found_skills,
                project_categories
            )
        }
        for index, (career, percentage) in enumerate(top_careers)
    ],

    "other_careers": [
        {
            "rank": index + 4,
            "career": career,
            "score": f"{percentage}%",
            "reason": get_career_reason(
                career,
                found_skills,
                project_categories
            )
        }
        for index, (career, percentage) in enumerate(other_careers)
    ],

    "suggestions": suggestions
}


CAREER_PATHS = {
    "Data Engineer": [
        "Python",
        "SQL",
        "Data Engineering",
        "Apache Spark",
        "PySpark",
        "AWS"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Data Analysis",
        "Data Visualization",
        "Pandas",
        "Excel"
    ],

    "AI/ML Engineer": [
        "Python",
        "Machine Learning",
        "Data Analysis",
        "NumPy",
        "Pandas",
        "Deep Learning"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Django",
        "Flask"
    ],

    "Cybersecurity Analyst": [
        "Cybersecurity",
        "Network Security",
        "OSINT",
        "Digital Forensics",
        "Ethical Hacking",
        "SIEM"
    ],

    "Cloud/DevOps Engineer": [
        "AWS",
        "Docker",
        "Git",
        "Linux",
        "Cloud Computing",
        "DevOps",
        "CI/CD"
    ],

    "Database Administrator": [
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Database",
        "Database Management",
        "Database Design"
    ]
}

CAREER_CATEGORY_MAP = {
    "Data Engineer": "Data Engineering",
    "Data Analyst": "Data Analytics",
    "AI/ML Engineer": "AI/ML",
    "Web Developer": "Web Development",
    "Cybersecurity Analyst": "Cybersecurity",
    "Cloud/DevOps Engineer": "Cloud/DevOps",
    "Database Administrator": "Database"
   }


@app.post("/job/match")
def match_job(data: JobMatchRequest):

    resume_skills = extract_skills(data.resume_text)
    job_skills = extract_skills(data.job_description)
    experience_analysis = extract_experience_requirement(data.job_description)
    candidate_experience = extract_resume_experience(data.resume_text)
    if experience_analysis["minimum_years"] is None:
      experience_status = "Experience requirement not specified"
    elif experience_analysis["fresher_eligible"] is True:
      experience_status = "Fresher eligible"
    elif candidate_experience < experience_analysis["minimum_years"]:
     if experience_analysis["requirement_type"] == "Preferred":
        experience_status = "Experience preferred but requirement not met"
     else:
        experience_status = "Does not meet stated experience requirement"
    else:
     experience_status = "Meets stated experience requirement"

    matched_skills = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
    missing_skills = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)
    if missing_skills:
         recommendations = "focus on learning: " + ", ".join(missing_skills)
    else:
        recommendations = "Your skills match all required skills."


    if len(job_skills) > 0:
        match_percentage = (len(matched_skills) / len(job_skills)) * 100
    else:
        match_percentage = 0
    if match_percentage >= 80:
        match_level = "Excellent Match"
    elif match_percentage >= 60:
        match_level = "Good Match"      
    elif match_percentage >= 40:
        match_level = "Moderate Match"
    else:
        match_level = "Poor Match"                

    return {
        "resume_skills": resume_skills,
        "required_skills": job_skills,
        "experience_analysis": experience_analysis,
        "candidate_experience": candidate_experience,
        "experience_status": experience_status,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": round(match_percentage, 2),
        "match_level": match_level,
        "recommendations": recommendations,  
    }