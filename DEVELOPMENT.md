# Development Guide

Complete guide for developing and extending Intuitive Draft.

## Development Environment Setup

### Prerequisites
- Node.js 18+
- Python 3.10+
- Git
- Your favorite code editor (VS Code recommended)

### Initial Setup

```bash
# Clone repository (if not already done)
git clone <repo-url>
cd intuitive-draft

# Create .env files
cp .env.example .env.local
cp backend/.env.example backend/.env
```

## Frontend Development

### Starting the Development Server

```bash
npm install
npm run dev
```

Server runs at `http://localhost:3000` with hot module reloading.

### Project Structure

```
app/
├── page.tsx                 # Main page component
├── layout.tsx              # Root layout
└── globals.css            # Global styles and theme variables

components/
├── input-form.tsx         # Input form component
├── results-display.tsx    # Results display
└── ui/                    # shadcn/ui components

lib/
├── api-client.ts         # API client functions
├── types.ts              # TypeScript type definitions
└── utils.ts              # Utility functions

styles/
└── (included in globals.css)
```

### Key Files to Understand

**page.tsx** - Main application logic:
- State management for results and loading
- Error handling
- API calls

**input-form.tsx** - Form component:
- Input validation
- Form submission
- Loading states

**results-display.tsx** - Results visualization:
- Clarity score display
- Structured plan rendering
- Copy functionality

### Adding New Features

**Example: Add a favorite/save feature**

1. Add to TypeScript types in `lib/types.ts`:
```typescript
export interface SavedPlan extends AnalyzePlanResult {
  id: string;
  savedAt: Date;
}
```

2. Create new component `components/saved-plans.tsx`:
```typescript
export function SavedPlans({ plans }: { plans: SavedPlan[] }) {
  // Component implementation
}
```

3. Update main page `app/page.tsx` to include the component

### Styling Guide

**Using Tailwind CSS:**
- Prefer utility classes: `flex items-center justify-between`
- Use semantic tokens from globals.css: `bg-primary`, `text-foreground`
- Mobile-first responsive: `md:`, `lg:` prefixes

**Theme Variables (globals.css):**
```css
:root {
  --primary: #3b82f6;
  --background: #ffffff;
  --foreground: #0a0a0a;
  /* ... more tokens ... */
}
```

### Testing Components

```bash
# Run type checking
npm run type-check

# Build for production
npm run build

# Start production build
npm run start
```

## Backend Development

### Starting the Development Server

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

Server runs at `http://localhost:8000`

### Project Structure

```
api/
├── views.py              # API view classes
├── serializers.py        # DRF serializers
├── gemini_service.py     # Gemini integration
├── urls.py               # URL routing
├── models.py             # Database models
└── apps.py               # App configuration

config/
├── settings.py           # Django settings
├── urls.py               # Main URL config
└── wsgi.py               # WSGI application

manage.py                 # Django management script
```

### Django Settings

Key settings in `backend/config/settings.py`:

```python
DEBUG = True                    # Development mode
ALLOWED_HOSTS = ['localhost']   # Allowed domains
INSTALLED_APPS = [...]          # Installed apps
CORS_ALLOWED_ORIGINS = [...]    # CORS origins
```

### Adding API Endpoints

**Example: Add a new endpoint**

1. Create view in `api/views.py`:
```python
class NewFeatureView(APIView):
    def post(self, request):
        serializer = NewFeatureSerializer(data=request.data)
        if serializer.is_valid():
            # Process data
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

2. Create serializer in `api/serializers.py`:
```python
class NewFeatureSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.IntegerField()
```

3. Add URL in `api/urls.py`:
```python
path('new-feature/', NewFeatureView.as_view(), name='new-feature'),
```

### Modifying the Gemini Prompt

Edit the prompt in `api/gemini_service.py` method `_build_prompt()`:

```python
def _build_prompt(self, idea: str) -> str:
    return f"""Your custom instructions here.
    
    Analyze this: "{idea}"
    
    Return JSON with:
    {{
      "field1": "value",
      ...
    }}
    """
```

### Testing Backend

```bash
# Run tests (if tests exist)
python manage.py test

# Check code with linting
pip install flake8
flake8 api/

# Interactive shell
python manage.py shell
```

### Making Database Changes

```bash
# Create migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create new app
python manage.py startapp app_name
```

## API Development Workflow

### Testing Endpoints with cURL

```bash
# Test analyze-plan endpoint
curl -X POST http://localhost:8000/api/analyze-plan/ \
  -H "Content-Type: application/json" \
  -d '{"idea": "Your idea here"}'

# Test health check
curl http://localhost:8000/api/health/
```

### Using Postman/Insomnia

1. Create new request
2. Set method to POST
3. Set URL to `http://localhost:8000/api/analyze-plan/`
4. Set header: `Content-Type: application/json`
5. Set body:
```json
{
  "idea": "Test idea"
}
```

### Error Debugging

Add debugging to `api/views.py`:

```python
import logging
logger = logging.getLogger(__name__)

class AnalyzePlanView(APIView):
    def post(self, request):
        logger.debug(f"Request data: {request.data}")
        # ... rest of code
        logger.error(f"Error: {str(e)}")
```

View logs in terminal output.

## Frontend-Backend Integration

### API Client Usage

In components, use the API client from `lib/api-client.ts`:

```typescript
import { analyzePlan } from '@/lib/api-client'

const result = await analyzePlan({ idea: userInput })
```

### Handling API Responses

```typescript
try {
  const result = await analyzePlan({ idea })
  setResult(result)
} catch (error) {
  setError(error.message)
}
```

### Debugging API Issues

1. **Check browser DevTools Network tab:**
   - See request/response details
   - Check status codes and headers

2. **Check backend logs:**
   - Look for errors in terminal where Django runs

3. **Test with curl directly:**
   - Verify API works independently

4. **Check environment variables:**
   - Ensure `NEXT_PUBLIC_API_URL` is set
   - Ensure `GOOGLE_API_KEY` is set

## Version Control

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/my-feature

# Create pull request on GitHub
```

### Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Code refactoring
- `test:` Adding tests

## Code Style Guidelines

### Python (Backend)

```python
# Use clear variable names
user_input = request.data.get('idea')

# Add docstrings
def analyze_plan(idea: str) -> dict:
    """Analyze a plan idea and return structured output."""
    pass

# Handle errors gracefully
try:
    result = gemini_service.analyze(idea)
except Exception as e:
    logger.error(f"Analysis failed: {e}")
    raise ValueError("Failed to analyze plan")
```

### TypeScript (Frontend)

```typescript
// Use clear names
const { idea, setIdea } = useState('')

// Add type annotations
function handleSubmit(idea: string): Promise<void> {
  // ...
}

// Handle errors
if (!response.ok) {
  throw new Error('API error')
}
```

## Performance Optimization

### Frontend

```bash
# Analyze bundle size
npm run build
npm run analyze

# Check with Lighthouse
npm run build
npm run start
# Open DevTools → Lighthouse tab
```

### Backend

- Use Django debug toolbar in development:
```bash
pip install django-debug-toolbar
```

- Query optimization with `.select_related()` and `.prefetch_related()`
- Cache frequent responses:
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def api_view(request):
    pass
```

## Debugging Tips

### Frontend Debugging

```typescript
// Add console logs
console.log("[v0] Debug message:", variable)

// Use debugger
debugger;

// React DevTools
npm install @react-devtools/shell
```

### Backend Debugging

```python
# Add print statements
print(f"Debug: {variable}")

# Use pdb
import pdb; pdb.set_trace()

# Check settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.INSTALLED_APPS)
```

## Testing Best Practices

### Frontend Testing

```bash
# Add testing library
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Run tests
npm test
```

Example test:
```typescript
import { render, screen } from '@testing-library/react'
import { InputForm } from '@/components/input-form'

test('renders input form', () => {
  render(<InputForm onSubmit={() => {}} isLoading={false} />)
  expect(screen.getByRole('button')).toBeInTheDocument()
})
```

### Backend Testing

```python
from django.test import TestCase
from rest_framework.test import APIClient

class AnalyzePlanTests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_analyze_plan(self):
        response = self.client.post(
            '/api/analyze-plan/',
            {'idea': 'Test idea'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
```

## Development Checklist

Before committing:
- [ ] Code is properly formatted
- [ ] No console errors or warnings
- [ ] Tests pass
- [ ] Environment variables are set
- [ ] Frontend builds successfully
- [ ] Backend tests pass
- [ ] API endpoints respond correctly
- [ ] Error handling is in place
- [ ] Documentation is updated

## Useful Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## Getting Help

1. Check existing documentation
2. Review similar implementations in codebase
3. Check error messages and logs
4. Search GitHub issues
5. Ask team members or community

## Setting Up Pre-commit Hooks (Optional)

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
npm install --save-dev prettier eslint
pip install black flake8

# Run hooks before commit
pre-commit run --all-files
```

## IDE Setup Recommendations

### VS Code Extensions
- Python
- Django
- REST Client
- Thunder Client
- Prettier - Code formatter
- ESLint
- Tailwind CSS IntelliSense
- Better Comments

### Settings (.vscode/settings.json)
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "python.formatting.provider": "black"
}
```

Happy coding!
