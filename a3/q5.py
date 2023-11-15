import requests
import base64
import binascii
import nacl.utils
import nacl.secret
import nacl.encoding
from nacl.hash import blake2b
import nacl.bindings
import nacl.public

# part 1: Verify a public key
url = "https://hash-browns.cs.uwaterloo.ca/api/pke/get-key"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
data = {
    "api_token": "a695541970563a34db9eb9237667a43317b638cfb67f71d820d12f6ad01542d9",
    "user": "Rex"
}
response = requests.post(url, json=data, headers=headers)
content = response.json()
print(content)
pubkey = content['pubkey']
pubkey = base64.b64decode(pubkey)
print(pubkey)
hashed_pubkey = blake2b(pubkey)
print(hashed_pubkey)

# part 2: Send a message
Rex_pubkey = pubkey
public_key, secret_key = nacl.bindings.crypto_kx_keypair()

url = "https://hash-browns.cs.uwaterloo.ca/api/pke/set-key"
data = {
    "api_token": "a695541970563a34db9eb9237667a43317b638cfb67f71d820d12f6ad01542d9",
    "pubkey": base64.b64encode(public_key).decode()
}

response = requests.post(url, json=data, headers=headers)

message = b"Hello, World!"

# generate nonce
nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
encrypted = nacl.bindings.crypto_box(message, nonce, Rex_pubkey, secret_key)
final_msg = base64.b64encode(nonce + encrypted).decode()
url = "https://hash-browns.cs.uwaterloo.ca/api/pke/send"
data = {
    "api_token": "a695541970563a34db9eb9237667a43317b638cfb67f71d820d12f6ad01542d9",
    "recipient": "Rex",
    "msg": final_msg
}
response = requests.post(url, json=data, headers=headers)

# part 3: Receive a message
url = "https://hash-browns.cs.uwaterloo.ca/api/pke/inbox"
data = {
    "api_token": "a695541970563a34db9eb9237667a43317b638cfb67f71d820d12f6ad01542d9"
}
response = requests.post(url, json=data, headers=headers)
content = response.json()
print("received")
print(content)
content = content[0]
msg = base64.b64decode(content['msg'])

# create the box
box = nacl.public.Box(nacl.public.PrivateKey(secret_key), nacl.public.PublicKey(Rex_pubkey))
# decode the message
decode_msg = box.decrypt(msg)
print(decode_msg)