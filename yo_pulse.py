# -*- coding: utf-8 -*-
"""
Yo Blinkt friend flash
Yo Docs: http://docs.justyo.co
Yo Keys: http://dev.justyo.co

"""
import sys
import time
import requests
import colorsys
from flask import request, Flask

try:
    import numpy as np
except ImportError:
    exit("This script requires the numpy module\nInstall with: sudo pip install numpy")

from blinkt import set_clear_on_exit, set_pixel, show, set_brightness


# Yo API Token: http://dev.justyo.co (not needed in current release)
YO_API_TOKEN = ''


app = Flask(__name__)


#Yo Callback 
@app.route("/yo")
def yo():

    # extract and parse query parameters
    username = request.args.get('username')

    print username
    if (username):
        print "We got a Yo from " + username
        if (username == "orangeoctopus"):
            blink_blinkt()

    # OK!
    return 'OK'

def reset_lights():
    set_brightness(0)
    show()

def make_gaussian(fwhm):
    x = np.arange(0, 8, 1, float)
    y = x[:, np.newaxis]
    x0, y0 = 3.5, 3.5
    fwhm = fwhm
    gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
    return gauss

def blink_blinkt():
    set_brightness(1)
    for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
        fwhm = 4.0/z
        gauss = make_gaussian(fwhm)
        start = time.time()
        y = 4
        for x in range(8):
            h = 0.5
            s = 1.0
            v = gauss[x, y]
            rgb = colorsys.hsv_to_rgb(h, s, v)
            r, g, b = [int(255.0 * i) for i in rgb]
            set_pixel(x, r, g, b)
        show()
        end = time.time()
        t = end - start
        if t < 0.1:
            time.sleep(0.04 - t)
        print "lighting";
    reset_lights()



if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)