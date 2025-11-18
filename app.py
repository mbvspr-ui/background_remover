"""
Background Removal Service
A Flask microservice for removing backgrounds from images using rembg
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, origins=[
    'http://localhost:3000',
    'http://localhost:3002',
    'https://school.unicard-serverless.com',
    'https://admin.unicard-serverless.com'
])

# Configuration
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'background-removal',
        'version': '1.0.0'
    }), 200

@app.route('/remove-background', methods=['POST'])
def remove_background():
    """
    Remove background from an image
    
    Accepts:
    - multipart/form-data with 'image' file
    - JSON with 'image' as base64 data URL
    
    Returns:
    - JSON with 'image' as base64 data URL (PNG with transparent background)
    """
    try:
        # Get image from request
        image_data = None
        
        # Check if it's a file upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No file selected'
                }), 400
            
            # Read file data
            image_data = file.read()
        
        # Check if it's JSON with base64 image
        elif request.is_json:
            data = request.get_json()
            if 'image' not in data:
                return jsonify({
                    'success': False,
                    'error': 'No image data provided'
                }), 400
            
            # Handle base64 data URL
            image_str = data['image']
            if image_str.startswith('data:image'):
                # Remove data URL prefix
                image_str = image_str.split(',')[1]
            
            # Decode base64
            try:
                image_data = base64.b64decode(image_str)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid base64 image data: {str(e)}'
                }), 400
        
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid request format. Send multipart/form-data or JSON with base64 image'
            }), 400
        
        if not image_data:
            return jsonify({
                'success': False,
                'error': 'No image data received'
            }), 400
        
        # Open image
        try:
            input_image = Image.open(io.BytesIO(image_data))
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Invalid image format: {str(e)}'
            }), 400
        
        # Remove background using rembg
        try:
            output_image = remove(input_image)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Background removal failed: {str(e)}'
            }), 500
        
        # Convert to PNG bytes
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_bytes = output_buffer.getvalue()
        
        # Encode to base64
        output_base64 = base64.b64encode(output_bytes).decode('utf-8')
        
        # Create data URL
        data_url = f'data:image/png;base64,{output_base64}'
        
        return jsonify({
            'success': True,
            'image': data_url,
            'format': 'png'
        }), 200
    
    except Exception as e:
        app.logger.error(f'Error in remove_background: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print(f'🚀 Background Removal Service starting on port {PORT}')
    print(f'📍 Health check: http://localhost:{PORT}/health')
    print(f'📍 Remove background: http://localhost:{PORT}/remove-background')
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
