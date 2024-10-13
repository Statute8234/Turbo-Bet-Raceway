import requests

model = 'jeep'
api_url = 'https://api.api-ninjas.com/v1/cars?limit=2&model={}'.format(model)
response = requests.get(api_url, headers={'X-Api-Key': 'WA4JaGhb4IwV1SB7HB3WtA==F9pCGDsOMvwjnyyj'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)