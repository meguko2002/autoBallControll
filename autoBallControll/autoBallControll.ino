/*******************************
  autoBallControll !!
 ******************************/
#include <Servo.h>           //Servo motor
#define SERVO_L 5
#define SERVO_R 6
const float Ak = -0.05;
const float Bk = 0;
const float Ck = 0.6;
const float obj_x = 100;

const int CTR = 90;      //center angle
const int MAX = 140;     //斜めの上限角度
const int MIN = 40;      //斜めの下限角度
const int adj_l = 2, adj_r = -12;    //モータ角度微調整
const int DELAY = 5;   // DELAY > MotorSpeed (=2.67msec/deg)
const int OFFSET = 10; //deg
Servo servo_l;
Servo servo_r;

void setup() {
  servo_l.attach(SERVO_L);
  servo_r.attach(SERVO_R);
  Serial.begin(115200);
}

int gopos(int pos, int obj) {
  if (pos - obj > 0) pos--;
  else if (pos - obj < 0) pos++;
  return pos;
}

void loop() {
  int pos_r = CTR + OFFSET, pos_l = CTR - OFFSET;
  float x = 0, pre_x = 0;
  float v, pre_v = 0, a, obj_r, obj_l;
  servo_r.write(pos_r + adj_r);
  servo_l.write(180 - (pos_l + adj_l));
  delay(2000);

  while (1) {
    //    x = Serial.read();
    v = x - pre_x;
    a = v - pre_v;
    obj_r = Ak * a + Bk * v + Ck * (x - obj_x) + CTR;
    obj_l = 180 - obj_r;
    pos_r = gopos(pos_r, int(obj_r));
    pos_l = gopos(pos_l, int(obj_l));
    servo_r.write(pos_r + adj_r);
    servo_l.write(180 - (pos_l + adj_l));
    Serial.print("obj_r=");
    Serial.print(obj_r);
    Serial.print(",");
    Serial.print(pos_r);
    Serial.print(",");
    Serial.println(pos_l);
    pre_x = x;
    pre_v = v;
    delay(DELAY);
  }
}
