import serial
import json
import time
from collections import deque

ser = serial.Serial('/dev/tty.usbmodem1411', 19200)
ser.write(b'd')
ser.write(b'd')

data = deque(maxlen=)

z = ser.readline()

#b'{type: current_data, rotation: 0, temperature: 143, light_intensity: 364}\r\n'
x = str(data)
x = x[2:-5]


json_acceptable_string = x.replace("'", "\"")
d = json.loads(json_acceptable_string)

test = ''
counter = 0
import time
while counter != 15:
    global test
    ser.write(b'd')
    test = ser.readline()
    print(test)
    time.sleep(1)
    counter += 1
