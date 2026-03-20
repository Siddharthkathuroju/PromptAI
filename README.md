# Intuitive Draft - AI-Powered Plan Analyzer

Transform vague ideas into clear, structured plans using AI. Intuitive Draft helps you analyze ideas and generate actionable plans with clarity scoring, structured steps, and next actions.

## Architecture

The application consists of:
- **Frontend**: Next.js 15 with TypeScript, Tailwind CSS, and shadcn/ui
- **Backend**: Django REST Framework with Google Gemini AI integration
- **API**: RESTful API for plan analysis

## Prerequisites

- Node.js 18+ 
- Python 3.10+
- Google Gemini API Key (get one at https://ai.google.dev/)

## Installation

### 1. Frontend Setup

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 2. Backend Setup

```bash
cd backend

# Create a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver 0.0.0.0:8000
```

The backend API will be available at `http://localhost:8000`

## Configuration

### Frontend Environment Variables

Create `.env.local` in the project root:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend Environment Variables

Create `.env` in the `backend/` directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## Getting a Google Gemini API Key

1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Create a new project or select an existing one
4. Generate an API key
5. Copy the key and add it to your `.env` file

## Running the Application

### Start both servers:

**Terminal 1 - Frontend:**
```bash
npm run dev
```

**Terminal 2 - Backend:**
```bash
cd backend
python manage.py runserver
```

Then open `http://localhost:3000` in your browser.

## API Endpoints

### POST `/api/analyze-plan/`

Analyze an idea and get a structured plan.

**Request:**
```json
{
  "idea": "I want to build a social media app for developers"
}
```

**Response:**
```json
{
  "clarity_score": 65,
  "structured_plan": {
    "goal": "Create a social platform connecting developers",
    "method": "Build web app with user authentication, feed, and messaging",
    "steps": [
      {
        "title": "Design Database Schema",
        "description": "Plan user profiles, posts, and connections"
      }
    ],
    "timeline": "6-9 months"
  },
  "missing_elements": [
    "Budget and resources",
    "Target audience definition",
    "Monetization strategy"
  ],
  "simplified_version": "A social network for developers to connect and share ideas.",
  "actionable_steps": [
    "Define your target demographic",
    "Research existing platforms",
    "Create wireframes"
  ]
}
```

## Features

- **Clarity Score**: Evaluate how well-defined your idea is (0-100)
- **Structured Plan**: Break down ideas into goal, method, steps, and timeline
- **Missing Elements**: Identify gaps in your planning
- **Simplified Version**: Get a one-sentence summary
- **Actionable Steps**: Get concrete next actions to take

## Project Structure

```
.
├── app/                    # Next.js app directory
│   ├── page.tsx           # Main page
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── input-form.tsx     # Plan input form
│   ├── results-display.tsx # Results display
│   └── ui/               # shadcn/ui components
├── lib/
│   ├── api-client.ts      # API client
│   └── types.ts           # TypeScript types
├── backend/              # Django backend
│   ├── api/              # API app
│   │   ├── views.py      # API views
│   │   ├── serializers.py # DRF serializers
│   │   ├── gemini_service.py # Gemini integration
│   │   └── urls.py       # URL routing
│   ├── config/           # Django settings
│   ├── manage.py
│   └── requirements.txt
└── package.json
```

## Deployment

### Frontend (Vercel)
```bash
npm run build
npm run start
```

### Backend (Any Python-capable server)
```bash
pip install -r requirements.txt
python manage.py migrate --settings=config.settings
python manage.py collectstatic --noinput --settings=config.settings
gunicorn config.wsgi --bind 0.0.0.0:8000
```

## Troubleshooting

### "GOOGLE_API_KEY is not set"
- Ensure you have added `GOOGLE_API_KEY` to your `.env` file in the backend directory
- Restart the backend server after adding the key

### CORS errors
- Check that `CORS_ALLOWED_ORIGINS` in `backend/.env` includes your frontend URL
- Default is `http://localhost:3000` for development

### API connection issues
- Verify the backend is running at `http://localhost:8000`
- Check that `NEXT_PUBLIC_API_URL` in `.env.local` matches your backend URL
- Check browser console for error messages

### Response parsing errors
- Ensure your Gemini API key is valid and has quota remaining
- Check that the API response is valid JSON
- Review backend logs for detailed error messages

## Development

### Frontend
- Built with Next.js 15 and React 19
- Uses Tailwind CSS for styling
- shadcn/ui for UI components
- TypeScript for type safety

### Backend
- Django 4.2 with Django REST Framework
- Google Generative AI SDK for Gemini integration
- CORS support for frontend integration

## License

MIT

## Support

For issues and questions, please open an issue on the repository.
