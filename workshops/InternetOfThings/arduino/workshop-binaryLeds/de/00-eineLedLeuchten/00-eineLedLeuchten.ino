void setup() {
  // was hier steht, wird genau einmal beim Start ausgeführt.
}

void loop() {
  // das hier passiert immer wieder:
  pinMode(2, OUTPUT);
  pinMode(3, INPUT);
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
}
