# Quick Start Guide

## ✅ Repository Status

**GitHub**: https://github.com/ctf003/the-admin-panel
**Status**: Successfully pushed ✅

## 🚀 Deploy to Render (Recommended)

### Step 1: Go to Render
Visit: https://dashboard.render.com/

### Step 2: Create New Blueprint
1. Click **"New +"** → **"Blueprint"**
2. Connect GitHub if not already connected
3. Select repository: **ctf003/the-admin-panel**
4. Render will detect `render.yaml` automatically

### Step 3: Set Environment Variable
Add this environment variable:
- **Key**: `FLAG`
- **Value**: `flag{your_actual_flag_here}`

### Step 4: Deploy
Click **"Apply"** and wait 3-5 minutes for deployment.

### Step 5: Access Your Challenge
Your URL will be: `https://admin-panel-ctf.onrender.com`

**That's it!** 🎉

---

## 📋 What Gets Deployed

Render will automatically create:
- ✅ Web service (Flask app)
- ✅ Redis instance (for rate limiting)
- ✅ HTTPS certificate (free SSL)
- ✅ Health monitoring

---

## 🧪 Test Your Deployment

```bash
# Replace with your Render URL
URL="https://admin-panel-ctf.onrender.com"

# Test main page
curl $URL/

# Test robots.txt
curl $URL/robots.txt

# Test backup download
curl -O $URL/static/secret-backup.zip
```

---

## 🎯 Challenge Info

**Name**: The Admin Panel That Isn't
**Category**: Web Exploitation
**Difficulty**: Intermediate+
**Vulnerability**: Second-order SSTI

**Description for participants**:
```
We found an old internal tool running on this server. 
The admin has something we need. Can you get in?
```

---

## 📚 Documentation

- **Full Deployment Guide**: [RENDER_DEPLOY.md](RENDER_DEPLOY.md)
- **Solution Walkthrough**: [SOLUTION.md](SOLUTION.md)
- **Challenge Details**: [CHALLENGE.md](CHALLENGE.md)
- **Docker Deployment**: [DEPLOY.md](DEPLOY.md)

---

## ⚠️ Important Notes

### Free Tier Limitations
- Service spins down after 15 minutes of inactivity
- First request after spin down takes 30-60 seconds
- 750 hours/month free (sufficient for most CTFs)

### For Production CTF Events
Consider upgrading to Starter plan ($7/month) for:
- No spin down
- Faster response times
- Better reliability

---

## 🔧 Troubleshooting

### Service Won't Start
1. Check Render logs: Dashboard → Your Service → Logs
2. Verify FLAG environment variable is set
3. Ensure Redis instance is running

### SSTI Not Working
1. Test with simple payload: `{{7*7}}`
2. Check display_name is being stored
3. Verify you're logged in and viewing dashboard

### Rate Limiting Issues
1. Verify Redis instance is running
2. Check REDIS_URL environment variable
3. View Redis logs for connection errors

---

## 📞 Support

- **GitHub Issues**: https://github.com/ctf003/the-admin-panel/issues
- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com/

---

## 🎓 Next Steps

After deployment:

1. ✅ Test all endpoints
2. ✅ Verify SSTI works (register with `{{7*7}}`)
3. ✅ Test admin login (admin:p@ssw0rd123)
4. ✅ Verify rate limiting
5. ✅ Share URL with CTF participants

---

**Deployment Time**: ~5 minutes
**Cost**: Free (or $14/month for production)
**Difficulty**: Easy ⭐

Happy hacking! 🚀
