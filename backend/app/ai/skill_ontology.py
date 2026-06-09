"""
Skill Ontology — canonical skill names mapped to common aliases/variants.
Used by the SkillExtractor for accurate, normalized skill identification.
"""

SKILL_ONTOLOGY: dict[str, list[str]] = {
    # Programming Languages
    "Python": ["python", "py", "python3"],
    "JavaScript": ["javascript", "js", "ecmascript"],
    "TypeScript": ["typescript", "ts"],
    "Java": ["java", "jdk"],
    "C++": ["c++", "cpp", "cplusplus"],
    "C#": ["c#", "csharp", "c sharp"],
    "Go": ["go", "golang"],
    "Rust": ["rust", "rustlang"],
    "Ruby": ["ruby", "rb"],
    "PHP": ["php"],
    "Swift": ["swift"],
    "Kotlin": ["kotlin", "kt"],
    "R": ["r", "r language", "rlang"],
    "Scala": ["scala"],
    "SQL": ["sql", "structured query language"],

    # Web Frameworks
    "React": ["react", "reactjs", "react.js"],
    "Next.js": ["next.js", "nextjs", "next"],
    "Angular": ["angular", "angularjs"],
    "Vue.js": ["vue", "vuejs", "vue.js"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi", "fast api"],
    "Express.js": ["express", "expressjs", "express.js"],
    "Spring Boot": ["spring boot", "springboot", "spring"],
    "Node.js": ["node.js", "nodejs", "node"],
    "Ruby on Rails": ["rails", "ruby on rails", "ror"],

    # Databases
    "PostgreSQL": ["postgresql", "postgres", "psql", "pg"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"],
    "SQLite": ["sqlite"],
    "Elasticsearch": ["elasticsearch", "elastic"],
    "DynamoDB": ["dynamodb", "dynamo"],

    # Cloud & DevOps
    "AWS": ["aws", "amazon web services"],
    "Google Cloud": ["gcp", "google cloud", "google cloud platform"],
    "Azure": ["azure", "microsoft azure"],
    "Docker": ["docker", "containerization"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Terraform": ["terraform", "tf"],
    "CI/CD": ["ci/cd", "cicd", "continuous integration", "continuous deployment"],
    "Jenkins": ["jenkins"],
    "GitHub Actions": ["github actions", "gh actions"],
    "Linux": ["linux", "unix"],
    "Nginx": ["nginx"],

    # AI / ML / Data
    "Machine Learning": ["ml", "machine learning"],
    "Deep Learning": ["dl", "deep learning"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "Scikit-learn": ["sklearn", "scikit-learn", "scikit learn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy", "np"],
    "OpenCV": ["opencv", "cv2"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision", "cv"],
    "Data Science": ["data science", "ds"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Statistics": ["statistics", "stats"],
    "Matplotlib": ["matplotlib", "plt"],
    "Tableau": ["tableau"],
    "Power BI": ["power bi", "powerbi"],
    "Apache Spark": ["spark", "apache spark", "pyspark"],
    "Hadoop": ["hadoop"],

    # Tools & Misc
    "Git": ["git", "version control"],
    "GitHub": ["github", "gh"],
    "REST API": ["rest", "rest api", "restful"],
    "GraphQL": ["graphql", "gql"],
    "gRPC": ["grpc"],
    "Agile": ["agile", "scrum"],
    "Jira": ["jira"],
    "Figma": ["figma"],
    "Postman": ["postman"],

    # Soft Skills (relevant for placement readiness)
    "Communication": ["communication", "communication skills"],
    "Leadership": ["leadership", "team lead"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Teamwork": ["teamwork", "collaboration", "team player"],
}


def get_canonical_skill(term: str) -> str | None:
    """Look up a term and return the canonical skill name, or None."""
    term_lower = term.lower().strip()
    for canonical, aliases in SKILL_ONTOLOGY.items():
        if term_lower in aliases or term_lower == canonical.lower():
            return canonical
    return None


def get_all_skill_names() -> list[str]:
    """Return all canonical skill names."""
    return list(SKILL_ONTOLOGY.keys())
