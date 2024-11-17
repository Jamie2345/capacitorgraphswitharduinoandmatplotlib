#define capPin A0
#define digitalOut 5
int loop_count = 0;

bool charge = true;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  digitalWrite(digitalOut, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(10);
  int analogVoltage = analogRead(capPin);
  float voltage = ((analogVoltage / 1024.0) * 5.0);
  //Serial.println(analogVoltage);
  loop_count = loop_count + 1;
  if (loop_count > 20) {
    charge = !charge;
    loop_count = 0;
  }
  if (charge) {
    digitalWrite(digitalOut, HIGH);
  }
  else {
    digitalWrite(digitalOut, LOW);
  }
  Serial.println(voltage);
}
