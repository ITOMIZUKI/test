# -*- Coding: utf-8 -*-
import os
import time
import csv
import time
import datetime

class CanSat:
    def __init__(self):
        self.data_log_file_name = "C:\Python\datatest1.csv"

        with open(self.data_log_file_name, "w", encoding = "utf-8", newline = '') as f:
            w = csv.writer(f, delimiter = ",")
            #sum up all lists and write
            buf = ['timestamp']
            print(buf)
            w.writerow(buf)

    def update_atitude(self):
        self.nowtime = datetime.datetime.now().strftime("%H%M%S")
        #= sensers.gps.timestamp[1] + sensers.gps.timestamp[2]
        self.print_status()
        self.data_log()
        #print (self.nowtime)

    def print_status(self):
        print('timestamp :{}'.format(self.nowtime))

    def data_log(self):
        with open(self.data_log_file_name, "a") as f:
            w = csv.writer(f, delimiter = ",")
            #sum up all tuples and write
            buf = list(int(self.nowtime))
            buf = [str(s) for s in buf]
            w.writerow(buf)

cansat = CanSat()

while True:
    cansat.update_atitude()
    time.sleep(1)
    