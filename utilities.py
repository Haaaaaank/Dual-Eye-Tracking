"""
    Utilities that get data from eye tracker or display data on screen
"""
"""
    Copyright 2016 Meng Du

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
"""

from ast import literal_eval
import logging

# from pygaze.libscreen import Display, Screen
# from pygaze.eyetracker import EyeTracker

# disp = Display()
# tracker = EyeTracker(disp)
# scr = Screen

logging.basicConfig(filename='dataLog.log', level=logging.DEBUG)


def get_data():
    # data = tracker.sample()
    # TODO
    return 'test'  # str(data)


def display(data):
    # assuming data is a string containing tuple (x, y)
    try:
        pos_tuple = literal_eval(data)
        logging.info(pos_tuple)
    except (ValueError, SyntaxError):
        print data
    # import datetime
    # print datetime.datetime.now(), data
