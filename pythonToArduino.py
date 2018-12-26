import time
import serial

ser = serial.Serial('/dev/cu.usbmodem1421', 9600, timeout=0.1)

def sendtoArd(val):
    head = 128
    high = (val >> 7) & 127
    low = val & 127
    headByte = head.to_bytes(1, 'big')
    highByte = high.to_bytes(1, 'big')
    lowByte = low.to_bytes(1, 'big')
    ser.write(headByte)
    ser.write(highByte)
    ser.write(lowByte)

def main():
    while True:
        for i in range(1000):
            sendtoArd(i)
            time.sleep(0.005)


if __name__ == '__main__':
   main()