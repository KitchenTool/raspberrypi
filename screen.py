from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

from datetime import datetime
from urllib import request
import requests
from pathlib import Path
import json
import textwrap
import pytz

from openweathermap_key import API_KEY
import wikipedia

EPD_WIDTH = 640
EPD_HEIGHT = 384

  
def get_image():
    # Prepare timestamp weather data
    timestamp = datetime.now(pytz.timezone('Europe/Copenhagen'))
    weather_json = request.urlopen('https://api.openweathermap.org/data/2.5/weather?q=Copenhagen,DK&appid='+API_KEY).read().decode()
    weather = json.loads(weather_json)

    # For simplicity, the arguments are explicit numerical coordinates
    HBlackimage = Image.new('L', (EPD_WIDTH, EPD_HEIGHT), 255)  # 298*126
    HRYimage = Image.new('L', (EPD_WIDTH, EPD_HEIGHT), 255)  # 298*126  ryimage: red or yellow image  
    draw_on_image(timestamp, weather, HBlackimage, HRYimage)
    return HBlackimage, HRYimage

def get_font(fontname, size):
    path = Path(__file__).absolute().parent / fontname
    return ImageFont.truetype(str(path), size)

def draw_on_image(timestamp, weather, bw, r):
    drawb = ImageDraw.Draw(bw)
    drawr = ImageDraw.Draw(r)
    #draw.rectangle((0, 6, 640, 40), fill = 127)

    # Date and weather
    font = get_font('NotoSans-Bold.ttf', 25)
    date_text = timestamp.strftime("%A %d/%m/%y")
    condition = weather['weather'][0]['main'] # Weather condition like 'Rain'
    temperature = round(weather['main']['temp'] - 273.15, 1) # Temperature converted from fucking Kelvin
    text = '{} - {}°C {}'.format(date_text, temperature, condition)
    w, h = drawb.textsize(text, font)
    drawb.text(((EPD_WIDTH // 2 - w // 2), 10), text, font = font, fill = 0)

    # Time
    font = get_font('NotoSans-Bold.ttf', 185)
    time_text = timestamp.strftime("%H:%M")
    time_text = time_text[:-1] + "0"
    w, h = drawb.textsize(time_text, font)
    drawb.text((EPD_WIDTH // 2 - w // 2, 0), time_text, font = font, fill = 0)

    # Location
    font = get_font('NotoSans-Regular.ttf', 40)
    drawr.text((0, 210), "Welcome to Copenhagen!", font=font, fill=0, align="left")

    # Quotes
    font = get_font('NotoSerif-Regular.ttf', 24)
    quote = wikipedia.random_event()
    lines = textwrap.wrap(quote, width=50)
    MAX_LENGTH = 4
    if len(lines) > MAX_LENGTH:
        lines[MAX_LENGTH - 1] = lines[MAX_LENGTH - 1] + "..."
    for i, line in enumerate(lines[:MAX_LENGTH]):
        w, h = drawr.textsize(line, font)
        drawr.text(((EPD_WIDTH // 2 - w // 2), 270 + (i * 24)), line, font = font, fill = 127)

if __name__ == "__main__":
    get_image().show()
