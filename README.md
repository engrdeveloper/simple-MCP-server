# Facebook OAuth Callback Server

A simple FastAPI server for handling Facebook OAuth callbacks, ready for both local development and Vercel deployment.

## Quick Start

### Local Development
```bash
pip install -r requirements.txt
cp env.example .env
# Edit .env with your Facebook app credentials
python index.py
```

### Vercel Deployment
```bash
npm i -g vercel
vercel
```

See `DEPLOYMENT.md` for detailed instructions.
