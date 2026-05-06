# Deploy to Render

This guide explains how to deploy "The Admin Panel That Isn't" CTF challenge to Render.

## Prerequisites

- GitHub account with the repository pushed
- Render account (free tier works)
- Repository URL: https://github.com/ctf003/the-admin-panel

## Deployment Options

### Option 1: Using render.yaml (Recommended)

This automatically creates both the web service and Redis instance.

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com/

2. **Create New Blueprint**
   - Click "New +" → "Blueprint"
   - Connect your GitHub account if not already connected
   - Select repository: `ctf003/the-admin-panel`
   - Render will detect `render.yaml` automatically

3. **Configure Environment Variables**
   - Service name: `admin-panel-ctf`
   - Add environment variable:
     - Key: `FLAG`
     - Value: `flag{your_actual_flag_here}`
   - Click "Apply"

4. **Deploy**
   - Render will automatically:
     - Create Redis instance
     - Build Docker image
     - Deploy web service
     - Connect services

5. **Access Your Challenge**
   - URL will be: `https://admin-panel-ctf.onrender.com`
   - Wait 2-3 minutes for initial build

### Option 2: Manual Setup

If you prefer manual control:

#### Step 1: Create Redis Instance

1. Go to Render Dashboard
2. Click "New +" → "Redis"
3. Configure:
   - Name: `admin-panel-redis`
   - Plan: Free
   - Max Memory Policy: `noeviction`
4. Click "Create Redis"
5. Copy the **Internal Redis URL** (starts with `redis://`)

#### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect repository: `ctf003/the-admin-panel`
3. Configure:
   - **Name**: `admin-panel-ctf`
   - **Environment**: Docker
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Dockerfile Path**: `./Dockerfile.render`
   - **Plan**: Free

4. **Environment Variables**:
   ```
   FLAG=flag{your_actual_flag_here}
   REDIS_URL=<paste-internal-redis-url-from-step-1>
   ```

5. Click "Create Web Service"

## Important Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `FLAG` | Yes | The CTF flag | `flag{s3c0nd_0rd3r_sst1}` |
| `REDIS_URL` | Auto | Redis connection (auto-set with Blueprint) | `redis://red-xxx:6379` |
| `PORT` | Auto | Port (Render sets this automatically) | `10000` |

### Health Check

Render will automatically check `/` endpoint for health status.

## Verification

After deployment, test these endpoints:

```bash
# Replace with your Render URL
RENDER_URL="https://admin-panel-ctf.onrender.com"

# Test main page
curl $RENDER_URL/

# Test robots.txt
curl $RENDER_URL/robots.txt

# Test backup download
curl -O $RENDER_URL/static/secret-backup.zip
```

## Render-Specific Considerations

### Free Tier Limitations

- **Spin down after 15 minutes of inactivity**
  - First request after spin down takes 30-60 seconds
  - Consider upgrading to paid plan for CTF events

- **750 hours/month free**
  - Sufficient for most CTF events
  - Monitor usage in dashboard

- **No persistent storage**
  - Database is in-memory (tmpfs)
  - Resets on each deployment/restart
  - This is intentional for the challenge

### Performance

- **Cold starts**: 30-60 seconds on free tier
- **Active response**: < 100ms
- **Concurrent users**: ~50-100 on free tier
- **Rate limiting**: Enforced via Redis

### Scaling for Large CTFs

If expecting > 100 concurrent users:

1. **Upgrade to Starter Plan** ($7/month)
   - No spin down
   - Faster cold starts
   - Better performance

2. **Upgrade Redis** to Starter ($7/month)
   - More memory
   - Better rate limiting

3. **Add Multiple Instances**
   - Deploy to multiple regions
   - Use different subdomains
   - Distribute load

## Troubleshooting

### Service Won't Start

**Check logs**:
```
Render Dashboard → Your Service → Logs
```

**Common issues**:
1. `FLAG environment variable is not set`
   - Solution: Add FLAG in environment variables

2. `Redis connection failed`
   - Solution: Check REDIS_URL is set correctly
   - Verify Redis instance is running

3. `Port binding error`
   - Solution: Ensure Dockerfile.render uses $PORT variable

### Rate Limiting Not Working

- Verify Redis instance is running
- Check REDIS_URL environment variable
- View Redis logs for connection errors

### SSTI Not Working

- Verify you're registering with correct payload
- Check that display_name is being stored
- Test with simple payload: `{{7*7}}`

### Slow Response Times

- Free tier spins down after 15 minutes
- First request wakes up service (30-60s)
- Subsequent requests are fast
- Consider paid plan for CTF events

## Monitoring

### View Logs

```
Render Dashboard → admin-panel-ctf → Logs
```

### Metrics

```
Render Dashboard → admin-panel-ctf → Metrics
```

Monitor:
- Request rate
- Response times
- Memory usage
- CPU usage

### Alerts

Set up alerts for:
- Service down
- High error rate
- Memory/CPU limits

## Security Notes

### Render Security Features

✅ **Automatic HTTPS**: All Render services get free SSL
✅ **DDoS Protection**: Built-in at infrastructure level
✅ **Network Isolation**: Services isolated by default
✅ **Secrets Management**: Environment variables encrypted

### Additional Hardening

For production CTF:

1. **Custom Domain**
   - Add your own domain
   - Hides Render infrastructure

2. **Access Control**
   - Use Render's IP allowlist
   - Restrict to CTF network

3. **Monitoring**
   - Set up external monitoring
   - Alert on anomalies

## Cost Estimate

### Free Tier (Recommended for Testing)
- Web Service: Free (750 hours/month)
- Redis: Free (25MB)
- **Total**: $0/month

### Starter Tier (Recommended for CTF Events)
- Web Service: $7/month (no spin down)
- Redis: $7/month (better performance)
- **Total**: $14/month

### Professional Tier (Large CTFs)
- Web Service: $25/month (more resources)
- Redis: $25/month (more memory)
- **Total**: $50/month

## Deployment Checklist

Before going live:

- [ ] Repository pushed to GitHub
- [ ] FLAG environment variable set
- [ ] Redis instance created and connected
- [ ] Web service deployed successfully
- [ ] Health check passing
- [ ] Test registration with PoW
- [ ] Verify SSTI with {{7*7}}
- [ ] Test admin login (admin:p@ssw0rd123)
- [ ] Verify /admin shows canary flag
- [ ] Test rate limiting
- [ ] Download and verify backup.zip
- [ ] Check all documentation links work

## Post-Deployment

### Share with Participants

```
Challenge: The Admin Panel That Isn't
URL: https://admin-panel-ctf.onrender.com
Description: We found an old internal tool running on this server. 
             The admin has something we need. Can you get in?
```

### Monitor During CTF

- Watch logs for errors
- Monitor resource usage
- Check for abuse/attacks
- Be ready to scale if needed

### After CTF

- Download logs for analysis
- Review solve statistics
- Collect feedback
- Consider keeping deployed for practice

## Alternative: Deploy Multiple Instances

For redundancy:

```bash
# Deploy to multiple regions
1. US East: admin-panel-ctf-us
2. EU West: admin-panel-ctf-eu
3. Asia: admin-panel-ctf-asia
```

Share all URLs with participants for load distribution.

## Support

If you encounter issues:

1. Check Render Status: https://status.render.com/
2. Render Docs: https://render.com/docs
3. Render Community: https://community.render.com/
4. GitHub Issues: https://github.com/ctf003/the-admin-panel/issues

---

**Quick Deploy**: Click "Deploy to Render" button (if configured) or follow Option 1 above.

**Estimated Setup Time**: 5-10 minutes
**First Deploy Time**: 3-5 minutes
**Cold Start Time**: 30-60 seconds (free tier)
