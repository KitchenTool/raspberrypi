import epd7in5b
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

import random
import time
from datetime import datetime
import pytz
import os
import io

EPD_WIDTH = 640
EPD_HEIGHT = 384
WEATHER_IMAGE = "/tmp/weather.png"

QUOTES = [
    "I don't know\n    - Andreas"
  , "Stupidity is doing the same thing twice,\nand expecting a different result\n    - Kristin"
  , "Oh, so hot\n    - Andreas"
  , "DMI is so pessimistic\n    - Andreas"
  , "I'm SO funny!\n    - Kristin"
  , "I'm tiiiiiirrreeeeeeeed\n    - Kristin"
  , "Skildpadde drikker mælk\n    - Kristin"
  , "When you think you lack words\nWhat you really lack is ideas\n- Jens"
  , "BAU CHICKA WA-WAAAAU"
  , "Jens is the most awesome person!\n- Kristin and Andreas"
  , "Jens never has to clean. Ever!\n- Kristin and Andreas"
  ]

def main():
    # Loop and redraw every 60 seconds
    while True:
      epd = epd7in5b.EPD()
      epd.init()

      # Prepare timestamp and weather data
      os.system("curl https://wttr.in/Copenhagen_tqp0.png 2>/dev/null > " + WEATHER_IMAGE)
      timestamp = datetime.now(pytz.timezone('Europe/Copenhagen'))
      time.sleep(5)

      # For simplicity, the arguments are explicit numerical coordinates
      image = Image.new('L', (EPD_WIDTH, EPD_HEIGHT), 255) # 255: clear the frame
      draw_on_image(timestamp, image)
      epd.display_frame(epd.get_frame_buffer(image))

      # time until next 10 minutes
      time_after = timestamp.minute % 10 * 60 + timestamp.second
      time_until = 600 - time_after - 5 # 7 sec buffer
      time.sleep(time_until)

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
    weather_image = Image.open(WEATHER_IMAGE).convert('L')
    inverted_weather = ImageOps.invert(weather_image)
    image.paste(inverted_weather, (20, 230))

if __name__ == '__main__':
    main()
