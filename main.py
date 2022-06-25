import epd7in5b

from datetime import datetime
import time

import pytz
import io
import screen

import os, sys
libdir = "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib/"
sys.path.append(libdir)

from waveshare_epd import epd7in5bc

if __name__ == '__main__':
    """
    Draw the current time
    """
    try:
      epd = epd7in5bc.EPD()
      epd.init()
      epd.Clear()
      timestamp = datetime.now(pytz.timezone('Europe/Copenhagen'))


      HBlackimage, HRYimage = screen.get_image()
      buffer_bw = epd.getbuffer(HBlackimage)
      buffer_r = epd.getbuffer(HRYimage)
      epd.display(buffer_bw, buffer_r)
      time.sleep(2)
      
    except Exception as e:
      print("Failed to render", e)
