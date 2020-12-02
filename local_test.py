from seldon_core.seldon_client import SeldonClient

payload_data = {"features": [1]}

endpoint = "0.0.0.0:5000"

sc = SeldonClient(microservice_endpoint=endpoint)
response = sc.microservice(
   json_data=payload_data,
   method="predict"
)

print(response.request)
print(response.success)
