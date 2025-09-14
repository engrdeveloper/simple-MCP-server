#!/usr/bin/env python3
"""
Local development server for Facebook OAuth callbacks
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Facebook App Configuration
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
FACEBOOK_REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:8000/api/facebook/callback")
LE_CHAT_USER_ID = os.getenv("LE_CHAT_USER_ID")

class FacebookCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "message": "Facebook OAuth Callback Server",
                "status": "running",
                "deployment": "local",
                "environment": {
                    "facebook_app_id_set": bool(FACEBOOK_APP_ID),
                    "facebook_app_secret_set": bool(FACEBOOK_APP_SECRET),
                    "redirect_uri_set": bool(FACEBOOK_REDIRECT_URI),
                    "user_id_set": bool(LE_CHAT_USER_ID)
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif parsed_path.path == '/api/facebook/callback':
            query_params = parse_qs(parsed_path.query)
            # Convert list values to single values
            query_params = {k: v[0] if v else None for k, v in query_params.items()}
            
            # Import the handler from api/index.py
            import sys
            sys.path.append('api')
            from index import handle_facebook_callback
            
            result = handle_facebook_callback(query_params)
            
            self.send_response(result['statusCode'])
            for header, value in result['headers'].items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(result['body'].encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found", "path": parsed_path.path}
            self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer(('localhost', port), FacebookCallbackHandler)
    
    print(f"🚀 Starting Facebook OAuth Callback Server on port {port}")
    print(f"📍 Callback URL: http://localhost:{port}/api/facebook/callback")
    print(f"📊 Health check: http://localhost:{port}/")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()
