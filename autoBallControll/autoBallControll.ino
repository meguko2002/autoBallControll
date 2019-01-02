/*******************************
  autoBallControll !!
 ******************************/
#include <Servo.h>
#define SERVO_L 5
#define SERVO_R 6
const float Ak = -0.05;
const float Bk = -0.1;
const float Ck = -0.1;
const float RATETHA = 0.1; // =5mm/15deg/200mm*180deg/pi()
const float CNV = 1;  //[mm/pixel]

//***servo motor parameter***//
const int CTR = 90;      //center angle
const int MAX = 140;     //斜めの上限角度
const int MIN = 40;      //斜めの下限角度
const int adj_l = 2, adj_r = -12;    //モータ角度微調整
const int DELAY = 5;   // DELAY > MotorSpeed (=2.67msec/deg)
//**************************//

Servo servo_l;
Servo servo_r;

void setup() {
  servo_l.attach(SERVO_L);
  servo_r.attach(SERVO_R);
  Serial.begin(9600);
}

void loop() {
  int pos_r = CTR;
  int x = 0, pre_x = 0;
  float v, pre_v = 0, a, F_r=0;
//  static unsigned long deltat = 0, nowtime = 0, pretime = 0;
  bool isValid = false;

  servo_r.write(pos_r + adj_r);
  delay(2000);

  while (1) {
    if (Serial.available() >= 3) {
      int head = Serial.read();
      if (head == 128) {
        int high = Serial.read();
        int low  = Serial.read();
        x = (high << 7) + low;
//        nowtime = millis();
//        deltat = nowtime - pretime;
//        Serial.print(x, DEC);
//        Serial.print(",");
//        Serial.println(deltat);
//        pretime = nowtime;
        if (0 <= x <= 1023) {
          isValid = true;
        }
        x = x*CNV; //pixelをmmに変換
      }
    }
    
    v = (x - pre_x)/DELAY;
    a = (v - pre_v)/DELAY;
    F_r = Ak * a + Bk * v + Ck * x;
    if(F_r>RATETHA)pos_r++;
    else if(F_r< -RATETHA)pos_r--;
    servo_r.write(pos_r + adj_r);
    Serial.println(pos_r);
    if(isValid){
      Serial.println("x range over!!");
      break;
    }
    pre_x = x;
    pre_v = v;
    delay(DELAY);
  }
}
