#!/usr/bin/env python3
"""
Vercel serverless function for Facebook OAuth callbacks
"""

import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Facebook App Configuration
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
FACEBOOK_REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI")
LE_CHAT_USER_ID = os.getenv("LE_CHAT_USER_ID")

def load_user_data():
    """Load user data - in serverless environment, this would be from a database"""
    return {}

def save_user_data(data):
    """Save user data - in serverless environment, this would be from a database"""
    print(f"User data to save: {json.dumps(data, indent=2)}")

def create_error_html(title, message):
    """Create error HTML page"""
    return f"""
    <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; text-align: center; }}
                .error {{ color: #d32f2f; }}
                .container {{ background-color: #ffebee; padding: 20px; border-radius: 8px; }}
                button {{ padding: 12px 24px; background-color: #d32f2f; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; margin-top: 15px; }}
                .countdown {{ font-size: 18px; font-weight: bold; color: #d32f2f; }}
            </style>
            <script>
                let countdown = 10;
                function updateCountdown() {{
                    document.getElementById('countdown').textContent = countdown;
                    countdown--;
                    if (countdown < 0) {{
                        closeWindow();
                    }}
                }}
                
                function closeWindow() {{
                    try {{
                        window.close();
                    }} catch(e) {{
                        alert('Please close this window manually (Ctrl+W or Cmd+W)');
                    }}
                }}
                
                window.onload = function() {{
                    setInterval(updateCountdown, 1000);
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h1 class="error">❌ {title}</h1>
                <p><strong>Error:</strong> {message}</p>
                <p class="countdown">This window will close automatically in <span id="countdown">10</span> seconds</p>
                <button onclick="closeWindow()">❌ Close Window</button>
                <p style="font-size: 12px; color: #666; margin-top: 10px;">
                    Or close manually with Ctrl+W (Windows) or Cmd+W (Mac)
                </p>
            </div>
        </body>
    </html>
    """

def create_success_html(pages_list, facebook_user_id):
    """Create success HTML page"""
    return f"""
    <html>
        <head>
            <title>Facebook Authorization Complete</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
                .success {{ color: #4CAF50; }}
                .container {{ text-align: center; }}
                ul {{ text-align: left; }}
                .countdown {{ font-size: 18px; font-weight: bold; color: #FF6B35; }}
            </style>
            <script>
                let countdown = 10;
                function updateCountdown() {{
                    document.getElementById('countdown').textContent = countdown;
                    countdown--;
                    if (countdown < 0) {{
                        closeWindow();
                    }}
                }}
                
                function closeWindow() {{
                    try {{
                        window.close();
                    }} catch(e) {{
                        alert('Please close this window manually (Ctrl+W or Cmd+W)');
                    }}
                }}
                
                window.onload = function() {{
                    setInterval(updateCountdown, 1000);
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h1 class="success">✅ Facebook Authorization Complete!</h1>
                <p>Successfully connected your Facebook account!</p>
                <h3>Available Pages:</h3>
                <ul>{pages_list}</ul>
                <p><strong>User ID:</strong> {facebook_user_id}</p>
                
                <div style="margin-top: 30px; padding: 20px; background-color: #f0f8ff; border-radius: 8px;">
                    <p style="font-size: 16px; color: #333; margin-bottom: 15px;">
                        ✅ <strong>Authorization Complete!</strong><br>
                        You can now use the Facebook posting tools in your MCP client!
                    </p>
                    <p class="countdown">This window will close automatically in <span id="countdown">10</span> seconds</p>
                    <button onclick="closeWindow()" style="padding: 12px 24px; background-color: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold;">
                        ✅ Close Window
                    </button>
                    <p style="font-size: 12px; color: #666; margin-top: 10px;">
                        Or close manually with Ctrl+W (Windows) or Cmd+W (Mac)
                    </p>
                </div>
            </div>
        </body>
    </html>
    """

def handle_facebook_callback(query_params):
    """Handle Facebook OAuth callback"""
    try:
        # Extract parameters
        code = query_params.get("code")
        error = query_params.get("error")
        
        if error:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': create_error_html("Authorization Failed", error)
            }
        
        if not code:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': create_error_html("Authorization Failed", "Missing authorization code")
            }
        
        # Exchange code for access token
        print(f"🔄 Exchanging authorization code for access token...")
        token_url = "https://graph.facebook.com/oauth/access_token"
        token_params = {
            'client_id': FACEBOOK_APP_ID,
            'client_secret': FACEBOOK_APP_SECRET,
            'redirect_uri': FACEBOOK_REDIRECT_URI,
            'code': code
        }
        
        response = requests.get(token_url, params=token_params)
        token_data = response.json()
        
        if 'access_token' not in token_data:
            error_msg = token_data.get('error', {}).get('message', 'Unknown error')
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': create_error_html("Token Exchange Failed", error_msg)
            }
        
        access_token = token_data['access_token']
        
        # Get user's pages
        pages_url = f"https://graph.facebook.com/me/accounts?access_token={access_token}"
        pages_response = requests.get(pages_url)
        pages_data = pages_response.json()
        
        if 'data' not in pages_data:
            error_msg = pages_data.get('error', {}).get('message', 'Unknown error')
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': create_error_html("Failed to Access Pages", error_msg)
            }
        
        # Save user data
        user_data = load_user_data()
        facebook_user_id = LE_CHAT_USER_ID
        user_data[facebook_user_id] = {
            'facebook_user_id': facebook_user_id,
            'access_token': access_token,
            'pages': pages_data['data']
        }
        save_user_data(user_data)
        
        # Create pages list for display
        pages_list = ""
        for page in pages_data['data']:
            pages_list += f"<li><strong>{page['name']}</strong> (ID: {page['id']})</li>"
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': create_success_html(pages_list, facebook_user_id)
        }
        
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': create_error_html("Error", str(e))
        }

def handler(request):
    """Vercel serverless function handler"""
    try:
        # Get path and query parameters
        path = request.get('path', '/')
        query_params = request.get('queryStringParameters', {}) or {}
        
        # Handle different endpoints
        if path == '/' or path == '/api':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    "message": "Facebook OAuth Callback Server",
                    "status": "running",
                    "deployment": "vercel",
                    "environment": {
                        "facebook_app_id_set": bool(FACEBOOK_APP_ID),
                        "facebook_app_secret_set": bool(FACEBOOK_APP_SECRET),
                        "redirect_uri_set": bool(FACEBOOK_REDIRECT_URI),
                        "user_id_set": bool(LE_CHAT_USER_ID)
                    }
                })
            }
        
        elif path == '/api/facebook/callback':
            return handle_facebook_callback(query_params)
        
        else:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "Not found", "path": path})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Internal server error", "message": str(e)})
        }