import urllib.request
import urllib.error
import json
import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

base_url = "http://127.0.0.1:8000/api/auth/register/"
username = f"user_{get_random_string(8)}"
email = f"{username}@test.com"
password = "password123"

data = {
    "username": username,
    "email": email,
    "password": password,
    "user_type": "client"
}
json_data = json.dumps(data).encode('utf-8')

def register(expect_fail=False):
    req = urllib.request.Request(base_url, data=json_data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Status: {response.status}")
            print(response.read().decode('utf-8'))
            return response.status
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code}")
        print(e.read().decode('utf-8'))
        return e.code
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")
        return None

print(f"--- Attempt 1: Register {username} (Expect 201) ---")
status1 = register()

if status1 == 201:
    print(f"\n--- Attempt 2: Register {username} AGAIN (Expect 400) ---")
    status2 = register(expect_fail=True)
    
    if status2 == 400:
        print("\nSUCCESS: Got 400 Bad Request as expected for duplicate user.")
    elif status2 == 500:
        print("\nFAILURE: Got 500 Internal Server Error. Fix not working.")
    else:
        print(f"\nUNEXPECTED: Got status {status2}")

else:
    print("\nInitial registration failed. Is the server running?")
