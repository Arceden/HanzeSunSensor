'''
Gebruik dit python script om alle Arduino functies te testen vanuit Python
'''

import serial
from time import sleep

com = '/dev/tty.usbmodem1411'
baud_rate = 19200

#Get com port from the configuration file
try:
    f = open("serial.conf", "r")
    com = f.read()
except FileNotFoundError:
    f = open("serial.conf", "w")

try:
    ser = serial.Serial(com, baud_rate)
except serial.serialutil.SerialException:
    com = input("Enter com port (example: COM4): ")
    ser = serial.Serial(com, baud_rate)
    f.write(com)
    f.close()

ser.flushInput()
ser.flushOutput()
ser.timeout = True
ser.write_timeout = 100

class Arduino():
    def __init__(self, ser):
        self.ser = ser
        self.connected = False

    def connected(self):
        return self.connected

    def connect(self):
        self.ser.write(b'd\\')
        self.wait_for_buffer()
        connected = True
        ser.flushInput()
        ser.flushOutput()
        return self.ser.in_waiting

    def wait_for_buffer(self):
        for i in range(0,20):
            sleep(.1)
            if self.ser.in_waiting>0:
                return True
        return False

    def get_data(self):
        self.ser.write(b'd$')
        self.wait_for_buffer()
        return self.ser.readline()

    def get_settings(self):
        self.ser.write(b's$')
        self.wait_for_buffer()
        return self.ser.readline()

    def toggle_debugger(self):
        self.ser.write(b'debg$')
        self.wait_for_buffer()
        return self.ser.readline()

    def post_message(self, string):
        string += "$"
        self.ser.write(bytearray(string, "UTF-8"))
        self.wait_for_buffer()
        return self.ser.readline()


ar = Arduino(ser)
print("Connecting..")
ar.connect()
print("Connected!")
print("GET | DATA     | ", ar.get_data() )
print("GET | SETTINGS | ", ar.get_settings() )
print("POST| DEBUGGER | ", ar.toggle_debugger() )
print("POST| TEMP_H   | ", ar.post_message("tmph 120") )
print("POST| TEMP_L   | ", ar.post_message("tmpl 110") )
print("POST| EXT_H    | ", ar.post_message("exth 90") )
print("POST| EXT_L    | ", ar.post_message("extl 12") )
print("POST| LUX_H    | ", ar.post_message("luxh 69") )
print("POST| LUX_L    | ", ar.post_message("luxl 420") )
print("POST| MANU     | ", ar.post_message("manu") )
print("GET | SETTINGS | ", ar.get_settings() )
