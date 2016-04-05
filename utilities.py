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
from pygaze.libscreen import Display
from pygaze.eyetracker import EyeTracker

disp = Display()
tracker = EyeTracker(disp)


def get_data():
    data = tracker.sample()
    return str(data)


def display(data):
    # assume data is a string containing tuple (x, y)
    tuple = literal_eval(data)
    # import datetime
    # print datetime.datetime.now(), data
