import serial
def main():
    ser = serial.Serial("COM15",9600,timeout=None)  # COMポート(Arduino接続)
    while True:
      flag = input('>>')
      ser.write(flag.encode('utf-8'))
      if flag == 'a':
        break
    ser.close()

if __name__ == '__main__':
   main()