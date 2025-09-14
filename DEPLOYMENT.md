# Vercel Deployment Guide

This guide will help you deploy your Facebook OAuth callback server to Vercel.

## Prerequisites

1. A Vercel account (free tier is sufficient)
2. Facebook App credentials
3. Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### 1. Prepare Your Repository

Make sure all files are committed to your Git repository:
- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies
- `api/index.py` - Main serverless function
- `env.example` - Environment variables template

### 2. Deploy to Vercel

#### Option A: Deploy via Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow the prompts to configure your project
```

#### Option B: Deploy via Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your Git repository
4. Vercel will automatically detect the Python configuration

### 3. Configure Environment Variables

In your Vercel dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variables:

```
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_REDIRECT_URI=https://your-project-name.vercel.app/api/facebook/callback
LE_CHAT_USER_ID=your_user_id
```

### 4. Update Facebook App Settings

1. Go to your Facebook App dashboard
2. Navigate to "Facebook Login" > "Settings"
3. Update the "Valid OAuth Redirect URIs" to include:
   ```
   https://your-project-name.vercel.app/api/facebook/callback
   ```

### 5. Test Your Deployment

1. Visit your deployed URL: `https://your-project-name.vercel.app`
2. You should see: `{"message": "Facebook OAuth Callback Server", "status": "running", "deployment": "vercel"}`
3. Test the callback endpoint: `https://your-project-name.vercel.app/api/facebook/callback`

## Local Development

To run locally for development:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (copy from env.example)
cp env.example .env
# Edit .env with your actual values

# Run the server
python main.py
```

## Important Notes

### Data Storage
- The current implementation uses in-memory storage for demo purposes
- For production use, implement proper database storage (e.g., PostgreSQL, MongoDB)
- Consider using Vercel's serverless database solutions

### Security
- Never commit your `.env` file
- Use Vercel's environment variables for production secrets
- Consider implementing rate limiting and request validation

### Facebook App Configuration
- Ensure your Facebook App is in "Live" mode for production
- Configure proper app domains and redirect URIs
- Review Facebook's OAuth security requirements

## Troubleshooting

### Common Issues

1. **Environment Variables Not Loading**
   - Check that variables are set in Vercel dashboard
   - Redeploy after adding new environment variables

2. **Facebook OAuth Errors**
   - Verify redirect URI matches exactly
   - Check Facebook App settings and permissions

3. **Function Timeout**
   - Vercel has a 30-second timeout for hobby plans
   - Consider optimizing API calls or upgrading plan

### Debugging

Check Vercel function logs:
1. Go to your project dashboard
2. Click on "Functions" tab
3. View logs for debugging

## Production Considerations

1. **Database Integration**
   - Replace in-memory storage with persistent database
   - Consider Vercel Postgres or external database service

2. **Monitoring**
   - Set up error tracking (Sentry, etc.)
   - Monitor function performance and costs

3. **Scaling**
   - Vercel automatically scales serverless functions
   - Monitor usage and costs as you scale

## Support

For issues specific to:
- Vercel: Check [Vercel documentation](https://vercel.com/docs)
- Facebook API: Check [Facebook Developer documentation](https://developers.facebook.com/docs/)
- This project: Check the main README.md
