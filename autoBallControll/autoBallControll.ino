/*******************************
  autoBallControll !!
 ******************************/
#include <Servo.h>           //Servo motor
#include <SNESpaduino.h>     //Super Famicon controller

#define SERVO_L 5
#define SERVO_R 6
#define LATCH 7     //orange line 
#define DAT 8       //red line 
#define CLOCK 9     //yellow line 
const int CTR = 90;      //center angle
const int MAX = 140;     //斜めの上限角度
const int MIN = 40;      //斜めの下限角度
const int SQMAX = CTR + 0.7 * (MAX - CTR); //上下左右の振れ角度は斜め振れの0.7倍
const int SQMIN = CTR - 0.7 * (CTR - MIN);
const int adj_l = 2, adj_r = -12;    //モータ角度微調整
const int MOTOR_DELAY = 5;   // MOTOR_DELAY > MotorSpeed (=2.67msec/deg)

Servo servo_l;
Servo servo_r;
SNESpaduino pad(LATCH, CLOCK, DAT);

void setup(){
  servo_l.attach(SERVO_L);
  servo_r.attach(SERVO_R);
  Serial.begin(9600);
}

int gopos(int pos, int obj) {
  if (pos - obj > 0) pos--;
  else if (pos - obj < 0) pos++;
  return pos;
}

void loop() {
  static int pos_l = CTR, pos_r = CTR;

  int btns = pad.getButtons(false);  //コントローラの入力を読み取る

  if (!(btns & BTN_UP)) {
    if (!(btns & (BTN_UP | BTN_LEFT))) {
      pos_l = gopos(pos_l, MIN);
      pos_r = gopos(pos_r, CTR);
      Serial.println(pos_l);
    }
    else if (!(btns & (BTN_UP | BTN_RIGHT))) {
      pos_l = gopos(pos_l, CTR);
      pos_r = gopos(pos_r, MIN);
    }
    else {
      pos_l = gopos(pos_l, SQMIN);
      pos_r = gopos(pos_r, SQMIN);
      Serial.println(pos_l);
    }
  }
  else if (!(btns & BTN_DOWN)) {
    if (!(btns & (BTN_LEFT | BTN_DOWN))) {
      pos_l = gopos(pos_l, CTR);
      pos_r = gopos(pos_r, MAX);
    }
    else if (!(btns & (BTN_DOWN | BTN_RIGHT))) {
      pos_l = gopos(pos_l, MAX);
      pos_r = gopos(pos_r, CTR);
    }
    else {
      pos_l = gopos(pos_l, SQMAX);
      pos_r = gopos(pos_r, SQMAX);
    }
  }
  else if (!(btns & BTN_LEFT)) {
    pos_l = gopos(pos_l, SQMIN);
    pos_r = gopos(pos_r, SQMAX);
  }
  else if (!(btns & BTN_RIGHT)) {
    pos_l = gopos(pos_l, SQMAX);
    pos_r = gopos(pos_r, SQMIN);
  }

  else if (!(btns & BTN_SELECT)) {
    pos_l = CTR;
    pos_r = CTR;
  }

//  servo_l.write(pos_l+adj_l);         //move motors
//  servo_r.write(180 - (pos_r+adj_r)); //サーボは左右で取り付けが逆なので180に対する補数を入力
  servo_l.write(180-(pos_l+adj_l));         //move motors
  servo_r.write(pos_r+adj_r); //サーボは左右で取り付けが逆なので180に対する補数を入力
 Serial.print(pos_l);
  Serial.print(" , ");
 Serial.println(pos_r);

  delay(MOTOR_DELAY);
}

