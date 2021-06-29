import json
import urllib3 as urllib

city = "Braga"
country="pt"
API_KEY = "9895877bceb93ae7cec3933caebf6914"


http = urllib.PoolManager()
weather = http.request("Get",f"api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric")
weather = json.loads(weather.data.decode('utf-8'))

print(json.dumps(weather,indent=2))
