import json
import urllib3 as urllib

city = "Porto"

http = urllib.PoolManager()

pollution = http.request("Get",f"https://api.openaq.org/v1/latest?city={city}")
pollution = json.loads(pollution.data.decode('utf-8'))

print(json.dumps(pollution,indent=2))
