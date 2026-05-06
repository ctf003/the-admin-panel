# Challenge: The Admin Panel That Isn't

## Category
Web Exploitation

## Difficulty
Intermediate+

## Points
500

## Description
We found an old internal tool running on this server. The admin has something we need. Can you get in?

## Connection Info
http://challenge-server:8080

## Hints
(Release after 24 hours if needed)

1. Not everything that looks vulnerable actually is. Sometimes the real vulnerability is where you least expect it.
2. How does the application remember who you are? What information does it display back to you?
3. Template engines can be powerful... and dangerous.

## Author Notes

This challenge tests:
- Ability to identify and ignore red herrings
- Understanding of second-order vulnerabilities
- Knowledge of Server-Side Template Injection (SSTI)
- Python object model and MRO traversal
- Jinja2 template engine exploitation

Expected solve time: 2-4 hours for experienced players

## Flag Format
flag{...}

## Tags
- web
- ssti
- jinja2
- python
- second-order
- template-injection

## Files Provided
None (players must discover everything through reconnaissance)

## Infrastructure Requirements
- 256MB RAM per instance
- 0.5 CPU per instance
- Redis for rate limiting
- No outbound internet access required
