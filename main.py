# -*- Coding: utf-8 -*-
"""
Main Program of CanSat
Calling each modules and methods from this
"""
import sensers
import steerage
import communication
import control

import os
import csv
import time
import datetime

class CanSat:
    """
    Fundamental Class for CanSat models
    description of member variables
        destination : GPS positon of destionation in format (latitude, longitude) tuple
        location : GPS position of current position in format [latitude, longitude] list
        altitude : altitude of rover
        euler : euler of rover in format [heading, roll, pitch]
        mag : magnetometer of rover [x, y, z]
        gyro : gyroscope [x, y, z]
        accel : accelerometer [x, y, z]
        direction : direction to destionation in format of 360 degrees
        distance : distance to destionation (meters)
        
    """

    def __init__(self):
        """
        constructor of CanSat instance
        """
        #info about position
        self.destination = self.define_destination()
        
        self.location = list()#initialize 
        
        #info about the rover
        self.altitude = 0.00
        self.euler = list() #format [heading, roll, pitch]
        #self.axis = [0.0, 0.0, 0.0, 0.0]#format [sys, gyro, accel, mag]
        self.mag = list()
        self.gyro = list()
        self.accel = list()

        self.direction = 0.00
        self.distance = 0.00

        self.helm = None

        #read the file number
        try:
            with open('file_number.txt', 'r') as f:
                self.file_number = int(f.read())
                #print(type(self.file_number))
                #print(self.file_number)

        except:
            print("fail to read file_number.txt!")
        
        #generate file name
        self.data_log_file_name = "/home/pi/Desktop/CanSat-Alpha-Software/datalog/data_log_" + str(self.file_number) + ".csv"

        #write the new file number
        try:
            with open('file_number.txt', 'w') as f:
                buf = str(self.file_number + 1)
                f.write(buf)

        except:
            print("fail to write file_number.txt!")     

        #make the data log file
        try:
            with open(self.data_log_file_name, "w", encoding = "utf-8", newline = '') as f:
                w = csv.writer(f, delimiter = ",")
                #sum up all lists and write
                buf = ['timestamp','latitude','longitude','pressure[hPa]','temperature[degC]','humidity[percent]', 'altitude', 'heading', 'roll', 'pitch', 'mag_x', 'mag_y', 'mag_z', 'gyro_x', 'gyro_y', 'gyro_z', 'accel_x', 'accel_y', 'accel_z', 'distance', 'direction']
                print(buf)
                w.writerow(buf)

        except:
            print("fail to save the flight data!")
            
        return   
    
    def motor_test(self):
        communication.im920_send('initiating motor test now')
        communication.lighting(0b11100111)
        control.straight(100)
        time.sleep(5)
        communication.lighting(0b00100111)
        control.turnR(100)
        time.sleep(5)
        communication.lighting(0b11100100)
        control.turnL(100)
        time.sleep(5)
        communication.lighting(0b10100101)
        control.rover_brake()
        time.sleep(1)
        communication.lighting(0b01100110)
        control.rover_stop()
        time.sleep(1)

        communication.lighting(0b00000000)

    def define_destination(self):
        """
        Defines GPS Position of destionation from file
        Returns tuple of GPS position in format (latitude, longitude)
        """
        with open("destination.txt", "r") as f:
            buf = f.read()
            #print(buf)
            buf = buf.split()
            #print(buf)
            #change the type of each elements
            buf = [float(s) for s in buf]
        
        return tuple(buf)#split and make it tuple
    
    def update_atitude(self):
        """
        update atitude variables by reading sensors
        """
        self.nowtime = datetime.now().strftime('%Y%m%d %H%M%S')
        
        self.location = sensers.getGPS_position()
        #print(type(self.location))

        self.environment = sensers.read_env_data()
        
        #self.altitude = 
        self.euler = sensers.read_imu_euler()
        #print(type(self.euler))

        self.mag = sensers.read_imu_mag()
        #print(type(self.mag))
        self.gyro = sensers.read_imu_gyro()
        #print(type(self.gyro))
        self.accel = sensers.read_imu_accel()
        #print(type(self.accel))

        self.distance, self.direction = steerage.get_distance_rad(self.location, self.destination)
        #print(type(self.distance))
        #print(type(self.direction))

        self.print_status()
        self.data_log()
    
    def print_status(self):
        print('timestamp : {}' .nowtime)
        print('location : {}'.format(self.location))
        print('pressure : {}  temperature : {}  humidity : {}'.format(self.environment[0], self.environment[1], self.environment[2]))
        print('heading : {}  roll : {} pitch : {}'.format(self.euler[0],self.euler[1],self.euler[2]))
        print('mag   {}'.format(self.mag))
        print('gyro  {}'.format(self.gyro))
        print('accel {}'.format(self.accel))
        print('distance : {}  direction : {}'.format(self.distance, self.direction))

    def data_log(self):
        """
        save the sensor value as CSV file
        this is for flight analyis
        """
        try:
            with open(self.data_log_file_name, "a") as f:
                w = csv.writer(f, delimiter = ",")
                #sum up all tuples and write
                buf = list(self.location) + list(self.environment)
                buf.append(self.altitude)
                buf = buf + nowtime + list(self.euler) + list(self.mag) + list(self.gyro) + list(self.accel)
                buf.append(self.distance)
                buf.append(self.direction)
                buf = [str(s) for s in buf]
                #print(buf)
                w.writerow(buf)

        except:
            print("fail to save the flight data!")
            
        return

    def rover_derivation(self):
        """
        ローバーを目的地に導く自動操縦の関数だよ！
        """
        self.helm = steerage.decideHelm(self.direction, self.euler[0])
        
        if self.helm == 0:
            communication.lighting(0b11000011)
            communication.im920_send('Go straight!')
            control.straight(50)
            time.sleep(3)

        elif self.helm == 1:
            communication.lighting(0b00000011)
            communication.im920_send('Turn Right!')
            control.turnR(50)
            time.sleep(3)

        elif self.helm == 2:
            communication.lighting(0b00000011)
            communication.im920_send('Turn Right more!')
            control.turnR(70)
            time.sleep(3)
        
        elif self.helm == -1:
            communication.lighting(0b11000000)
            communication.im920_send('Turn Left!')
            control.turnL(50)
            time.sleep(3)

        elif self.helm == -2:
            communication.lighting(0b11000000)
            communication.im920_send('Turn Left more!')
            control.turnL(70)
            time.sleep(3)

        communication.lighting(0b00000000)
        control.rover_stop()


    def control_log(self):
        """
        save the control data as CSV file
        this is for control analysis
        """
        try:
            with open(self.control_log_file_name, "w", encoding = "utf-8", newline = '') as f:
                w = csv.writer(f, delimiter = ",")
                #sum up all lists and write
                w.writerow(self.location + self.distance + self.direction)

        except:
            print("fail to save the control log")
            
        return    

    def imu_calibration(self):
        """
        キャリブレーションを行う関数
        すべてキャリブレーションするまで，俺らの夏は終わらないぜ！
        """
        while True:
            imu_status = sensers.read_imu_calibration_status()
            print('imu_status = {}'.format(imu_status))
            if imu_status == (3,3,3,3):
                """
                返り値は(sys_status, gyro_status, accel_status, mag_status)
                0=uncalibrated and 3=fully calibrated
                """
                return
            else:
                print('imu is not fully calibrated!\n')

communication.im920_send('CanSat PRECURSOR Activation!')
cansat = CanSat()

cansat.motor_test()

cansat.imu_calibration()

while True:
    cansat.update_atitude()
    cansat.rover_derivation()