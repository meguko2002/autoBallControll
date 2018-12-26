int value = 0;
bool isValid = false;

void setup() {
  Serial.begin(9600);
}

void loop() {
  static unsigned long deltat=0,nowtime=0,pretime=0;
  isValid = false;
  if (Serial.available() >= 3) {
    int head = Serial.read();
    if (head == 128) {
      int high = Serial.read();
      int low  = Serial.read();
      value = (high << 7) + low;
      nowtime = millis();
      deltat = nowtime - pretime;
      Serial.print(value, DEC);
      Serial.print(",");
      Serial.println(deltat);
      pretime = nowtime;
      if (0 <= value <= 1023) {
        isValid = true;
      }
    }
  }
}
