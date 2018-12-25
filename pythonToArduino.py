import serial
def main():
    ser = serial.Serial("/dev/cu.usbmodem1421",115200,timeout=None)  # COMポート(Arduino接続)
    while True:
      flag = input('>>')
      ser.write(flag.encode('utf-8'))
      if flag == 'a':
        break
    ser.close()

if __name__ == '__main__':
   main()