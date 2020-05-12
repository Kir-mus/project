from requests import get, delete

print(get('http://localhost:7000/api/v2/stories/4/secret_token0000').json())
print(get('http://localhost:7000/api/v2/all_stories/secret_token0000').json())
print(delete('http://localhost:7000/api/v2/stories/4/secret_token0000').json())
print(get('http://localhost:7000/api/v2/stories/4/secret_token0000').json())
print(get('http://localhost:7000/api/v2/trainer/1').json())
print(get('http://localhost:7000/api/v2/catalog/2').json())
print(get('http://localhost:7000/api/v2/catalog').json())
print(get('http://localhost:7000/api/v2/user/secret_token0000').json())
print(get('http://localhost:7000/api/v2/user/1/secret_token0000').json())
print(get('http://localhost:7000/api/v2/trainers').json())
print(get('http://localhost:7000/api/v2/trainer/1').json())
