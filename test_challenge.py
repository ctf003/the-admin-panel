#!/usr/bin/env python3
import requests
import hashlib
import time
import sys

BASE_URL = "http://localhost:8080"

def test_main_page():
    print("[*] Testing main page...")
    r = requests.get(BASE_URL)
    assert r.status_code == 200
    assert "Internal Portal" in r.text
    print("[+] Main page OK")

def test_robots_txt():
    print("[*] Testing robots.txt...")
    r = requests.get(f"{BASE_URL}/robots.txt")
    assert r.status_code == 200
    assert "secret-backup.zip" in r.text
    print("[+] robots.txt OK")

def test_backup_zip():
    print("[*] Testing backup.zip...")
    r = requests.get(f"{BASE_URL}/static/secret-backup.zip")
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/zip'
    print("[+] backup.zip OK")

def test_sqli_fake_error():
    print("[*] Testing fake SQLi error...")
    r = requests.post(f"{BASE_URL}/login", data={
        'username': "admin' OR '1'='1",
        'password': "anything"
    })
    assert "OperationalError" in r.text
    print("[+] Fake SQLi error OK")

def test_admin_login():
    print("[*] Testing admin login...")
    r = requests.post(f"{BASE_URL}/login", data={
        'username': 'admin',
        'password': 'p@ssw0rd123'
    })
    assert r.status_code == 200
    data = r.json()
    assert 'token' in data
    token = data['token']
    
    r = requests.get(f"{BASE_URL}/admin", cookies={'token': token})
    assert r.status_code == 200
    assert "flag{not_the_real_one_nice_try}" in r.text
    print("[+] Admin login and canary flag OK")

def solve_pow(challenge):
    nonce = 0
    while True:
        proof = hashlib.sha256((challenge + str(nonce)).encode()).hexdigest()
        if proof.startswith('0000'):
            return str(nonce)
        nonce += 1
        if nonce > 1000000:
            raise Exception("PoW failed")

def test_ssti_basic():
    print("[*] Testing basic SSTI...")
    
    r = requests.get(f"{BASE_URL}/pow-challenge")
    challenge = r.json()['challenge']
    pow_nonce = solve_pow(challenge)
    
    username = f"test_{int(time.time())}"
    r = requests.post(f"{BASE_URL}/register", data={
        'username': username,
        'password': 'password123',
        'display_name': '{{7*7}}',
        'pow_nonce': pow_nonce,
        'challenge': challenge
    })
    assert r.status_code == 200
    
    r = requests.post(f"{BASE_URL}/login", data={
        'username': username,
        'password': 'password123'
    })
    token = r.json()['token']
    
    r = requests.get(f"{BASE_URL}/dashboard", cookies={'token': token})
    assert "49" in r.text
    print("[+] Basic SSTI (7*7=49) OK")

def test_blocked_paths():
    print("[*] Testing blocked paths...")
    paths = ['/.git/config', '/.env', '/app.py', '/__pycache__/']
    for path in paths:
        r = requests.get(f"{BASE_URL}{path}")
        assert r.status_code == 404
    print("[+] Blocked paths OK")

def test_scanner_blocking():
    print("[*] Testing scanner blocking...")
    r = requests.get(BASE_URL, headers={'User-Agent': 'sqlmap/1.0'})
    assert r.status_code == 403
    print("[+] Scanner blocking OK")

if __name__ == '__main__':
    tests = [
        test_main_page,
        test_robots_txt,
        test_backup_zip,
        test_sqli_fake_error,
        test_admin_login,
        test_ssti_basic,
        test_blocked_paths,
        test_scanner_blocking
    ]
    
    print("=" * 60)
    print("Challenge Verification Tests")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"[-] {test.__name__} FAILED: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    sys.exit(0 if failed == 0 else 1)
