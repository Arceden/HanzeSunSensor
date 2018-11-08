'''
Gebruik dit python script om alle Arduino functies te testen vanuit Python
'''

import serial
from time import sleep

try:
    ser = serial.Serial('/dev/tty.usbmodem1411', 19200)
except serial.serialutil.SerialException:
    com = input("Enter com port (example: COM4): ")
    ser = serial.Serial(com, 19200)

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

    def post_temph(self):
        self.ser.write(b'tmpl 12344')
        self.wait_for_buffer()
        return self.ser.readline()


ar = Arduino(ser)
print("Connecting..")
ar.connect()
print("Connected!")
print("GET | DATA     | ", ar.get_data() )
print("GET | SETTINGS | ", ar.get_settings() )
print("POST| DEBUGGER | ", ar.toggle_debugger() )
print("GET | SETTINGS | ", ar.get_settings() )
print("POST| TEMP_H   | ", ar.post_temph() )
