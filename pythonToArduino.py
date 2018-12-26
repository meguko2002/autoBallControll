# import serial
# def main():
#     ser = serial.Serial("/dev/cu.usbmodem1421",115200,timeout=None)  # COMポート(Arduino接続)
#     while True:
#       flag = input('>>')
#       ser.write(flag.encode('utf-8'))
#
# if __name__ == '__main__':
#    main()


import time
import serial
ser = serial.Serial('/dev/cu.usbmodem1421', 115200, timeout=0.1)
while True:
    # val = int(input('>>'))
    for val in range(1000):
        head = 128
        high = (val >> 7) & 127
        low  = val & 127
        headByte = head.to_bytes(1, 'big')
        highByte = high.to_bytes(1, 'big')
        lowByte = low.to_bytes(1, 'big')
        ser.write(headByte)
        ser.write(highByte)
        ser.write(lowByte)
        time.sleep(0.005)