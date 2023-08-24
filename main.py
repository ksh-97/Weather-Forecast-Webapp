import requests
from ssl import SSLContext
from flask import Flask, render_template, request
import time
import os
import csv

ssl_context = SSLContext()
ssl_context.load_cert_chain('cert.pem', 'key.pem')

app = Flask(__name__)

def kelvin_to_celsius(temp_k):
    return temp_k - 273.15

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
	lat = request.json['lat']
	lon = request.json['lon']

	# Get weather information for clicked location
	weather_url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=5471b45ad1c4e2545c84beb542fcb88c'
	weather_response = requests.get(weather_url)
	weather_data = weather_response.json()

	avg_temp = [0.0] * 7
	avg_rainfall = [0.0] * 7

	for i in range(0, 5):
		for j in range(0, 8):
			avg_temp[i] += kelvin_to_celsius(weather_data['list'][i * 8 + j]['main']['temp'])
			avg_rainfall[i] += weather_data['list'][i * 8 + j]['main']['humidity']
		avg_temp[i] /= 8
		avg_rainfall[i] /= 8		

	avg_temp[5] = avg_temp[2]
	avg_rainfall[5] = avg_rainfall[2]
	avg_temp[6] = avg_temp[4]
	avg_rainfall[6] = avg_temp[4]

	transaction = [
		int(time.time()),
		float(lat),
		float(lon),
		str(avg_temp[0]) + "°C",
		str(avg_temp[1]) + "°C",
		str(avg_temp[2]) + "°C",
		str(avg_temp[3]) + "°C",
		str(avg_temp[4]) + "°C",
		str(avg_temp[5]) + "°C",
		str(avg_temp[6]) + "°C",
		str(avg_rainfall[0]) + "%",
		str(avg_rainfall[1]) + "%",
		str(avg_rainfall[2]) + "%",
		str(avg_rainfall[3]) + "%",
		str(avg_rainfall[4]) + "%",
		str(avg_rainfall[5]) + "%",
		str(avg_rainfall[6]) + "%",
	]

	transaction_file = os.environ.get('TRANSACTION_FILE', 'transactions.csv')
	with open(transaction_file, 'a', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(transaction)

	return weather_data

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=ssl_context)