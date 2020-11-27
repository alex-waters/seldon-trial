from seldon_core.seldon_client import SeldonClient

notes = ['damage', 'fire']

endpoint = "0.0.0.0:5001"

sc = SeldonClient(microservice_endpoint=endpoint)
response = sc.microservice(
 json_data=notes,
 method="predict")

print(response.success)
