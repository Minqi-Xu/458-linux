import requests
import base64
import binascii
import nacl.utils
import nacl.secret

# part 1: send a message
url = "https://hash-browns.cs.uwaterloo.ca/api/psk/send"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# secret_key stores the secret key of binary form
secret_key = binascii.unhexlify("d728843bfc371662e478571365c05e851842d823bacdaa8cb5a55f056f57f5c0")

# generate nonce
nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

# create the secret box
secret_box = nacl.secret.SecretBox(secret_key)

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
url = "https://hash-browns.cs.uwaterloo.ca/api/psk/inbox"
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
decode_msg = secret_box.decrypt(msg)
print(decode_msg.decode('utf-8'))