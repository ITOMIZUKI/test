# -*- Coding: utf-8 -*-
import os
import time
import csv
import datetime



while True:
    nowtime = datetime.datetime.now().strftime("%H%M%S")
    print(nowtime)
    #print(nowtime.time())
    time.sleep(1)