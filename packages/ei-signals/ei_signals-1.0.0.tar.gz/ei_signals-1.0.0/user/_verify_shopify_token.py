import base64
import hashlib
import hmac
import json
import time

def base64url_decode(input):
    # Add necessary padding
    padding = '=' * (4 - len(input) % 4)
    return base64.urlsafe_b64decode(input + padding)

def base64url_encode(input):
    return base64.urlsafe_b64encode(input).rstrip(b'=')

def verify_shopify_jwt(token, secret):
    try:
        # Split the JWT into header, payload, and signature
        header_b64, payload_b64, signature_b64 = token.split('.')

        # Decode the header and payload
        header = json.loads(base64url_decode(header_b64).decode('utf-8'))
        payload = json.loads(base64url_decode(payload_b64).decode('utf-8'))

        if payload['exp'] < time.time():
            return False, "Token expired"
        # Combine header and payload
        unsigned_token = f"{header_b64}.{payload_b64}"

        # Hash the header and payload using SHA-256
        hash = hmac.new(secret.encode('utf-8'), unsigned_token.encode('utf-8'), hashlib.sha256)

        # Sign the hash using the HS256 algorithm
        signature = base64url_encode(hash.digest())

        # Compare the provided signature with the generated one
        if signature.decode('utf-8') == signature_b64:
            return True, payload
        else:
            return False, "Invalid signature"

    except Exception as e:
        return False, str(e)
    
# secret_key = ''
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczpcL1wvdGVzdC1zdG9yZS1lYXN5aW5zaWdodHMubXlzaG9waWZ5LmNvbVwvYWRtaW4iLCJkZXN0IjoiaHR0cHM6XC9cL3Rlc3Qtc3RvcmUtZWFzeWluc2lnaHRzLm15c2hvcGlmeS5jb20iLCJhdWQiOiI3OTM3ZDA2OTMxZThiNGUwNmZhNzI1NGE3ZmE3NmE1MSIsInN1YiI6IjEwNTEzMDU1NzcxNiIsImV4cCI6MTcyMTY0MTEyMCwibmJmIjoxNzIxNjQxMDYwLCJpYXQiOjE3MjE2NDEwNjAsImp0aSI6IjczMWM5OWU5LTYyNjYtNDhlZS05OGQwLWE5NjEyNjU1Zjc1MCIsInNpZCI6ImVmYWYyYThkLTAwYjItNGE2Mi1iMjBhLWI4MDg3NjZjZmRlNCIsInNpZyI6ImNkMmNiYjcxYTcwYzQyZTIwMWMxZmU4ZDJkZDJiNzA1YmUwMmIxNDgwOTI2Mjc5YjAxNzA2NTZjNTM5MDRhOWEifQ.lFepWRzWiTErEv7BbWtmndbPrsNeNYiknhECxa8Tgwg'
# is_valid, result = verify_shopify_jwt(token, secret_key)

# if is_valid:
#     print("Token is valid:", result)
# else:
#     print("Token is invalid:", result)