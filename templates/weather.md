Weather in {{ weather.name }} ({{ weather.sys.country }}):
Description: {{ weather.weather.0.description }}
Temperature: {{ weather.main.temp }} °C
Wind: {{ weather.wind.speed }} m/s
Pressure: {{ weather.main.pressure }} hpa
Humidity: {{ weather.main.humidity }} %
