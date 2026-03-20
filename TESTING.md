# Testing Guide

Complete testing procedures for the Intuitive Draft application.

## Prerequisites

Before testing, ensure:
1. Both frontend and backend are running
2. GOOGLE_API_KEY is set in backend/.env
3. Frontend is at http://localhost:3000
4. Backend is at http://localhost:8000

## API Testing

### 1. Health Check

**Verify the backend is running:**

```bash
curl http://localhost:8000/api/health/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "intuitive-draft-api"
}
```

### 2. Plan Analysis

**Test the main API endpoint:**

```bash
curl -X POST http://localhost:8000/api/analyze-plan/ \
  -H "Content-Type: application/json" \
  -d '{"idea": "I want to learn machine learning"}'
```

**Expected Response Structure:**
```json
{
  "clarity_score": 45,
  "structured_plan": {
    "goal": "Gain proficiency in machine learning concepts and applications",
    "method": "Structured learning through courses, projects, and practice",
    "steps": [
      {
        "title": "Establish Foundation",
        "description": "Learn Python, linear algebra, statistics, and calculus"
      },
      ...
    ],
    "timeline": "6-12 months"
  },
  "missing_elements": ["Budget", "Learning resources", "Project ideas"],
  "simplified_version": "Learn machine learning through structured study and hands-on projects",
  "actionable_steps": [
    "Enroll in a Python course",
    "Set up a development environment",
    ...
  ]
}
```

### 3. Error Handling

**Test with empty idea:**
```bash
curl -X POST http://localhost:8000/api/analyze-plan/ \
  -H "Content-Type: application/json" \
  -d '{"idea": ""}'
```

**Expected Response:** 400 Bad Request

**Test with missing Google API key:**
Remove GOOGLE_API_KEY from backend/.env and restart.

**Expected Response:** 500 Internal Server Error with API key error message

## Frontend Testing

### 1. UI Rendering

- [ ] Page loads without errors
- [ ] Header and description are visible
- [ ] Input textarea is focused and ready for input
- [ ] "Analyze Idea" button is enabled
- [ ] Empty state message is visible

### 2. Input Validation

- [ ] Empty input disables the button
- [ ] Long input (>5000 chars) is handled gracefully
- [ ] Special characters and Unicode are accepted
- [ ] Whitespace-only input disables the button

### 3. Form Submission

**Test Case 1: Valid Idea**
1. Enter: "I want to start a freelance web design business"
2. Click "Analyze Idea"
3. Verify:
   - Loading state shows spinner
   - Button is disabled during processing
   - Results appear within 10 seconds

**Test Case 2: Simple Idea**
1. Enter: "Learn piano"
2. Click "Analyze Idea"
3. Verify response is generated

### 4. Results Display

- [ ] Clarity score is displayed with progress bar
- [ ] Score color changes based on value (red < 60, blue 60-80, green > 80)
- [ ] Structured plan sections display correctly
- [ ] All steps are numbered and formatted properly
- [ ] Missing elements list displays correctly
- [ ] Action items show checkmark icons
- [ ] "Copy" button works for simplified version
- [ ] "Start over" button resets the form

### 5. Error Handling

**Test Case: API Unreachable**
1. Stop the backend server
2. Enter an idea and submit
3. Verify:
   - Error message appears
   - Helpful message about backend URL
   - User can try again

**Test Case: Invalid Response**
1. Modify gemini_service.py to return invalid JSON (temporarily)
2. Submit a request
3. Verify error is handled gracefully

## Browser Compatibility Testing

Test on the following browsers:
- [ ] Chrome/Edge (Latest)
- [ ] Firefox (Latest)
- [ ] Safari (Latest)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

### Mobile Testing Checklist
- [ ] Input textarea is responsive
- [ ] Results display without horizontal scrolling
- [ ] Buttons are touch-friendly (min 44x44px)
- [ ] Copy button functionality works
- [ ] Clarity score visualization is clear

## Performance Testing

### Load Testing

1. **Frontend Performance**
   ```bash
   npm run build
   npm run start
   # Check Lighthouse scores
   ```
   Expected:
   - Lighthouse Performance > 80
   - First Contentful Paint < 1s

2. **Backend Response Time**
   ```bash
   time curl -X POST http://localhost:8000/api/analyze-plan/ \
     -H "Content-Type: application/json" \
     -d '{"idea": "Build a mobile app"}'
   ```
   Expected: < 10 seconds

### Memory Usage

Monitor during extended use:
- Frontend: Monitor browser DevTools Memory tab
- Backend: Monitor with `ps aux | grep python`

## Integration Testing

### End-to-End Flow

1. **Setup**
   - Start fresh: clear browser cache
   - Ensure clean backend state

2. **Test Sequence**
   ```
   a. Open frontend in fresh browser
   b. Submit: "Create a sustainability consulting firm"
   c. Wait for results
   d. Verify all sections display
   e. Click "Start over"
   f. Submit different idea: "Learn web development"
   g. Verify new results appear
   h. Test copy functionality
   ```

3. **Verification**
   - All data loads correctly
   - No console errors
   - No memory leaks
   - Smooth transitions

## CORS Testing

**Test CORS Configuration:**

```bash
curl -i -X OPTIONS http://localhost:8000/api/analyze-plan/ \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST"
```

Should include:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: POST, OPTIONS
```

## Security Testing

### Input Validation
- [ ] XSS attempts are escaped
- [ ] SQL injection attempts are rejected (if using DB in future)
- [ ] Large payloads (>5MB) are rejected
- [ ] Binary data is handled safely

### API Security
- [ ] API key is not exposed in frontend code
- [ ] API key is not logged in responses
- [ ] Environment variables are properly secured

## Regression Testing

After code changes:

1. Run all API tests
2. Run all UI tests
3. Test with various idea lengths
4. Test error scenarios
5. Test on mobile devices

## Known Limitations

- Gemini API has usage quotas
- Responses may vary based on API model
- First API call may take longer due to cold start
- CORS limited to configured origins

## Debugging

### Enable Debug Logging

**Backend:**
```python
# In backend/config/settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'api': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

**Frontend:**
```javascript
// In lib/api-client.ts
console.log("[v0] API Request:", request);
console.log("[v0] API Response:", response);
```

## Test Data

Use these test ideas with expected outcomes:

| Idea | Expected Clarity |
|------|-----------------|
| "Start a business" | Low (30-40) |
| "Build an e-commerce site for selling handmade jewelry" | Medium (50-70) |
| "Create a SaaS tool for project management targeting remote teams" | High (70-85) |

## Support

If tests fail:
1. Check browser console for errors
2. Check backend logs for issues
3. Verify API key is valid
4. Verify CORS configuration
5. Check environment variables
6. Review README.md for setup instructions
