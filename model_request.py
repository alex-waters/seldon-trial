import requests

resp = requests.post(
    'http://localhost:5000/api/v1.0/predictions',
    headers={
        'Content-Type': 'application/json'
    },
    data=''
)

print(resp.json())
