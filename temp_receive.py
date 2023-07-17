#!/usr/bin/python3
from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import json
import feedparser
from datetime import datetime
from datetime import datetime, timedelta
from pytz import timezone

app = Flask(__name__)
last_successful_receive_time = None

def get_weather():
    # Get weather data from OpenWeatherMap
    # Make sure to replace 'your_api_key' with your actual OpenWeatherMap API Key
    # And replace 'your_city' and 'your_country' with your actual city and country
    weather_response = requests.get('http://api.weatherapi.com/v1/current.json?key=30c20373dd8346feadf160425230407&q=St. Thomas, Ontario')
    weather_data = weather_response.json()
    location = weather_data['location']['name']
    condition = weather_data['current']['condition']['text']
    temperature = weather_data['current']['temp_c']
    return location, condition, temperature

CORS(app)

def get_news():
    # Parse the RSS feed
    feed = feedparser.parse('https://www.cbc.ca/cmlink/rss-world')

    # Get the first news item
    first_item = feed.entries[0]

    # Get the title and link from the first news item
    title = first_item.title
    link = first_item.link
    
    # Get the image URL for the channel
    image_url = feed.feed.image['href']

    return title, link, image_url

def process_pool_temperature(pool_temperature):
    global last_successful_receive_time
    print("Received temperature data:", pool_temperature)

    # Get the current time in Eastern Standard Time (EST)
    est_timezone = timezone('US/Eastern')
    est_time = datetime.now(est_timezone)

    # Update the last successful receive time in EST format
    last_successful_receive_time = est_time.strftime("%H:%M:%S")

    # Convert the temperature from Celsius to Fahrenheit
    temp_fahrenheit = (float(pool_temperature) * 9/5) + 32

    # Render the temperature in the 'pool_temperature' element of 'index.html'
    return render_template('index.html', pool_temperature=temp_fahrenheit, last_successful_receive_time=last_successful_receive_time)


p_temp = None  # Global variable to store the pool temperature

@app.route('/temperature', methods=['GET', 'POST', 'PUT'])
def receive_temperature():
    global p_temp

    if request.method == 'POST' or request.method == 'PUT':
        p_temp = request.args.get('value')
        print(f"Received temperature: {p_temp}°C")
        return process_pool_temperature(p_temp)

    if request.method == 'GET':
        return p_temp

@app.route('/', methods=['GET'])
def home():
    location, condition, temperature = get_weather()
    news_title, news_link, news_image = get_news()
    return render_template('index.html', location=location, condition=condition, temperature=temperature, news_title=news_title, news_link=news_link, news_image=news_image, pool_temperature=p_temp, last_successful_receive_time=last_successful_receive_time)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
