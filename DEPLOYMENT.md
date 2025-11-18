# Background Removal Service Deployment Guide

## Overview
This guide covers deploying the Python Flask background removal service to Render or Railway.

## Prerequisites
- Docker installed (for local testing)
- Render or Railway account
- GitHub repository (recommended)

## Option 1: Deploy to Render

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up or log in
3. Connect your GitHub account

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your repository
3. Select the `unicard-serverless/background-removal-service` directory

### Step 3: Configure Service
```
Name: unicard-bg-removal
Environment: Python 3
Region: Choose closest to your users
Branch: main
Root Directory: unicard-serverless/background-removal-service
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

### Step 4: Set Environment Variables
```
PORT=5000
DEBUG=False
PYTHON_VERSION=3.11.0
```

### Step 5: Configure Instance
- Instance Type: Starter ($7/month) or Free
- Auto-Deploy: Yes

### Step 6: Deploy
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes first time)
3. Note the service URL: `https://unicard-bg-removal.onrender.com`

### Step 7: Test Deployment
```bash
curl https://unicard-bg-removal.onrender.com/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "background-removal",
  "version": "1.0.0"
}
```

## Option 2: Deploy to Railway

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up or log in with GitHub

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository

### Step 3: Configure Service
1. Railway will auto-detect Python
2. Set root directory: `unicard-serverless/background-removal-service`

### Step 4: Set Environment Variables
```
PORT=5000
DEBUG=False
```

### Step 5: Configure Build
Railway auto-detects:
- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`

### Step 6: Deploy
1. Click "Deploy"
2. Wait for deployment
3. Generate domain: Settings → Generate Domain
4. Note the service URL: `https://unicard-bg-removal.up.railway.app`

### Step 7: Test Deployment
```bash
curl https://unicard-bg-removal.up.railway.app/health
```

## Local Testing with Docker

### Build Image
```bash
cd unicard-serverless/background-removal-service
docker build -t unicard-bg-removal .
```

### Run Container
```bash
docker run -p 5000:5000 unicard-bg-removal
```

### Test Locally
```bash
curl http://localhost:5000/health
```

## Update Environment Variables in Portals

After deployment, update the environment variables in both portals:

### School Portal
```env
VITE_BG_REMOVAL_URL=https://your-service-url.com
```

### API (if needed)
```env
BG_REMOVAL_URL=https://your-service-url.com
```

## Performance Considerations

### Cold Starts
- First request after inactivity may take 10-30 seconds
- Consider using a paid tier to avoid cold starts
- Implement keep-alive pings if needed

### Memory Requirements
- Minimum: 512MB RAM
- Recommended: 1GB RAM
- The rembg model requires significant memory

### Scaling
- Render: Auto-scales with paid plans
- Railway: Manual scaling configuration
- Consider horizontal scaling for high traffic

## Monitoring

### Health Checks
Set up health check endpoint:
- URL: `/health`
- Interval: 60 seconds
- Timeout: 10 seconds

### Logs
- Render: View logs in dashboard
- Railway: View logs in project dashboard
- Monitor for errors and performance issues

### Metrics to Monitor
- Response time (target: < 3 seconds)
- Error rate (target: < 1%)
- Memory usage
- CPU usage

## Troubleshooting

### Service Won't Start
1. Check logs for errors
2. Verify Python version (3.11)
3. Ensure all dependencies installed
4. Check PORT environment variable

### Out of Memory
1. Upgrade to larger instance
2. Optimize image processing
3. Implement request queuing

### Slow Response Times
1. Check instance resources
2. Optimize model loading
3. Consider caching
4. Upgrade instance type

### CORS Errors
1. Verify CORS configuration in app.py
2. Check allowed origins
3. Ensure proper headers

## Security

### Best Practices
- Use HTTPS only
- Implement rate limiting
- Validate file uploads
- Set file size limits
- Monitor for abuse

### Environment Variables
Never commit:
- API keys
- Secrets
- Database credentials

## Cost Estimates

### Render
- Free tier: Limited hours/month
- Starter: $7/month
- Standard: $25/month

### Railway
- Free tier: $5 credit/month
- Pay as you go: ~$5-20/month

## Maintenance

### Updates
1. Update dependencies regularly
2. Monitor security advisories
3. Test updates in staging first
4. Deploy during low-traffic periods

### Backups
- Code is in Git (no data to backup)
- Document configuration
- Keep deployment scripts updated

## Support

For issues:
1. Check service logs
2. Review error messages
3. Test health endpoint
4. Verify environment variables
5. Contact platform support if needed
