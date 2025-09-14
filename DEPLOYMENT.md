# Facebook OAuth Callback Server

## Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

3. **Run locally**
   ```bash
   python local_server.py
   ```

4. **Test locally**
   - Health check: `http://localhost:8000/`
   - Callback URL: `http://localhost:8000/api/facebook/callback`

## Vercel Deployment

1. **Deploy to Vercel**
   ```bash
   npm i -g vercel
   vercel
   ```

2. **Set Environment Variables** in Vercel dashboard:
   ```
   FACEBOOK_APP_ID=your_facebook_app_id
   FACEBOOK_APP_SECRET=your_facebook_app_secret
   FACEBOOK_REDIRECT_URI=https://your-project-name.vercel.app/api/facebook/callback
   LE_CHAT_USER_ID=your_user_id
   ```

3. **Update Facebook App** redirect URI to:
   ```
   https://your-project-name.vercel.app/api/facebook/callback
   ```

## Files
- `local_server.py` - Local development server
- `api/index.py` - Vercel serverless function
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel configuration
- `env.example` - Environment variables template

## Test
- Local: `http://localhost:8000/api/facebook/callback`
- Vercel: `https://your-project-name.vercel.app/api/facebook/callback`

## Troubleshooting

### Vercel Function Crashes (500 Error)
If you see "FUNCTION_INVOCATION_FAILED", check:
1. Environment variables are set in Vercel dashboard
2. Visit `https://your-project-name.vercel.app/` to see health check
3. Check Vercel function logs in dashboard

### Health Check
Visit your domain root to see environment variable status:
```json
{
  "message": "Facebook OAuth Callback Server",
  "status": "running",
  "deployment": "vercel",
  "environment": {
    "facebook_app_id_set": true,
    "facebook_app_secret_set": true,
    "redirect_uri_set": true,
    "user_id_set": true
  }
}
```
