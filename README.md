# Background Removal Service

A Flask microservice for removing backgrounds from images using the rembg AI model.

## Overview

This service provides a simple HTTP API for removing backgrounds from images, returning PNG images with transparent backgrounds. It uses the u2net model from the rembg library for high-quality background removal.

## Features

- ✅ Remove backgrounds from JPEG/PNG images
- ✅ Accept multipart/form-data or JSON with base64 images
- ✅ Return PNG with transparent background as base64 data URL
- ✅ CORS enabled for frontend integration
- ✅ Health check endpoint
- ✅ Docker support for easy deployment
- ✅ Error handling and validation

## Tech Stack

- **Framework**: Flask 3.0
- **AI Model**: rembg (u2net)
- **Image Processing**: Pillow (PIL)
- **CORS**: flask-cors
- **Python**: 3.11

## Installation

### Local Development

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create .env file**:
```bash
cp .env.example .env
```

4. **Run the service**:
```bash
python app.py
```

The service will start on `http://localhost:5000`

### Docker Deployment

1. **Build Docker image**:
```bash
docker build -t background-removal-service .
```

2. **Run container**:
```bash
docker run -p 5000:5000 background-removal-service
```

## API Endpoints

### Health Check

Check if the service is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "ok",
  "service": "background-removal",
  "version": "1.0.0"
}
```

### Remove Background

Remove background from an image.

**Endpoint**: `POST /remove-background`

**Content-Type**: `multipart/form-data` or `application/json`

#### Option 1: File Upload (multipart/form-data)

**Request**:
```bash
curl -X POST http://localhost:5000/remove-background \
  -F "image=@photo.jpg"
```

#### Option 2: Base64 JSON

**Request**:
```bash
curl -X POST http://localhost:5000/remove-background \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
  }'
```

**Success Response (200)**:
```json
{
  "success": true,
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "format": "png"
}
```

**Error Response (400/500)**:
```json
{
  "success": false,
  "error": "Error message"
}
```

## Usage Examples

### JavaScript/TypeScript

```typescript
// Using File Upload
const removeBackground = async (file: File) => {
  const formData = new FormData();
  formData.append('image', file);

  const response = await fetch('http://localhost:5000/remove-background', {
    method: 'POST',
    body: formData
  });

  const data = await response.json();
  return data.image; // Base64 data URL
};

// Using Base64
const removeBackgroundBase64 = async (base64Image: string) => {
  const response = await fetch('http://localhost:5000/remove-background', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image: base64Image })
  });

  const data = await response.json();
  return data.image; // Base64 data URL
};
```

### Python

```python
import requests

# Using file upload
def remove_background_file(image_path):
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(
            'http://localhost:5000/remove-background',
            files=files
        )
    return response.json()

# Using base64
def remove_background_base64(base64_image):
    response = requests.post(
        'http://localhost:5000/remove-background',
        json={'image': base64_image}
    )
    return response.json()
```

### cURL

```bash
# File upload
curl -X POST http://localhost:5000/remove-background \
  -F "image=@student-photo.jpg" \
  -o response.json

# Base64 JSON
curl -X POST http://localhost:5000/remove-background \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/jpeg;base64,/9j/4AAQ..."}' \
  -o response.json
```

## Deployment

### Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3.11
4. Add environment variables:
   - `PORT`: 5000
   - `DEBUG`: False
5. Deploy

### Railway

1. Create a new project on Railway
2. Connect your GitHub repository
3. Railway will auto-detect Python and use the Dockerfile
4. Add environment variables:
   - `PORT`: 5000
   - `DEBUG`: False
5. Deploy

### Heroku

1. Create a new app on Heroku
2. Add Python buildpack
3. Create `Procfile`:
```
web: python app.py
```
4. Deploy via Git or GitHub integration

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port to run the service on | 5000 |
| `DEBUG` | Enable Flask debug mode | False |

## Performance

- **Processing Time**: 2-3 seconds per image (depends on image size)
- **Memory Usage**: ~500MB (model loaded in memory)
- **Supported Formats**: JPEG, PNG
- **Max Image Size**: Limited by available memory

## Error Handling

The service handles the following errors:

- **400 Bad Request**: Invalid image format or missing image data
- **500 Internal Server Error**: Background removal processing failed
- **404 Not Found**: Invalid endpoint

All errors return JSON with:
```json
{
  "success": false,
  "error": "Error message"
}
```

## CORS Configuration

CORS is enabled for the following origins:
- `http://localhost:3000` (School Portal dev)
- `http://localhost:3002` (Admin Portal dev)
- `https://school.unicard-serverless.com` (Production)
- `https://admin.unicard-serverless.com` (Production)

## Model Information

The service uses the **u2net** model from rembg:
- High-quality background removal
- Works well with portraits and objects
- Trained on diverse datasets
- No GPU required (CPU inference)

## Troubleshooting

### Service won't start

Check if port 5000 is already in use:
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

### Out of memory errors

The rembg model requires ~500MB of RAM. Ensure your deployment environment has sufficient memory.

### Slow processing

Background removal is CPU-intensive. For faster processing:
- Use a deployment platform with better CPU
- Consider GPU-enabled hosting for production
- Implement request queuing for high load

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

### Code Formatting

```bash
# Install formatting tools
pip install black flake8

# Format code
black app.py

# Check linting
flake8 app.py
```

## License

Proprietary - All rights reserved

## Support

For issues or questions, contact the development team.

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release
- Background removal with rembg
- File upload and base64 support
- Docker deployment support
- Health check endpoint
