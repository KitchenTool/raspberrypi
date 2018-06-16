import epd7in5b
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import random
import time
from datetime import datetime
import pytz


EPD_WIDTH = 640
EPD_HEIGHT = 384

QUOTES = [
    "I don't know\n    - Andreas"
  , "Stupidity is doing the same thing twice,\nand expecting a different result\n    - Kristin"
  , "Oh, so hot\n    - Andreas"
  , "DMI is so pessimistic\n    - Andreas"
  , "I'm SO funny!\n    - Kristin"
  , "I'm tiiiiiirrreeeeeeeed\n    - Kristin"
  , "Skildpadde drikker mælk\n    - Kristin"
  ]

def main():
    # Loop and redraw every 60 seconds
    while True:
      epd = epd7in5b.EPD()
      epd.init()

      timestamp = datetime.now(pytz.timezone('Europe/Copenhagen'))

      # For simplicity, the arguments are explicit numerical coordinates
      image = Image.new('L', (EPD_WIDTH, EPD_HEIGHT), 255) # 255: clear the frame
      draw_on_image(timestamp, image)
      epd.display_frame(epd.get_frame_buffer(image))  
  
      # time until next 10 minutes
      time_after = timestamp.minute % 10 * 60 + timestamp.second
      time_until = 600 - time_after - 5 # 5 sec buffer
      time.sleep(time_until)

def draw_on_image(timestamp, image):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 185)
    #draw.rectangle((0, 6, 640, 40), fill = 127)

    # Clock
    time_text = time_to_text(timestamp)
    draw.text((50, 50), time_text, font = font, fill = 0)
  
    # Quotes
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 30)
    quote = random.choice(QUOTES)
    w, h = draw.textsize(quote)
    draw.text(((EPD_WIDTH // 2 - w // 2), 250), quote, font = font, fill = 127)

def time_to_text(timestamp):
   return timestamp.strftime('%H:%M')

if __name__ == '__main__':
    main()
