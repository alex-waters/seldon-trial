import requests

req = requests.post(
    'http://localhost:5001/predict',
    headers={"Content-Type": "application/json"},
    data='''{"data": {"ndarray": ["hi"]}}'''
)

print(req)
resp = req.json()
print(resp)
