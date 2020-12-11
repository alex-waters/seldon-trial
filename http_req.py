import requests

req = requests.post(
    'http://localhost:5001/predict',
    headers={"Content-Type": "application/json"},
    data='''{"data": {"ndarray": ["1", "2", "3"]}}'''
)

print(req)
resp = req.json()
print(resp)
