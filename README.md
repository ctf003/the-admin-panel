# The Admin Panel That Isn't

## Challenge Description
We found an old internal tool running on this server. The admin has something we need. Can you get in?

## Deployment

```bash
export FLAG="flag{your_flag_here}"
docker-compose up -d
```

Access at: http://localhost:8080

## Solution Path

The challenge contains a second-order SSTI vulnerability in the display_name field during registration. The name is stored unsafely and rendered via render_template_string() on the dashboard.

Players must:
1. Register with SSTI payload in display_name
2. Login and access dashboard
3. Exploit Jinja2 SSTI via __mro__/__subclasses__() chain
4. Read os.environ['FLAG']

## Red Herrings

1. Fake SQL injection vulnerability in login form
2. JWT with role field suggesting privilege escalation
3. robots.txt pointing to backup.zip with admin credentials
4. Admin panel showing fake canary flag

## Technical Stack

- Python 3.11
- Flask + SQLAlchemy
- Redis (rate limiting)
- nginx (reverse proxy)
- Gunicorn (WSGI server)
