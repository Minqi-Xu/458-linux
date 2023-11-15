import requests
import base64
import binascii
import nacl.utils
import nacl.secret
import nacl.encoding
from nacl.hash import blake2b
import nacl.bindings

# generate key pair
verification_key, signature_key = nacl.bindings.crypto_sign_keypair()

# part 1: upload a public verification key
url = "https://hash-browns.cs.uwaterloo.ca/api/signed/set-key"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

data = {
    "api_token": "a695541970563a34db9eb9237667a43317b638cfb67f71d820d12f6ad01542d9",
    "pubkey": base64.b64encode(verification_key).decode()
}

response = requests.post(url, json=data, headers=headers)
# print(response.json())


# part 2: send a message
# print(signature_key)
msg = b'Hello, World!'
msg = nacl.bindings.crypto_sign(msg, signature_key)
url = "https://hash-browns.cs.uwaterloo.ca/api/signed/send"
data = {
    "api_token": "a695541970563a34db9eb9237667a43317b638cfb67f71d820d12f6ad01542d9",
    "recipient": "Rex",
    "msg": base64.b64encode(msg).decode()
}
response = requests.post(url, json=data, headers=headers)