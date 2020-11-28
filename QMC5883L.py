# the following reference codes were used to solve the problem
#https://github.com/robert-hh/QMC5883/blob/master/qmc5883.py
#https://github.com/gvalkov/micropython-esp8266-hmc5883l/blob/master/hmc5883l.py
#https://github.com/Slaveche90/gy271compass

import math, machine, time
from ustruct import pack
from array import array

"""TODO:
 + Temperature accuracy i got in my case was about + 10°C from the real value 
 + Make Module accessible for other register and other magnetic field sensitivity
"""



class QMC5883L():
    def __init__ (self, scl=22, sda=21 ):
        self.i2c =i2c= machine.I2C(scl=machine.Pin(scl), sda=machine.Pin(sda), freq=100000)
        #self.address=const(13)
        # Initialize sensor.
        i2c.start()
        #Write Register 0BH by 0x01 (Define Set/Reset period)
        i2c.writeto_mem(13, 0xB, b'\x01')
        #Write Register 09H by 0x1D 
        # (Define OSR = 512, Full Scale Range = 8 Gauss, ODR = 200Hz, set continuous measurement mode)
        i2c.writeto_mem(13, 0x9, b'\x11101')
        i2c.stop()

        # Reserve some memory for the raw xyz measurements.
        self.data = array('B', [0] * 9)

    def reset(self):
        """performs a reset of the device by writing to the memory address 0xA, the value of b '\ x10000000' """
        #Write Register 0AH by 0x80
        self.i2c.writeto_mem(13, 0xA, b'\x10000000')
        
    def standby (self):
        """device goes into a sleep state by writing to memory address 0x9, b '\ x00' """
        self.i2c.writeto_mem(13, 0x9, b'\x00')
        
    def read_rawData(self):
        """performs a reading of the data in the position of momoria 0x00, by means of a buffer"""
        data = self.data        
        
        self.i2c.readfrom_mem_into(13, 0x00, data)
        time.sleep(0.005)
#        print(data)
        # concatenate high_byte and low_byte into two_byte data
        x_raw = (data[1] << 8) | data[0]
        y_raw = (data[3] << 8) | data[2]
        z_raw = (data[5] << 8) | data[4]
        
        return x_raw, y_raw, z_raw
   
    def read_rawTemperature(self):
        data = self.data
        
        self.i2c.readfrom_mem_into(13, 0x00, data)
        time.sleep(0.005)
        temperature_raw = (data[8] << 8) | data[7]
         # signed int (-32766 : 32767)
        if temperature_raw > 32767:           
            temperature_raw = temperature_raw - 65536
        temperature_raw = temperature_raw & 0x3fff # to get only positive numbers (first bit, sign bit)
        
        return temperature_raw
        
    def read_Temperature(self):
        """ performs a reading of temperature Data and Outputs Temperature in Degree"""
        temp = self.read_rawTemperature()
        #print(temp)
        temperature = temp / 520
        print('Temp. in °C:', temperature)
    
    def heading(self):
        """ returns heading of Sensor in 0-360° """
        print(self.read_rawData())
        x_raw, y_raw, z_raw = self.read_rawData()
        
        
        heading = math.atan2(y_raw, x_raw)
        
        if(heading > 2.0 * math.pi):
            heading = heading - 2.0 * math.pi
        
        # check for sign
        if(heading < 0.0):
            heading = heading + 2.0 * math.pi
        
        # convert into angle
        heading_angle = int(heading * 180.0 / math.pi)
        print('heading_angle', heading_angle)
        
        return heading_angle
        
        
#qmc=QMC5883L()
#qmc.read_Temperature()
#qmc.heading()
        