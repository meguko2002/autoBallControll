void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(115200);
}

void loop() {

  int inputchar;
  // シリアルポートより1文字読み込む
  inputchar = Serial.read();

  if (inputchar != -1 ) {
    Serial.println(inputchar);
    switch (inputchar) {
      case 0:
        // 読み込みデータが　s の場合
        while(1){
        digitalWrite(13, HIGH);
        delay(100);
         digitalWrite(13, LOW);
        delay(100);  
        }     
        break;
      case 1:
        // 読み込みデータが　q の場合
        digitalWrite(13, LOW);
        break;
    }
  }
}
