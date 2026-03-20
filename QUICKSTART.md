# Quick Start Guide

Get the Intuitive Draft application running in minutes!

## Option 1: Using Docker (Recommended for Development)

### Prerequisites
- Docker and Docker Compose installed
- Google Gemini API Key

### Steps

1. **Clone the repository**
   ```bash
   cd intuitive-draft
   ```

2. **Create environment file**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your GOOGLE_API_KEY
   ```

3. **Start the application**
   ```bash
   docker-compose up
   ```

4. **Access the app**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Option 2: Manual Setup

### Frontend Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env.local
   # NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   - Opens at http://localhost:3000

### Backend Setup (in another terminal)

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   # Add your GOOGLE_API_KEY
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the server**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
   - API available at http://localhost:8000

## Getting Your Google Gemini API Key

1. Go to https://ai.google.dev/
2. Click "Get API Key" button
3. Create a new Google Cloud project or select existing
4. Generate an API key
5. Copy the key and paste it in your `.env` file:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

## Testing the Application

### Using the Web Interface
1. Open http://localhost:3000
2. Enter an idea in the textarea
3. Click "Analyze Idea"
4. View the analysis results

### Using the API Directly
```bash
curl -X POST http://localhost:8000/api/analyze-plan/ \
  -H "Content-Type: application/json" \
  -d '{"idea": "I want to build a mobile app for fitness tracking"}'
```

## Troubleshooting

### Issue: "NEXT_PUBLIC_API_URL is undefined"
**Solution**: Make sure you created `.env.local` file with the correct API URL

### Issue: "GOOGLE_API_KEY is not set"
**Solution**: Add your API key to `backend/.env` file and restart the server

### Issue: CORS errors in browser console
**Solution**: Verify backend is running and CORS_ALLOWED_ORIGINS includes your frontend URL

### Issue: Port 3000 or 8000 already in use
**Solution**: Either stop the other process or change the port in the respective application

## Next Steps

- Modify the prompt in `backend/api/gemini_service.py` for different analysis behavior
- Customize the UI components in `components/` directory
- Add authentication if needed
- Deploy to production using Vercel (frontend) and any Python host (backend)

For detailed documentation, see [README.md](README.md)
