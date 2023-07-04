
from flask import Flask, request, render_template
import requests
import json
import feedparser

app = Flask(__name__)
#parse a text file to retrieve the API key
api_key = open('api\keyfile.txt', 'r')
def get_weather():
    # Get weather data from OpenWeatherMap
    # Make sure to replace 'your_api_key' with your actual OpenWeatherMap API Key
    # And replace 'your_city' and 'your_country' with your actual city and country
    weather_response = requests.get('http://api.weatherapi.com/v1/current.json?key='+ api_key +'=St. Thomas, Ontario')
    weather_data = weather_response.json()
    location = weather_data['location']['name']
    condition = weather_data['current']['condition']['text']
    temperature = weather_data['current']['temp_c']
    return location, condition, temperature

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


@app.route('/tempdata', methods=['POST'])
def tempdata():
    temp = request.form['pool_temperature']
    print("Received temperature data: " + temp)
    if(temp == ''):
        print("No temperature data received")
        temp = "No temperature data, check connection"
    else:
        return 'OK', 200

@app.route('/')
def home():
    location, condition, temperature = get_weather()
    news_title, news_link, news_image = get_news()
    return render_template('index.html', location=location, condition=condition, temperature=temperature, news_title=news_title, news_link=news_link, news_image=news_image)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
