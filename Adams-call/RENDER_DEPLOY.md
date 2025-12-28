# Deploying Adams-call to Render

## 🚀 Quick Deploy

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect to Render:**
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the `Adams-call` directory (or root if Adams-call is root)
   - Render will auto-detect `render.yaml` and configure everything
   - Click "Apply"

3. **Wait for deployment:**
   - Render will build and deploy automatically
   - You'll get a URL like `https://adams-call-webrtc.onrender.com`

### Option 2: Manual Setup

1. **Create New Web Service:**
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service:**
   - **Name:** `adams-call-webrtc`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m server.main`
   - **Plan:** Free (or paid for better performance)

3. **Environment Variables:**
   Add these in the Render dashboard:
   - `HOST` = `0.0.0.0`
   - `PORT` = (leave empty, Render sets this automatically)
   - `JWT_SECRET_KEY` = (generate a random string or let Render generate it)
   - `PYTHON_VERSION` = `3.11.0`

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for the build to complete

## ⚠️ Important Notes

### SSL/HTTPS
- Render provides automatic HTTPS
- The self-signed certificate generation in `main.py` won't work on Render
- You need to modify the code to skip SSL in production (see below)

### WebRTC Requirements
- WebRTC requires HTTPS (Render provides this automatically)
- STUN/TURN servers may be needed for connections across different networks
- The current setup uses public STUN servers which should work

### Free Tier Limitations
- Free tier services spin down after 15 minutes of inactivity
- First request after spindown takes 30-60 seconds
- Upgrade to paid tier ($7/month) for always-on service

## 🔧 Required Code Changes

The current code generates SSL certificates for local development. On Render, SSL is handled by their infrastructure. You need to modify `server/main.py`:

### Option A: Conditional SSL (Development vs Production)

Add this to detect production environment:

```python
import os

# At the top with other imports
RENDER_PRODUCTION = os.environ.get("RENDER", False)

# In main() function, modify SSL setup:
def main():
    # ... existing code ...
    
    app = create_app()
    
    if RENDER_PRODUCTION:
        # Production: Render handles SSL
        print(f"🚀 Server starting on http://{HOST}:{PORT} (SSL handled by Render)")
        web.run_app(app, host=HOST, port=PORT)
    else:
        # Development: Use self-signed certificates
        key_path, cert_path = generate_ssl_certs()
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(str(cert_path), str(key_path))
        print(f"🚀 Server starting on https://{HOST}:{PORT}")
        web.run_app(app, host=HOST, port=PORT, ssl_context=ssl_context)
```

Then add `RENDER=True` to Render environment variables.

### Option B: Check for Render Environment Variable

Render automatically sets `RENDER=True`, so you can check for it:

```python
# In main() function:
if os.environ.get("RENDER"):
    # Production mode - no SSL context needed
    web.run_app(app, host=HOST, port=PORT)
else:
    # Development mode - use SSL
    key_path, cert_path = generate_ssl_certs()
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(str(cert_path), str(key_path))
    web.run_app(app, host=HOST, port=PORT, ssl_context=ssl_context)
```

## 📝 Post-Deployment

1. **Test Your App:**
   - Visit your Render URL
   - Create an account and test video/audio calls
   - Test with multiple users

2. **Monitor Logs:**
   - Use Render dashboard to view logs
   - Check for any errors or issues

3. **Custom Domain (Optional):**
   - Render allows custom domains on all plans
   - Configure in the Render dashboard under "Settings" → "Custom Domain"

## 🐛 Troubleshooting

- **Build fails:** Check `requirements.txt` has all dependencies
- **App crashes:** Check logs in Render dashboard
- **WebRTC not connecting:** Ensure HTTPS is working, may need TURN server for some networks
- **Slow startup:** Free tier limitation, upgrade for faster cold starts

## 💡 Tips

1. Enable auto-deploy for automatic updates when you push to GitHub
2. Use environment variables for sensitive config
3. Monitor your app's performance in Render dashboard
4. Consider upgrading to paid tier for production use

## 📞 Support

For Render-specific issues, check:
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
