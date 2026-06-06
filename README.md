# SkillBridge AI

> AI-Powered Career Intelligence and Recommendation Platform for Students

SkillBridge AI is a comprehensive career development platform that helps students discover opportunities, build skills, and connect with mentors through intelligent recommendations powered by AI and machine learning.

## 🚀 Features

- **Smart Recommendations**: AI-powered job, internship, and course recommendations
- **Resume Intelligence**: Automated resume parsing and skill extraction
- **Career Roadmaps**: Personalized learning paths with Gemini AI
- **Mentor Matching**: Connect with industry experts in your field
- **Study Groups**: Collaborative learning communities
- **Profile Builder**: AI-assisted profile creation from resumes
- **Placement Readiness**: Track and improve your job readiness score

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL 16** - Primary database
- **Qdrant** - Vector database for embeddings
- **Redis** - Caching and session management
- **SQLAlchemy** - Async ORM
- **Alembic** - Database migrations
- **Celery** - Background task processing

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS
- **ShadCN UI** - Beautiful component library

### AI/ML
- **Sentence Transformers** - Text embeddings (all-MiniLM-L6-v2)
- **Google Gemini** - LLM for roadmap generation
- **SpaCy** - NLP and entity extraction
- **PyMuPDF** - PDF parsing

## 📁 Project Structure

```
SkillBridge/
├── backend/              # FastAPI backend
│   ├── alembic/         # Database migrations
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core utilities (security, config)
│   │   ├── db/          # Database setup
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── main.py      # Application entry
│   ├── scripts/         # Utility scripts
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # App router pages
│   │   ├── components/ # React components
│   │   └── lib/        # Utilities
│   └── package.json
├── docker-compose.yml   # Docker orchestration
├── phase1.md           # Phase 1 documentation
├── phase2.md           # Phase 2 documentation
└── implementation_plan.md
```

## 🔧 Development Setup

### Prerequisites
- Docker Desktop
- Python 3.11 or 3.12
- Node.js 18+
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/skillbridge-ai.git
cd skillbridge-ai
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration

# Frontend
cp frontend/.env.local.example frontend/.env.local
```

3. **Start services with Docker**
```bash
docker compose up -d
```

4. **Run database migrations**
```bash
cd backend
python -m alembic upgrade head
```

5. **Access the application**
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## 📚 Documentation

Detailed documentation for each development phase:

- **[Phase 1: Infrastructure & Scaffolding](phase1.md)** - Docker, database models, initial setup
- **[Phase 2: Authentication & Profiles](phase2.md)** - JWT auth, RBAC, profile management
- **Phase 3: Resume & AI Pipeline** (Coming soon)
- **Phase 4: Recommendations** (Coming soon)
- **Phase 5: Portals** (Coming soon)
- **Phase 6: Deployment** (Coming soon)

See [implementation_plan.md](implementation_plan.md) for the complete roadmap.

## 🔑 Key Features by Role

### Students
- Upload and analyze resume
- Get personalized job/internship recommendations
- Generate career roadmaps
- Connect with mentors
- Join study groups
- Track placement readiness

### Mentors
- Manage mentee relationships
- Schedule mentoring sessions
- Provide feedback and guidance
- Build professional network

### Companies
- Post jobs and internships
- Search candidate database
- Review applications
- Manage hiring pipeline

### Admins
- User management and verification
- Platform analytics
- Content moderation

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Production Environment
- **Frontend**: Vercel
- **Backend**: Railway
- **Database**: Supabase (PostgreSQL)
- **Vector DB**: Qdrant Cloud
- **Monitoring**: Sentry + LogTail

See deployment guides in Phase 6 documentation.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Vedant Naik** - Initial work

## 🙏 Acknowledgments

- FastAPI community for excellent documentation
- Next.js team for the amazing framework
- All open-source contributors

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

Built with ❤️ for students seeking their career path
