import serial
import json
from time import sleep

class Arduino():

    def __init__(self, com, baud_rate):
        self.com = com
        self.baud_rate = baud_rate
        self.connected = False
        self.data = self.json_convert('{"type": "current_data", "rotation": 0, "temperature": 164, "light_intensity": 46}')
        self.settings = self.json_convert('{"type": "settings", "manual": 1, "debug": 1, "rotation": 0, "temperature":{"max": 50, "min": 0}, "light":{"max": 50, "min": 0}, "extension":{"max": 50, "min": 0}}')
        self.manual = False
        

        #Make connection
        try:
            self.ser = serial.Serial(com, baud_rate)
        except serial.serialutil.SerialException:
            com = Arduino.reset_com()
            self.ser = serial.Serial(com, baud_rate)

        self.ser.timeout = True
        self.ser.write_timeout = 100

    '''
    First connection may take a while to work.
    Use this function when testing the connection.
    '''
    def connect(self):
        self.write("d")
        while(self.ser.in_waiting == 0):
            self.write('d')
            sleep(.5)
        self.connected = True
        self.ser.flushInput()
        self.ser.flushOutput()

    '''
    Wait for the input to be received.
    If this waiting took too long, it returns False
    '''
    def wait_for_buffer(self):
        for i in range(0,20):
            if self.ser.in_waiting>0:
                return True
            sleep(.1)
        return False

    '''
    Clean the output by removing the \r\n parts of the output
    '''
    def clean_output(self, s):
        s = s.replace("\\r","")
        s = s.replace("\\n","")
        return s[2:-1]

    def json_convert(self, s):
        s = s.replace("'","\"")
        try:
            rs = json.loads(s)
        except json.decoder.JSONDecodeError:
            f = open("arduino_error.log","w")
            f.write("JSONDecodeError: "+s)
            f.close()
            rs = json.loads(s)

        return rs

    '''
    Write to the Arduino.
    No need to add the EOL markers, the program does it for you
    '''
    def write(self, s):
        s+="$"
        self.ser.write(bytearray(s, "UTF-8"))

    '''
    Read the output from the Arduino.
    It sometimes may take a while for it to load, so the buffer is included
    '''
    def readline(self):
        if self.wait_for_buffer():
            return self.clean_output(str(self.ser.readline()))
        return False

    '''
    Get the data from the Arduino
    '''
    def get_data(self):
        self.write("d")
        output = self.readline()
        output = self.json_convert(output)
        self.data = output
        return output

    def get_settings(self):
        self.write("s")
        output = self.readline()
        output = self.json_convert(output)
        self.settings = output
        return output

    '''
    Get temperature
    '''
    def get_temperature(self):
        return self.data['temperature']

    '''
    Get light intensity
    '''
    def get_light(self):
        return self.data['light_intensity']

    def get_state(self):
        return self.manual

    def set_state(self, bool):
        self.manual = bool


    '''
    This function handles the com ports, so you dont have to rewrite it all the time
    '''
    @staticmethod
    def get_com():
        try:
            f = open("serial.conf", "r")
            com = f.read()
            f.close()
        except FileNotFoundError:
            com = Arduino.reset_com()
        return com

    @staticmethod
    def reset_com():
        f = open("serial.conf", "w")
        com = input("Enter com port (default: '/dev/tty.usbmodem1411'): ")
        if len(com)==0:
            com = '/dev/tty.usbmodem1411'
        f.write(com)
        f.close()
        return com
