"""
Skill Categories - Categorize skills into domains for better organization and matching.
"""

SKILL_CATEGORIES = {
    # Programming Languages
    "Programming Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C", "C#", "Go", "Rust",
        "PHP", "Ruby", "Swift", "Kotlin", "R", "MATLAB", "Scala", "Perl", "Haskell",
        "Elixir", "Dart", "Lua", "Julia", "Clojure", "Objective-C", "Assembly",
        "Shell", "PowerShell", "Groovy", "F#", "Solidity"
    ],
    
    # Frontend Development
    "Frontend": [
        "React", "Angular", "Vue.js", "Svelte", "Solid.js", "Preact", "Ember.js",
        "Backbone.js", "Alpine.js", "Lit", "Qwik", "Astro", "htmx", "HTML", "CSS",
        "Sass", "Less", "Tailwind CSS", "Bootstrap", "Material UI", "Chakra UI",
        "Ant Design", "Styled Components", "Emotion", "CSS Modules", "PostCSS"
    ],
    
    # Backend Development
    "Backend": [
        "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring", "ASP.NET",
        "Next.js", "Nuxt.js", "Remix", "Nest.js", "Koa", "Hapi", "Laravel",
        "Symfony", "Ruby on Rails", "Sinatra", "Gin", "Echo", "Fiber", "Actix",
        "Rocket", "Ktor", "Quarkus", "Micronaut"
    ],
    
    # Database & Data Storage
    "Database": [
        "PostgreSQL", "MySQL", "SQLite", "Oracle", "SQL Server", "SQL", "MariaDB",
        "CockroachDB", "PlanetScale", "Supabase", "MongoDB", "Redis", "Cassandra",
        "DynamoDB", "Couchbase", "CouchDB", "Neo4j", "ArangoDB", "RethinkDB",
        "Firebase", "Elasticsearch", "Solr"
    ],
    
    # ORM & Query Builders
    "ORM": [
        "Prisma", "TypeORM", "Sequelize", "Mongoose", "SQLAlchemy", "Hibernate",
        "JPA", "Doctrine", "ActiveRecord", "Drizzle", "Knex.js"
    ],
    
    # Cloud Platforms
    "Cloud": [
        "AWS", "Azure", "GCP", "Digital Ocean", "Heroku", "Netlify", "Vercel",
        "Railway", "Render", "Fly.io", "Cloudflare", "Linode", "EC2", "S3",
        "Lambda", "RDS", "CloudFront", "ECS", "EKS", "API Gateway", "CloudWatch",
        "SNS", "SQS"
    ],
    
    # DevOps & Infrastructure
    "DevOps": [
        "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "GitHub Actions",
        "GitLab CI", "CircleCI", "Travis CI", "ArgoCD", "Helm", "Vagrant", "Puppet",
        "Chef", "Prometheus", "Grafana", "Datadog", "New Relic", "Nginx", "Apache"
    ],
    
    # Testing & QA
    "Testing": [
        "Jest", "Vitest", "Mocha", "Chai", "Jasmine", "Cypress", "Playwright",
        "Selenium", "Puppeteer", "Testing Library", "PyTest", "JUnit", "TestNG",
        "Mockito", "RSpec", "Enzyme"
    ],
    
    # Mobile Development
    "Mobile": [
        "React Native", "Flutter", "SwiftUI", "Jetpack Compose", "Xamarin", "Ionic",
        "Cordova", "Expo", "Capacitor"
    ],
    
    # Machine Learning & AI
    "Machine Learning": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras",
        "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly",
        "Jupyter", "NLP", "Computer Vision", "Data Analysis", "Statistics",
        "LangChain", "Hugging Face", "YOLO", "OpenCV", "SpaCy", "NLTK", "XGBoost",
        "LightGBM", "Apache Spark", "Tableau", "Power BI"
    ],
    
    # Version Control
    "Version Control": [
        "Git", "GitHub", "GitLab", "Bitbucket", "Mercurial", "SVN"
    ],
    
    # Project Management
    "Project Management": [
        "Jira", "Confluence", "Trello", "Asana", "Monday.com", "Notion", "Slack",
        "Discord", "Microsoft Teams"
    ],
    
    # Design & UI/UX
    "Design": [
        "Figma", "Sketch", "Adobe XD", "InVision", "Framer", "Zeplin", "Photoshop",
        "Illustrator"
    ],
    
    # API & Integration
    "API": [
        "REST API", "GraphQL", "gRPC", "WebSocket", "tRPC", "Postman", "Insomnia",
        "Swagger", "Axios", "Fetch API"
    ],
    
    # Architecture & Patterns
    "Architecture": [
        "Microservices", "Monolith", "Serverless", "Event-Driven", "CQRS",
        "Domain-Driven Design", "Clean Architecture", "MVC", "MVVM"
    ],
    
    # Security
    "Security": [
        "OAuth", "JWT", "SSL/TLS", "OWASP", "Penetration Testing", "Cryptography"
    ],
    
    # Methodologies
    "Methodologies": [
        "Agile", "Scrum", "Kanban", "DevOps", "CI/CD", "TDD", "BDD",
        "Pair Programming", "Code Review"
    ],
    
    # Operating Systems
    "Operating Systems": [
        "Linux", "Ubuntu", "Debian", "CentOS", "Red Hat", "macOS", "Windows",
        "Windows Server"
    ],
    
    # Blockchain & Web3
    "Blockchain": [
        "Blockchain", "Ethereum", "Web3.js", "Ethers.js", "Hardhat", "Truffle"
    ],
    
    # Build Tools
    "Build Tools": [
        "Webpack", "Vite", "Rollup", "Parcel", "esbuild", "Turbopack", "Gulp",
        "Grunt", "Babel", "SWC"
    ],
    
    # Package Managers
    "Package Managers": [
        "npm", "Yarn", "pnpm", "pip", "Poetry", "Composer", "Maven", "Gradle", "Cargo"
    ]
}


def get_skill_category(skill_name: str) -> str | None:
    """
    Get the category for a given skill.
    
    Args:
        skill_name: Name of the skill
        
    Returns:
        Category name or None if not found
    """
    for category, skills in SKILL_CATEGORIES.items():
        if skill_name in skills:
            return category
    return "Other"


def categorize_skills(skills: list[str]) -> dict[str, list[str]]:
    """
    Categorize a list of skills into their respective domains.
    
    Args:
        skills: List of skill names
        
    Returns:
        Dictionary mapping category names to list of skills
    """
    categorized = {}
    
    for skill in skills:
        category = get_skill_category(skill)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(skill)
    
    return categorized


def get_primary_domain(skills: list[str]) -> str:
    """
    Determine the primary domain based on skill distribution.
    
    Args:
        skills: List of skill names
        
    Returns:
        Primary domain/category name
    """
    if not skills:
        return "General"
    
    categorized = categorize_skills(skills)
    
    # Find category with most skills
    primary = max(categorized.items(), key=lambda x: len(x[1]))
    return primary[0]
