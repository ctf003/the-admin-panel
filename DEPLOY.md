# Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- Port 8080 available

## Quick Start

1. Set the flag environment variable:
```bash
export FLAG="flag{your_actual_flag_here}"
```

2. Build and start the challenge:
```bash
cd web-challenge
docker-compose up -d --build
```

3. Verify deployment:
```bash
curl http://localhost:8080/
```

## Stopping the Challenge

```bash
docker-compose down
```

## Verification Checklist

After deployment, verify:

- [ ] Main page loads at http://localhost:8080/
- [ ] Registration requires proof-of-work (JavaScript enabled)
- [ ] Login with SQLi payloads returns fake error
- [ ] /robots.txt is accessible
- [ ] /static/secret-backup.zip downloads
- [ ] Admin credentials (admin:p@ssw0rd123) work
- [ ] /admin shows canary flag for admin role
- [ ] SSTI test: register with {{7*7}}, see 49 on dashboard
- [ ] Rate limiting works (6th registration blocked)

## Troubleshooting

### Container won't start
Check FLAG is set: `echo $FLAG`

### Database errors
The database is created in /tmp inside the container (tmpfs mount)

### Rate limiting not working
Ensure Redis container is running: `docker-compose ps`

## Security Notes

- Container runs as non-root user (ctfuser, UID 1001)
- Filesystem is read-only except /tmp
- No outbound internet access from app container
- Resource limits: 256MB RAM, 0.5 CPU
