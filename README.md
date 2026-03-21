# PromptAI

PromptAI is a is a full-stack AI application designed to transform vague, unstructured natural language ideas into clear, actionable project roadmaps. Developed for the KALNET Intern Assignment, the tool bridges the gap between raw ideation and execution by identifying missing elements and providing a quantitative clarity score.

## Architecture

The application consists of:
- **Frontend**: Built with Next.js 15, TypeScript, Tailwind CSS, and shadcn/ui.
- **Backend**: Powered by Django REST Framework with Google Gemini AI integration.
- **API**: RESTful API for analyzing and structuring project plans.

## Prerequisites

To run this application, ensure you have the following installed:
- Node.js 18+
- Python 3.10+
- Google Gemini API Key (get one at [Google AI](https://ai.google.dev/))

## Installation

### Frontend Setup

1. Navigate to the `app` directory and install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env.local
   ```
   Edit `.env.local` and set the following:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at [http://localhost:3000](http://localhost:3000).

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Google Gemini API key:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the backend server:
   ```bash
   python manage.py runserver
   ```
   The backend API will be available at [http://localhost:8000](http://localhost:8000).

## Features

- **Clarity Score**: Evaluate the clarity of your idea (0-100).
- **Structured Plan**: Break down ideas into goals, methods, steps, and timelines.
- **Missing Elements**: Identify gaps in your planning.
- **Simplified Version**: Get a one-sentence summary of your idea.
- **Actionable Steps**: Receive concrete next actions to take.

## Clarity Score Logic:
- The score is calculated on a 100-point weighted scale:
- Goal Clarity (25%): Is a specific, measurable objective present?
- Defined Steps (25%): Are there at least three logical milestones?
- Timeline Presence (25%): Is a timeframe or deadline identified?
- Resource Identification (25%): Are required tools or personnel mentioned? 

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

## Project Structure

```plaintext
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

1. Build the frontend:
   ```bash
   npm run build
   ```

2. Start the production server:
   ```bash
   npm run start
   ```

### Backend (Any Python-capable server)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate --settings=config.settings
   ```

3. Collect static files:
   ```bash
   python manage.py collectstatic --noinput --settings=config.settings
   ```

4. Start the server using Gunicorn:
   ```bash
   gunicorn config.wsgi --bind 0.0.0.0:8000
   ```
   Successfully Dockerized and ready for deployment on platforms like Vercel or Render.
 
  ## Developer Note (Challenges & Approach)
  I implemented this project using Next.js for the frontend and Django for the backend, ensuring a clean separation of concerns. The project was successfully implemented, Dockerized, and published to this repository.

  ## Challenges Faced:
  The primary challenge was ensuring the AI consistently returned structured JSON without conversational "noise." Handling edge cases where user input was extremely brief required fine-tuning the prompt to provide constructive feedback rather than failing.

  ## Approach to AI Prompting:
  I approached prompting by treating the LLM as a data extractor first and a writer second. By providing a strict rubric for the "Clarity Score," I ensured that the results were objective and reproducible, aligning with the requirement for "thinking clarity" over "coding complexity".
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

## Support

For issues and questions, please open an issue on the repository.
