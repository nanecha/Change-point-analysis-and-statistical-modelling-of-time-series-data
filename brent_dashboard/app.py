# app.py
from flask import Flask, send_from_directory
from api import register_api_routes
import os

app = Flask(__name__, static_folder='static')

# Register API routes
register_api_routes(app)

@app.route('/')
def serve_index():
    """Serve the Vite-built index.html."""
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from Vite build."""
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)