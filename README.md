# Background Removal Service

A Flask microservice for removing backgrounds from images using the `rembg` library.

## Features

- ✅ Remove background from images
- ✅ Support for multiple image formats (JPEG, PNG, WebP)
- ✅ Base64 and file upload support
- ✅ CORS enabled for web applications
- ✅ Health check endpoint
- ✅ Production-ready with Gunicorn

## Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Service**
   ```bash
   python app.py
   ```

3. **Test the Service**
   ```bash
   curl http://localhost:5000/health
   ```

### Production Deployment

See [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md) for detailed deployment instructions to Render.com.

## API Endpoints

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "service": "background-removal",
  "version": "1.0.0"
}
```

### Remove Background
```
POST /remove-background
```

**Request (File Upload):**
```bash
curl -X POST http://localhost:5000/remove-background \
  -F "image=@photo.jpg" \
  -o output.png
```

**Request (JSON with Base64):**
```bash
curl -X POST http://localhost:5000/remove-background \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/jpeg;base64,/9j/4AAQ..."}'
```

**Response:**
```json
{
  "success": true,
  "image": "data:image/png;base64,iVBORw0KGgo...",
  "format": "png"
}
```

## Configuration

Environment variables (create `.env` file):

```env
PORT=5000
DEBUG=false
```

## Technology Stack

- **Flask**: Web framework
- **rembg**: Background removal library
- **Pillow**: Image processing
- **Gunicorn**: Production WSGI server
- **Flask-CORS**: Cross-origin resource sharing

## Performance

- **Processing Time**: 2-5 seconds per image (depends on size)
- **Max Image Size**: Recommended 2048x2048 pixels
- **Supported Formats**: JPEG, PNG, WebP, BMP

## Deployment

### Render.com (Recommended)
- Free tier available
- Auto-scaling
- Easy deployment
- See [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md)

### Docker
```bash
docker build -t bg-removal .
docker run -p 5000:5000 bg-removal
```

### Railway (Alternative)
```bash
railway up
```

## Troubleshooting

### Service is slow
- Reduce image size before uploading
- Use image compression
- Upgrade to paid hosting plan

### CORS errors
- Add your domain to CORS origins in `app.py`
- Check browser console for specific error

### Out of memory
- Reduce `MAX_IMAGE_SIZE` in app.py
- Upgrade hosting plan

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
