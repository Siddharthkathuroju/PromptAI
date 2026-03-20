# Deployment Guide

Complete guide for deploying Intuitive Draft to production.

## Deployment Architecture

```
┌─────────────────────┐
│   Frontend (Next.js) │─── Vercel / Netlify / Similar
└─────────────────────┘
         │ HTTPS
         ↓
┌─────────────────────┐
│  Backend (Django)   │─── Railway / Render / Heroku / AWS
└─────────────────────┘
         │
         ↓
┌─────────────────────┐
│   Gemini API        │─── Google Cloud
└─────────────────────┘
```

## Prerequisites

- GitHub account (for source control)
- Vercel account (or similar platform)
- Railway/Render account (or similar for backend)
- Google Cloud account with Gemini API key
- Domain name (optional but recommended)

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

```bash
# Ensure all tests pass
npm run build
npm run lint

# Check for any build errors
npm run build
```

### Step 2: Connect to Vercel

1. Go to https://vercel.com
2. Sign up/login with GitHub
3. Click "New Project"
4. Select the repository
5. Configure project:
   - Framework: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Environment Variables:
     - `NEXT_PUBLIC_API_URL`: (set to your backend URL)

### Step 3: Set Environment Variables

In Vercel dashboard:
1. Go to Settings → Environment Variables
2. Add `NEXT_PUBLIC_API_URL`:
   ```
   Production: https://api.yourdomain.com (or your backend URL)
   Preview: http://localhost:8000 (for testing)
   ```

### Step 4: Deploy

```bash
git push origin main
```

Vercel will automatically deploy. View at your-project.vercel.app

### Step 5: Custom Domain (Optional)

1. In Vercel → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

## Backend Deployment (Railway/Render)

### Option A: Railway (Recommended)

1. **Connect to Railway**
   - Go to https://railway.app
   - Create account and connect GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Service**
   - Railway will auto-detect Django
   - Set build command: `pip install -r backend/requirements.txt && python backend/manage.py collectstatic --noinput`
   - Set start command: `python backend/manage.py migrate && gunicorn config.wsgi --bind 0.0.0.0:$PORT`

3. **Add Environment Variables**
   ```
   GOOGLE_API_KEY=your_api_key
   SECRET_KEY=generate_secure_key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
   CORS_ALLOWED_ORIGINS=https://yourdomain.com
   ```

4. **Deploy**
   ```bash
   git push origin main
   ```

### Option B: Render

1. **Connect to Render**
   - Go to https://render.com
   - Create account
   - Click "New +" → "Web Service"
   - Connect GitHub repository

2. **Configure**
   - Environment: Python 3.11
   - Build Command: `pip install -r backend/requirements.txt && python backend/manage.py collectstatic --noinput`
   - Start Command: `python backend/manage.py migrate && gunicorn config.wsgi`
   - Root Directory: `backend`

3. **Add Environment Variables**
   Same as Railway configuration

4. **Deploy**
   Service will automatically deploy

## Production Configuration

### Backend Settings (settings.py)

Update for production:

```python
# settings.py

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'api.yourdomain.com']
CORS_ALLOWED_ORIGINS = ['https://yourdomain.com']

# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}

# Database (if using PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### Using PostgreSQL in Production

1. **Create PostgreSQL Database**
   - Railway: Auto-provided
   - Render: Add PostgreSQL service
   - Alternative: AWS RDS, Heroku Postgres

2. **Update requirements.txt**
   ```bash
   pip install psycopg2-binary
   ```

3. **Set Database URL**
   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```

4. **Update Django Settings**
   ```python
   import dj_database_url
   
   DATABASES = {
       'default': dj_database_url.config(
           default=os.getenv('DATABASE_URL')
       )
   }
   ```

## API Security

### Set Secure Secret Key

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Add the output to `SECRET_KEY` environment variable.

### Enable HTTPS

Ensure:
- `SECURE_SSL_REDIRECT = True`
- Use HTTPS for API calls
- Update `CORS_ALLOWED_ORIGINS` to use HTTPS

## Monitoring

### Backend Monitoring

Set up error tracking (choose one):

**Sentry:**
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    traces_sample_rate=0.1,
)
```

**Log Aggregation:**
- Railway: Built-in logs
- Render: Built-in logs
- Alternative: Loggly, Papertrail

### Frontend Monitoring

Add to Next.js:

```bash
npm install @sentry/nextjs
```

## Scaling

### Handle High Load

**Backend:**
1. Use async workers:
   ```bash
   gunicorn config.wsgi --workers=4 --worker-class=gevent
   ```

2. Add caching:
   ```bash
   pip install django-redis
   ```

3. Use CDN for static files:
   - Vercel automatically does this for frontend
   - For backend, upload to S3/CloudFlare

**Frontend:**
- Vercel automatically optimizes and caches
- Configure ISR (Incremental Static Regeneration) if needed

## Database Backups

For PostgreSQL:

```bash
# Manual backup
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

Set up automatic backups through your hosting provider.

## Continuous Deployment

### Automatic Deploys on Git Push

**Frontend (Vercel):**
- Automatic on push to main
- Preview deployments for PRs

**Backend (Railway/Render):**
- Automatic on push to main
- Manual deploys if needed

### CI/CD Pipeline

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r backend/requirements.txt
      - run: cd backend && python manage.py test
  
  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm ci
      - run: npm run build
```

## Troubleshooting

### API Connection Errors
- Verify CORS_ALLOWED_ORIGINS includes frontend URL
- Check that backend is running
- Verify GOOGLE_API_KEY is set

### Build Failures
- Check build logs in deployment platform
- Ensure requirements.txt is up to date
- Verify Python version compatibility

### Slow API Responses
- Check Gemini API quotas
- Monitor database queries
- Check backend logs for errors
- Consider caching responses

### Static Files Not Loading
- Run `collectstatic`
- Configure CDN for large files
- Use WhiteNoise for serving static files

## Rollback

### Rollback Frontend
In Vercel Dashboard → Deployments → Select previous → Redeploy

### Rollback Backend
In Railway/Render → Deployments → Select previous → Redeploy

Or via Git:
```bash
git revert <commit-hash>
git push origin main
```

## DNS Configuration

### Pointing Domain to Services

**Frontend (Vercel):**
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

**Backend API:**
```
Type: CNAME
Name: api
Value: your-railway/render-domain
```

## Production Checklist

Before going live:

- [ ] Frontend builds without errors
- [ ] Backend tests pass
- [ ] All environment variables are set
- [ ] Secret key is secure and random
- [ ] Database is configured and migrated
- [ ] SSL/HTTPS is enabled
- [ ] CORS is properly configured
- [ ] Logging and monitoring are set up
- [ ] Error handling is tested
- [ ] API rate limiting is considered
- [ ] Backup strategy is in place
- [ ] Domain DNS is configured
- [ ] Email notifications are set up for errors

## Helpful Resources

- [Vercel Deployment Documentation](https://vercel.com/docs)
- [Railway Documentation](https://railway.app/docs)
- [Render Documentation](https://render.com/docs)
- [Django Production Deployment](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Gunicorn Documentation](https://gunicorn.org/)

## Support

For deployment issues:
1. Check platform-specific logs
2. Verify all environment variables
3. Test API endpoints manually
4. Review error tracking (Sentry, etc.)
5. Contact platform support if needed
