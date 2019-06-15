import epd7in5b

from datetime import datetime
import time
import pytz
import io
import screen

if __name__ == '__main__':
    # Loop and redraw every 60 seconds
    while True:
      epd = epd7in5b.EPD()
      epd.init()
      timestamp = datetime.now(pytz.timezone('Europe/Copenhagen'))

      try:
        image = screen.get_image()
        epd.display_frame(epd.get_frame_buffer(image))
      
      except Exception as e:
        print("Failed to render", e)

      # time until next 10 minutes
      time_after = timestamp.minute % 10 * 60 + timestamp.second
      time_until = 600 - time_after - 5 # 7 sec buffer
      time.sleep(time_until)
