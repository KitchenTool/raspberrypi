from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

from datetime import datetime
from urllib import request
import json
import random
import pytz
import time

from openweathermap_key import API_KEY

EPD_WIDTH = 640
EPD_HEIGHT = 384

QUOTES = [
    "I don't know\n    - Andreas"
  , "Stupidity is doing the same thing twice,\nand expecting a different result\n    - Kristin"
  , "Oh, so hot\n    - Andreas"
  , "DMI is so pessimistic\n    - Andreas"
  , "I'm SO funny!\n    - Kristin"
  , "I'm tiiiiiirrreeeeeeeed\n    - Kristin"
  , "Skildpadde drikker malk\n    - Kristin"
  , "When you think you lack words\nWhat you really lack is ideas\n- Jens"
  , "BAU CHICKA WA-WAAAAU"
  , "Kristin is the most awesome person!\n- Jens and Andreas"
  ]
  
def get_image():
    # Prepare timestamp weather data
    timestamp = datetime.now(pytz.timezone('Europe/Copenhagen'))
    weather_json = request.urlopen('https://api.openweathermap.org/data/2.5/weather?q=Copenhagen,DK&appid='+API_KEY).read()
    weather = json.loads(weather_json)
    condition = weather['weather'][0]['main'] # Weather condition like 'Rain'
    temperature = weather['main']['temp'] - 273.15 # Temperature converted from fucking Kelvin

    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('L', (EPD_WIDTH, EPD_HEIGHT), 255) # 255: clear the frame
    draw_on_image(timestamp, image)
    return image

def draw_on_image(timestamp, image):
    draw = ImageDraw.Draw(image)
    #draw.rectangle((0, 6, 640, 40), fill = 127)

    # Date
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 30)
    date_text = timestamp.strftime("%A %d/%m/%y")
    draw.text((200, 10), date_text, font = font, fill = 0)

    # Time
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 185)
    time_text = timestamp.strftime("%H:%M")
    time_text = time_text[:-1] + "?"
    draw.text((50, 50), time_text, font = font, fill = 0)

    # Quotes
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 30)
    quote = random.choice(QUOTES)
    w, h = draw.textsize(quote)
    draw.text(((EPD_WIDTH // 2 - w // 2), 250), quote, font = font, fill = 127)

    # Weather
    #weather_image = Image.open().convert('L')
    #inverted_weather = ImageOps.invert(weather_image)
    #image.paste(inverted_weather, (20, 230))

if __name__ == "__main__":
    get_image().show()