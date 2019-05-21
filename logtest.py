from datetime import datetime

def updata(self):
    self.nowtime = datetime.now().strftime('%Y%m%d %H%M%S')

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



while(Tlue):
    updata()
    

print (datetime.now().strftime('%Y/%m/%d %H:%M:%S'))