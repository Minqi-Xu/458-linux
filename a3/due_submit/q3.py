import requests
import base64
import binascii
import nacl.utils
import nacl.secret
import nacl.encoding
from nacl.hash import blake2b

# dervie two subkeys
master_key = "ec3e4f2f813152f023e36c5b18ff657c3a4ecab5203e5d2d94fd905811f5c5d7"
master_key = binascii.unhexlify(master_key)
id1 = 1
id2 = 2
derivation_salt_1 = id1.to_bytes(1, 'big')
derivation_salt_2 = id2.to_bytes(1, 'big')

personalization_1 = b'purple_l'
personalization_2 = b'practica'

derived_1 = blake2b(b'', key=master_key, salt=derivation_salt_1, person=personalization_1, encoder=nacl.encoding.RawEncoder)
derived_2 = blake2b(b'', key=master_key, salt=derivation_salt_2, person=personalization_2, encoder=nacl.encoding.RawEncoder)

# part 1: send a message
url = "https://hash-browns.cs.uwaterloo.ca/api/kd/send"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# generate nonce
nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

# create the secret box
secret_box = nacl.secret.SecretBox(derived_1)

# generate encrypt message
message = b"Hello, World!"
encrypted = secret_box.encrypt(message, nonce)

#combined_data = nonce + encrypted
combined_data = encrypted
final_msg = base64.b64encode(combined_data).decode()

data = {
    "api_token": "a695541970563a34db9eb9237667a43317b638cfb67f71d820d12f6ad01542d9",
    "recipient": "Rex",
    "msg": final_msg
}

response = requests.post(url, json=data, headers=headers)
# print(response.json())


# part 2: receive a message
url = "https://hash-browns.cs.uwaterloo.ca/api/kd/inbox"
data = {
    "api_token": "a695541970563a34db9eb9237667a43317b638cfb67f71d820d12f6ad01542d9"
}

response = requests.post(url, json=data, headers=headers)
content = response.json()
print(content)

content = content[0]
msg_id = content['msg_id']
sender = content['sender']
msg = base64.b64decode(content['msg'])
#received_nonce = msg[:nacl.secret.SecretBox.NONCE_SIZE]
#received_msg = msg[nacl.secret.SecretBox.NONCE_SIZE:]
#decode_msg = secret_box.decrypt(received_msg)
secret_box = nacl.secret.SecretBox(derived_2)
decode_msg = secret_box.decrypt(msg)
print(decode_msg.decode('utf-8'))