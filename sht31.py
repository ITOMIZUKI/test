import time
import smbus

def tempChanger(msb, lsb):
    mlsb = ((msb << 8) | lsb)                                             # P1
    return (-45 + 175 * int(str(mlsb), 10) / (pow(2, 16) - 1))            # P2

def humidChanger(msb, lsb):
    mlsb = ((msb << 8) | lsb)
    return (100 * int(str(mlsb), 10) / (pow(2, 16) - 1))

i2c = smbus.SMBus(1)
i2c_addr = 0x45                                                           # P3

i2c.write_byte_data(i2c_addr, 0x21, 0x30)                                 # P4
time.sleep(0.5)

while 1:
    i2c.write_byte_data(i2c_addr, 0xE0, 0x00)                             # P5
    data = i2c.read_i2c_block_data(i2c_addr, 0x00, 6)                     # P6
    print( str('{:.4g}'.format(tempChanger(data[0], data[1]))) + "C" )
    print( str('{:.4g}'.format(humidChanger(data[3], data[4]))) + "%" )
    print("------")
    time.sleep(1)




