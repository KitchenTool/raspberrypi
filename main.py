import epd7in5b

from datetime import datetime
import time
import pytz
import io
import screen

if __name__ == '__main__':
    """
    Draw the current time
    """
    try:
      epd = epd7in5b.EPD()
      epd.init()
      timestamp = datetime.now(pytz.timezone('Europe/Copenhagen'))

      image = screen.get_image()
      epd.display_frame(epd.get_frame_buffer(image))
      
    except Exception as e:
      print("Failed to render", e)
