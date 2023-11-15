import requests
import base64

# part 1: send a message
url = "https://hash-browns.cs.uwaterloo.ca/api/plain/send"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
data = {
    "api_token": "a695541970563a34db9eb9237667a43317b638cfb67f71d820d12f6ad01542d9",
    "recipient": "Rex",
    "msg": "SGVsbG8sIFdvcmxkIQ==" 
    # note that the string is converted using https://onlinestringtools.com/convert-string-to-base64
    # the content of the message is "Hello, World!"
}

response = requests.post(url, json=data, headers=headers)
# print(response.json())

# part 2: receive a message
url = "https://hash-browns.cs.uwaterloo.ca/api/plain/inbox"
data = {
    "api_token": "a695541970563a34db9eb9237667a43317b638cfb67f71d820d12f6ad01542d9"
}

response = requests.post(url, json=data, headers=headers)
content = response.json()
print(content)
content = content[0]
msg_id = content['msg_id']
sender = content['sender']
msg = content['msg']
decode_msg = base64.b64decode(msg).decode('ascii')
print(decode_msg)