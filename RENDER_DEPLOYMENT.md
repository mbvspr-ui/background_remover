# Background Removal Service - Render Deployment Guide

## Overview
Deploy the background removal microservice to Render.com for production use.

## Prerequisites
- Render.com account (free tier available)
- GitHub repository with the background-removal-service code

## Deployment Steps

### Option 1: Deploy via Render Dashboard (Recommended)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com/
   - Sign in with your GitHub account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"

3. **Connect Repository**
   - Connect your GitHub account if not already connected
   - Select the repository: `mbvspr-ui/unicard-serverless`
   - Render will detect the `background-removal-service` directory

4. **Configure Service**
   ```
   Name: unicard-background-removal
   Region: Singapore (or closest to your users)
   Branch: main
   Root Directory: background-removal-service
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
   Plan: Free
   ```

5. **Environment Variables**
   Add these in the "Environment" section:
   ```
   PYTHON_VERSION=3.11.0
   DEBUG=false
   ```

6. **Advanced Settings**
   - Health Check Path: `/health`
   - Auto-Deploy: Yes (deploy on git push)

7. **Create Web Service**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes first time)

### Option 2: Deploy via render.yaml

1. **Push render.yaml to GitHub**
   ```bash
   cd unicard-serverless/background-removal-service
   git add render.yaml
   git commit -m "Add Render deployment config"
   git push origin main
   ```

2. **Create Service from Blueprint**
   - Go to Render Dashboard
   - Click "New +" → "Blueprint"
   - Select your repository
   - Render will detect `render.yaml`
   - Click "Apply"

## After Deployment

### 1. Get Your Service URL
After deployment completes, you'll get a URL like:
```
https://unicard-background-removal.onrender.com
```

### 2. Test the Service
```bash
# Health check
curl https://unicard-background-removal.onrender.com/health

# Test background removal
curl -X POST https://unicard-background-removal.onrender.com/remove-background \
  -F "image=@test-image.jpg" \
  -o output.png
```

### 3. Update Frontend Configuration

Update your school portal `.env` file:
```env
VITE_BG_REMOVAL_URL=https://unicard-background-removal.onrender.com
```

Update CORS in `app.py` to include your Render URL:
```python
CORS(app, origins=[
    'http://localhost:3000',
    'https://school.unicard-serverless.com',
    'https://unicard-background-removal.onrender.com'
])
```

## Important Notes

### Free Tier Limitations
- ⚠️ **Spins down after 15 minutes of inactivity**
- First request after spin-down takes 30-60 seconds
- 750 hours/month free (enough for one service)
- 512 MB RAM, 0.1 CPU

### Cold Start Handling
The service will "sleep" after 15 minutes of no requests. To handle this:

1. **Add Loading State in Frontend**
   ```typescript
   // Show "Processing... This may take up to 60 seconds on first use"
   ```

2. **Keep-Alive Ping (Optional)**
   Set up a cron job to ping the service every 14 minutes:
   ```bash
   # Use cron-job.org or similar
   curl https://unicard-background-removal.onrender.com/health
   ```

### Upgrade to Paid Plan
For production with no cold starts:
- **Starter Plan**: $7/month
  - No spin-down
  - 512 MB RAM
  - Always available

## Monitoring

### View Logs
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. View real-time logs

### Check Status
- Dashboard shows service status
- Health check endpoint: `/health`
- Metrics available in dashboard

## Troubleshooting

### Service Won't Start
**Check logs for:**
- Missing dependencies
- Python version mismatch
- Port binding issues

**Solution:**
```bash
# Verify requirements.txt is complete
pip install -r requirements.txt

# Test locally first
gunicorn app:app --bind 0.0.0.0:5000
```

### CORS Errors
**Update CORS origins in app.py:**
```python
CORS(app, origins=[
    'https://your-frontend-domain.com',
    'https://unicard-background-removal.onrender.com'
])
```

### Out of Memory
**Reduce image size before processing:**
```python
# Add to app.py
MAX_IMAGE_SIZE = (2048, 2048)
if input_image.size[0] > MAX_IMAGE_SIZE[0]:
    input_image.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
```

### Slow Performance
**Upgrade to paid plan** or **optimize:**
- Reduce image resolution
- Use image compression
- Cache results

## Alternative: Docker Deployment

If you prefer Docker:

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
   ```

2. **Deploy to Render**
   - Select "Docker" as runtime
   - Render will build from Dockerfile

## Cost Comparison

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | 750 hrs/month, spins down after 15 min |
| Starter | $7/month | Always on, 512 MB RAM |
| Standard | $25/month | 2 GB RAM, better performance |

## Security

### API Key Protection (Optional)
Add API key authentication:

```python
# app.py
API_KEY = os.getenv('API_KEY')

@app.before_request
def check_api_key():
    if request.endpoint != 'health_check':
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
```

Set `API_KEY` in Render environment variables.

## Next Steps

1. ✅ Deploy to Render
2. ✅ Test the service
3. ✅ Update frontend configuration
4. ✅ Monitor performance
5. ✅ Consider upgrading if needed

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com/
- Service Status: https://status.render.com/

---

**Ready to deploy!** Follow the steps above and your background removal service will be live in minutes.
