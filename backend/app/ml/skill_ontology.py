"""
Skill Ontology - Comprehensive mapping of 200+ skills to their variations and aliases.
Used for extracting skills from resume text.
"""

SKILL_ONTOLOGY = {
    # Programming Languages (Extended)
    "Python": ["python", "py", "python3", "python2", "python 3", "python 2"],
    "JavaScript": ["javascript", "js", "ecmascript", "es6", "es2015", "es2016", "es2017", "es2018", "es2019", "es2020", "es2021", "vanilla js"],
    "TypeScript": ["typescript", "ts", "type script"],
    "Java": ["java", "java se", "java ee", "j2ee", "java 8", "java 11", "java 17", "java 21"],
    "C++": ["c++", "cpp", "cplusplus", "c plus plus"],
    "C": ["c language", "c programming", "ansi c"],
    "C#": ["c#", "csharp", "c sharp", ".net"],
    "Go": ["golang", "go lang", "go language"],
    "Rust": ["rust", "rust lang", "rust language"],
    "PHP": ["php", "php5", "php7", "php8", "php 5", "php 7", "php 8"],
    "Ruby": ["ruby", "ruby on rails", "ror", "rails"],
    "Swift": ["swift", "swift ui", "swiftui", "swift 5"],
    "Kotlin": ["kotlin", "kotlin jvm", "kotlin native"],
    "R": ["r language", "r programming", "r stats"],
    "MATLAB": ["matlab", "octave"],
    "Scala": ["scala"],
    "Perl": ["perl", "perl 5"],
    "Haskell": ["haskell"],
    "Elixir": ["elixir", "phoenix"],
    "Dart": ["dart", "dart lang"],
    "Lua": ["lua"],
    "Julia": ["julia", "julia lang"],
    "Clojure": ["clojure", "clojurescript"],
    "Objective-C": ["objective-c", "objective c", "objc"],
    "Assembly": ["assembly", "asm", "x86", "arm assembly"],
    "Shell": ["shell", "bash", "zsh", "shell script", "bash script"],
    "PowerShell": ["powershell", "pwsh", "windows powershell"],
    "Groovy": ["groovy"],
    "F#": ["f#", "fsharp", "f sharp"],
    "Solidity": ["solidity", "ethereum", "smart contracts"],
    
    # Frontend Frameworks & Libraries
    "React": ["react", "reactjs", "react.js", "react js", "react 16", "react 17", "react 18"],
    "Angular": ["angular", "angularjs", "angular.js", "angular 2", "angular 12", "angular 14"],
    "Vue.js": ["vue", "vuejs", "vue.js", "vue js", "vue 2", "vue 3"],
    "Svelte": ["svelte", "sveltejs", "sveltekit"],
    "Solid.js": ["solid", "solidjs", "solid.js"],
    "Preact": ["preact"],
    "Ember.js": ["ember", "emberjs", "ember.js"],
    "Backbone.js": ["backbone", "backbonejs", "backbone.js"],
    "Alpine.js": ["alpine", "alpinejs", "alpine.js"],
    "Lit": ["lit", "lit-element", "lit-html"],
    "Qwik": ["qwik", "qwik city"],
    "Astro": ["astro", "astrojs"],
    "htmx": ["htmx"],
    
    # Backend Frameworks
    "Node.js": ["node", "nodejs", "node.js", "node js"],
    "Express": ["express", "expressjs", "express.js"],
    "Django": ["django", "django rest", "drf"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi", "fast api"],
    "Spring": ["spring", "spring boot", "spring framework", "spring mvc"],
    "ASP.NET": ["asp.net", "asp net", "aspnet", "asp.net core"],
    "Next.js": ["nextjs", "next.js", "next js", "next 13", "next 14"],
    "Nuxt.js": ["nuxt", "nuxtjs", "nuxt.js", "nuxt 3"],
    "Remix": ["remix", "remix run"],
    "Nest.js": ["nest", "nestjs", "nest.js"],
    "Koa": ["koa", "koajs"],
    "Hapi": ["hapi", "hapijs", "hapi.js"],
    "Laravel": ["laravel"],
    "Symfony": ["symfony"],
    "Ruby on Rails": ["ruby on rails", "rails", "ror"],
    "Sinatra": ["sinatra"],
    "Gin": ["gin", "gin gonic"],
    "Echo": ["echo", "echo framework"],
    "Fiber": ["fiber", "go fiber"],
    "Actix": ["actix", "actix-web"],
    "Rocket": ["rocket", "rocket.rs"],
    "Ktor": ["ktor"],
    "Quarkus": ["quarkus"],
    "Micronaut": ["micronaut"],
    
    # CSS & Styling
    "HTML": ["html", "html5", "html 5"],
    "CSS": ["css", "css3", "css 3"],
    "Sass": ["sass", "scss"],
    "Less": ["less", "lesscss"],
    "Tailwind CSS": ["tailwind", "tailwindcss", "tailwind css"],
    "Bootstrap": ["bootstrap", "bootstrap 4", "bootstrap 5"],
    "Material UI": ["material ui", "mui", "material-ui"],
    "Chakra UI": ["chakra", "chakra ui", "chakra-ui"],
    "Ant Design": ["ant design", "antd"],
    "Styled Components": ["styled components", "styled-components"],
    "Emotion": ["emotion", "emotion css"],
    "CSS Modules": ["css modules"],
    "PostCSS": ["postcss", "post css"],
    
    # Databases - SQL
    "PostgreSQL": ["postgresql", "postgres", "psql", "pg"],
    "MySQL": ["mysql", "mariadb"],
    "SQLite": ["sqlite", "sqlite3"],
    "Oracle": ["oracle", "oracle db", "oracle database"],
    "SQL Server": ["sql server", "mssql", "microsoft sql", "ms sql"],
    "SQL": ["sql", "structured query language"],
    "MariaDB": ["mariadb"],
    "CockroachDB": ["cockroachdb", "cockroach db"],
    "PlanetScale": ["planetscale", "planet scale"],
    "Supabase": ["supabase"],
    
    # Databases - NoSQL
    "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"],
    "Cassandra": ["cassandra", "apache cassandra"],
    "DynamoDB": ["dynamodb", "dynamo db", "aws dynamodb"],
    "Couchbase": ["couchbase"],
    "CouchDB": ["couchdb", "couch db"],
    "Neo4j": ["neo4j", "neo 4j"],
    "ArangoDB": ["arangodb", "arango db"],
    "RethinkDB": ["rethinkdb", "rethink db"],
    "Firebase": ["firebase", "firestore", "firebase realtime"],
    "Elasticsearch": ["elasticsearch", "elastic search", "elastic"],
    "Solr": ["solr", "apache solr"],
    
    # ORMs & Query Builders
    "Prisma": ["prisma", "prisma orm"],
    "TypeORM": ["typeorm", "type orm"],
    "Sequelize": ["sequelize"],
    "Mongoose": ["mongoose"],
    "SQLAlchemy": ["sqlalchemy", "sql alchemy"],
    "Hibernate": ["hibernate"],
    "JPA": ["jpa", "java persistence api"],
    "Doctrine": ["doctrine"],
    "ActiveRecord": ["activerecord", "active record"],
    "Drizzle": ["drizzle", "drizzle orm"],
    "Knex.js": ["knex", "knexjs", "knex.js"],
    
    # Cloud Platforms & Services
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Digital Ocean": ["digital ocean", "digitalocean", "do"],
    "Heroku": ["heroku"],
    "Netlify": ["netlify"],
    "Vercel": ["vercel"],
    "Railway": ["railway", "railway.app"],
    "Render": ["render", "render.com"],
    "Fly.io": ["fly", "fly.io", "flyio"],
    "Cloudflare": ["cloudflare", "cloudflare workers"],
    "Linode": ["linode"],
    
    # AWS Services
    "EC2": ["ec2", "aws ec2", "elastic compute"],
    "S3": ["s3", "aws s3", "amazon s3"],
    "Lambda": ["lambda", "aws lambda"],
    "RDS": ["rds", "aws rds"],
    "CloudFront": ["cloudfront", "aws cloudfront"],
    "ECS": ["ecs", "aws ecs", "elastic container"],
    "EKS": ["eks", "aws eks", "elastic kubernetes"],
    "API Gateway": ["api gateway", "aws api gateway"],
    "CloudWatch": ["cloudwatch", "aws cloudwatch"],
    "SNS": ["sns", "aws sns"],
    "SQS": ["sqs", "aws sqs"],
    
    # DevOps & CI/CD
    "Docker": ["docker", "docker compose", "docker-compose", "dockerfile"],
    "Kubernetes": ["kubernetes", "k8s", "k9s"],
    "Terraform": ["terraform", "tf"],
    "Ansible": ["ansible"],
    "Jenkins": ["jenkins"],
    "GitHub Actions": ["github actions", "gh actions"],
    "GitLab CI": ["gitlab ci", "gitlab ci/cd"],
    "CircleCI": ["circleci", "circle ci"],
    "Travis CI": ["travis", "travis ci"],
    "ArgoCD": ["argocd", "argo cd"],
    "Helm": ["helm", "helm charts"],
    "Vagrant": ["vagrant"],
    "Puppet": ["puppet"],
    "Chef": ["chef"],
    "Prometheus": ["prometheus"],
    "Grafana": ["grafana"],
    "Datadog": ["datadog"],
    "New Relic": ["new relic", "newrelic"],
    "Nginx": ["nginx"],
    "Apache": ["apache", "apache http"],
    
    # Testing Frameworks
    "Jest": ["jest", "jestjs"],
    "Vitest": ["vitest"],
    "Mocha": ["mocha", "mochajs"],
    "Chai": ["chai", "chaijs"],
    "Jasmine": ["jasmine"],
    "Cypress": ["cypress", "cypress.io"],
    "Playwright": ["playwright"],
    "Selenium": ["selenium", "selenium webdriver"],
    "Puppeteer": ["puppeteer"],
    "Testing Library": ["testing library", "react testing library", "rtl"],
    "PyTest": ["pytest", "py.test"],
    "JUnit": ["junit", "junit 5"],
    "TestNG": ["testng"],
    "Mockito": ["mockito"],
    "RSpec": ["rspec"],
    "Enzyme": ["enzyme"],
    
    # Mobile Development
    "React Native": ["react native", "react-native", "rn"],
    "Flutter": ["flutter"],
    "SwiftUI": ["swiftui", "swift ui"],
    "Jetpack Compose": ["jetpack compose", "compose"],
    "Xamarin": ["xamarin"],
    "Ionic": ["ionic"],
    "Cordova": ["cordova", "phonegap"],
    "Expo": ["expo", "expo.io"],
    "Capacitor": ["capacitor"],
    
    # Data Science & ML
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "Keras": ["keras"],
    "Scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "Pandas": ["pandas", "pd"],
    "NumPy": ["numpy", "np"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],
    "Plotly": ["plotly"],
    "Jupyter": ["jupyter", "jupyter notebook", "jupyterlab"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision", "cv", "image processing"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Statistics": ["statistics", "statistical analysis"],
    "LangChain": ["langchain", "lang chain"],
    "Hugging Face": ["hugging face", "huggingface", "transformers"],
    "YOLO": ["yolo", "yolov5", "yolov8"],
    "OpenCV": ["opencv", "cv2"],
    "SpaCy": ["spacy"],
    "NLTK": ["nltk"],
    "XGBoost": ["xgboost"],
    "LightGBM": ["lightgbm", "lgbm"],
    "Apache Spark": ["spark", "apache spark", "pyspark"],
    "Tableau": ["tableau"],
    "Power BI": ["power bi", "powerbi"],
    
    # Version Control & Collaboration
    "Git": ["git"],
    "GitHub": ["github"],
    "GitLab": ["gitlab"],
    "Bitbucket": ["bitbucket"],
    "Mercurial": ["mercurial", "hg"],
    "SVN": ["svn", "subversion"],
    
    # Project Management & Productivity
    "Jira": ["jira", "jira software"],
    "Confluence": ["confluence"],
    "Trello": ["trello"],
    "Asana": ["asana"],
    "Monday.com": ["monday", "monday.com"],
    "Notion": ["notion"],
    "Slack": ["slack"],
    "Discord": ["discord"],
    "Microsoft Teams": ["teams", "microsoft teams", "ms teams"],
    
    # Design & Prototyping
    "Figma": ["figma"],
    "Sketch": ["sketch"],
    "Adobe XD": ["adobe xd", "xd"],
    "InVision": ["invision"],
    "Framer": ["framer"],
    "Zeplin": ["zeplin"],
    "Photoshop": ["photoshop", "adobe photoshop"],
    "Illustrator": ["illustrator", "adobe illustrator"],
    
    # API & Integration
    "REST API": ["rest", "restful", "rest api", "restful api"],
    "GraphQL": ["graphql", "graph ql"],
    "gRPC": ["grpc", "grpc protocol"],
    "WebSocket": ["websocket", "websockets", "ws"],
    "tRPC": ["trpc"],
    "Postman": ["postman"],
    "Insomnia": ["insomnia"],
    "Swagger": ["swagger", "openapi"],
    "Axios": ["axios"],
    "Fetch API": ["fetch", "fetch api"],
    
    # Architecture & Patterns
    "Microservices": ["microservices", "microservice"],
    "Monolith": ["monolith", "monolithic"],
    "Serverless": ["serverless", "faas"],
    "Event-Driven": ["event driven", "event-driven", "eda"],
    "CQRS": ["cqrs"],
    "Domain-Driven Design": ["ddd", "domain driven design"],
    "Clean Architecture": ["clean architecture"],
    "MVC": ["mvc", "model view controller"],
    "MVVM": ["mvvm", "model view viewmodel"],
    
    # Security
    "OAuth": ["oauth", "oauth2", "oauth 2.0"],
    "JWT": ["jwt", "json web token"],
    "SSL/TLS": ["ssl", "tls", "https"],
    "OWASP": ["owasp"],
    "Penetration Testing": ["penetration testing", "pen testing", "pentesting"],
    "Cryptography": ["cryptography", "encryption"],
    
    # Methodologies & Practices
    "Agile": ["agile", "agile development"],
    "Scrum": ["scrum"],
    "Kanban": ["kanban"],
    "DevOps": ["devops", "dev ops"],
    "CI/CD": ["ci/cd", "ci cd", "continuous integration", "continuous delivery"],
    "TDD": ["tdd", "test driven development", "test-driven"],
    "BDD": ["bdd", "behavior driven development"],
    "Pair Programming": ["pair programming"],
    "Code Review": ["code review"],
    
    # Operating Systems
    "Linux": ["linux", "unix"],
    "Ubuntu": ["ubuntu"],
    "Debian": ["debian"],
    "CentOS": ["centos"],
    "Red Hat": ["red hat", "redhat", "rhel"],
    "macOS": ["macos", "mac os", "osx"],
    "Windows": ["windows", "windows 10", "windows 11"],
    "Windows Server": ["windows server"],
    
    # Blockchain & Web3
    "Blockchain": ["blockchain", "web3"],
    "Ethereum": ["ethereum", "eth"],
    "Web3.js": ["web3", "web3.js", "web3js"],
    "Ethers.js": ["ethers", "ethers.js", "ethersjs"],
    "Hardhat": ["hardhat"],
    "Truffle": ["truffle"],
    
    # Build Tools & Bundlers
    "Webpack": ["webpack"],
    "Vite": ["vite", "vitejs"],
    "Rollup": ["rollup"],
    "Parcel": ["parcel"],
    "esbuild": ["esbuild"],
    "Turbopack": ["turbopack"],
    "Gulp": ["gulp", "gulpjs"],
    "Grunt": ["grunt", "gruntjs"],
    "Babel": ["babel", "babeljs"],
    "SWC": ["swc"],
    
    # Package Managers
    "npm": ["npm"],
    "Yarn": ["yarn"],
    "pnpm": ["pnpm"],
    "pip": ["pip"],
    "Poetry": ["poetry"],
    "Composer": ["composer"],
    "Maven": ["maven"],
    "Gradle": ["gradle"],
    "Cargo": ["cargo"],
}

def get_canonical_skill_name(text: str) -> str | None:
    """
    Given a skill text, return the canonical skill name if it matches ontology.
    Returns None if no match found.
    """
    text_lower = text.lower().strip()
    
    for canonical, variations in SKILL_ONTOLOGY.items():
        if text_lower in variations or text_lower == canonical.lower():
            return canonical
    
    return None


def extract_skills_from_text(text: str) -> list[str]:
    """
    Extract all matching skills from text using the ontology with word boundary detection.
    Returns list of canonical skill names.
    
    Uses regex word boundaries to prevent false positives:
    - "rust" in "trust" -> NO MATCH
    - "go" in "let's go" -> NO MATCH  
    - "python" in "I know python" -> MATCH
    """
    import re
    
    text_lower = text.lower()
    found_skills = set()
    
    for canonical, variations in SKILL_ONTOLOGY.items():
        for variation in variations:
            # Use word boundaries to match complete words only
            # \b ensures we match whole words, not substrings
            pattern = r'\b' + re.escape(variation) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(canonical)
                break
    
    return sorted(list(found_skills))
