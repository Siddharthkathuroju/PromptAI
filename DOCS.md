# Documentation Index

Complete navigation guide for all project documentation.

## Getting Started

Start here if you're new to the project:

1. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
   - Docker setup (easiest)
   - Manual setup instructions
   - Getting Google API key
   - Testing with curl

2. **[README.md](README.md)** - Complete overview
   - Project architecture
   - Prerequisites and installation
   - Configuration details
   - Troubleshooting guide
   - File structure

## For Users

### Using the Application

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide with setup options
- **[README.md](README.md)** - Full usage documentation

### Deployment

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
  - Frontend deployment (Vercel)
  - Backend deployment (Railway/Render)
  - Database setup
  - Monitoring and scaling
  - Troubleshooting

## For Developers

### Setting Up Development Environment

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Complete development guide
  - Frontend development setup
  - Backend development setup
  - Adding new features
  - Code style guidelines
  - Debugging tips
  - Testing setup

### Testing

- **[TESTING.md](TESTING.md)** - Testing procedures
  - API testing with curl
  - Frontend testing
  - Browser compatibility
  - Performance testing
  - Integration testing
  - Security testing

## Project Information

### Understanding the Project

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview
  - What was built
  - Technology stack
  - API response structure
  - Key features
  - File structure

### Architecture

```
Frontend (Next.js) ←→ Backend (Django) ←→ Gemini API
     Port 3000           Port 8000
```

See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for detailed architecture.

## Quick Reference

### Commands

**Frontend:**
```bash
npm install          # Install dependencies
npm run dev          # Start dev server (port 3000)
npm run build        # Build for production
npm run start        # Start production server
npm run type-check   # Check TypeScript
```

**Backend:**
```bash
python -m venv venv              # Create environment
source venv/bin/activate         # Activate (Windows: venv\Scripts\activate)
pip install -r requirements.txt  # Install dependencies
python manage.py runserver       # Start dev server (port 8000)
python manage.py migrate         # Apply migrations
python manage.py test            # Run tests
```

**Docker:**
```bash
docker-compose up                # Start both services
docker-compose down              # Stop services
docker-compose logs -f backend   # View logs
```

### Environment Variables

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (backend/.env):**
```
GOOGLE_API_KEY=your_api_key
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health/` | Health check |
| POST | `/api/analyze-plan/` | Analyze an idea |

### File Structure

```
intuitive-draft/
├── Frontend files (Next.js)
│   ├── app/           # Pages and layouts
│   ├── components/    # React components
│   └── lib/          # Utilities and types
├── backend/          # Django backend
│   ├── api/          # API endpoints
│   └── config/       # Django config
├── Documentation
│   ├── README.md     # Main documentation
│   ├── QUICKSTART.md # Quick start
│   ├── DEVELOPMENT.md # Dev guide
│   ├── TESTING.md    # Testing guide
│   ├── DEPLOYMENT.md # Deploy guide
│   └── PROJECT_SUMMARY.md # Overview
└── Configuration
    ├── docker-compose.yml
    ├── Dockerfile
    └── Various configs
```

## Common Tasks

### Setting Up for Development
→ See [DEVELOPMENT.md](DEVELOPMENT.md)

### Running Locally
→ See [QUICKSTART.md](QUICKSTART.md)

### Testing Changes
→ See [TESTING.md](TESTING.md)

### Deploying to Production
→ See [DEPLOYMENT.md](DEPLOYMENT.md)

### Extending Features
→ See [DEVELOPMENT.md](DEVELOPMENT.md) - "Adding New Features"

### Understanding Architecture
→ See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## Technology Stack

### Frontend
- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui

### Backend
- Django 4.2
- Django REST Framework
- Google Generative AI SDK

### DevOps
- Docker & Docker Compose
- Python venv

## Documentation by Role

### Product Manager
1. Start with [README.md](README.md) for overview
2. Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for features
3. Review [DEPLOYMENT.md](DEPLOYMENT.md) for go-live steps

### Frontend Developer
1. Read [DEVELOPMENT.md](DEVELOPMENT.md) frontend section
2. Review [README.md](README.md) for setup
3. Check [TESTING.md](TESTING.md) for testing procedures

### Backend Developer
1. Read [DEVELOPMENT.md](DEVELOPMENT.md) backend section
2. Review [README.md](README.md) for setup
3. Check [TESTING.md](TESTING.md) for testing procedures

### DevOps Engineer
1. Review [DEPLOYMENT.md](DEPLOYMENT.md)
2. Check [DEVELOPMENT.md](DEVELOPMENT.md) for Docker setup
3. See [QUICKSTART.md](QUICKSTART.md) for local testing

### QA/Tester
1. Start with [QUICKSTART.md](QUICKSTART.md) to set up
2. Follow [TESTING.md](TESTING.md) procedures
3. Reference [README.md](README.md) for troubleshooting

## Troubleshooting

Having issues? Check these sections:

- **Setup issues** → [QUICKSTART.md](QUICKSTART.md) Troubleshooting
- **Runtime issues** → [README.md](README.md) Troubleshooting
- **Testing issues** → [TESTING.md](TESTING.md) Debugging
- **Development issues** → [DEVELOPMENT.md](DEVELOPMENT.md) Debugging Tips
- **Deployment issues** → [DEPLOYMENT.md](DEPLOYMENT.md) Troubleshooting

## FAQ

**Q: How do I get a Google API key?**
A: See [QUICKSTART.md](QUICKSTART.md) or [README.md](README.md) - "Getting a Google Gemini API Key"

**Q: Can I use Docker?**
A: Yes! See [QUICKSTART.md](QUICKSTART.md) - "Option 1: Using Docker"

**Q: How do I deploy to production?**
A: See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions

**Q: Where can I find API documentation?**
A: See [README.md](README.md) - "API Endpoints" section

**Q: How do I modify the Gemini prompt?**
A: See [DEVELOPMENT.md](DEVELOPMENT.md) - "Modifying the Gemini Prompt"

**Q: What are the system requirements?**
A: See [README.md](README.md) - "Prerequisites"

## Additional Resources

- [Google Gemini API Documentation](https://ai.google.dev/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## Document Versions

- README.md: Complete setup & usage guide
- QUICKSTART.md: Fast 5-minute start
- DEVELOPMENT.md: Development workflows
- TESTING.md: Testing procedures
- DEPLOYMENT.md: Production deployment
- PROJECT_SUMMARY.md: Architecture overview
- DOCS.md: This navigation guide

## Last Updated

Check individual documents for last update dates.

## Contributing

When adding features:
1. Update relevant documentation
2. Follow code style guidelines (see [DEVELOPMENT.md](DEVELOPMENT.md))
3. Add tests (see [TESTING.md](TESTING.md))
4. Update this index if adding new docs

## Support

For issues:
1. Check relevant documentation sections
2. Review troubleshooting guides
3. Check error messages in logs
4. Open an issue on GitHub with:
   - What you were trying to do
   - Error messages
   - Steps to reproduce
   - Your environment details

---

**Welcome to Intuitive Draft! Choose a guide above to get started.**
