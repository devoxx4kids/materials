/*
  Matrix-Laufschrift

  LED-Matrix zeigt ein Bild, das sich von links nach rechts bewegt.
*/

// Pinbelegung für Arduino UNO
int reihenPins[8] = {9, 3, 2, 12, 15, 11, 7, 6};       // Anschlüsse der Reihenpins am Arduino
int spaltenPins[8] = {13, 8, 17, 10, 5, 16, 4, 14};    // Anschlüsse der Spaltenpins am Arduino


// Bild, das auf der Matrix gezeigt wird. 1 = LED an, 0 = LED aus
int bild[8][24] = {                            

  {0, 1, 1, 0, 0, 1, 1, 0,   0, 1, 1, 0, 1, 1, 0, 0,   0, 1, 0, 0, 0, 0, 1, 0},
  {0, 1, 1, 0, 0, 1, 1, 0,   0, 1, 1, 0, 1, 1, 0, 0,   1, 1, 1, 0, 0, 1, 1, 1},
  {0, 1, 1, 0, 0, 1, 1, 0,   0, 1, 1, 0, 1, 1, 0, 0,   0, 1, 0, 0, 0, 0, 1, 0},
  {0, 1, 1, 1, 1, 1, 1, 0,   0, 1, 1, 0, 1, 1, 0, 0,   0, 0, 0, 1, 1, 0, 0, 0},
  {0, 1, 1, 1, 1, 1, 1, 0,   0, 1, 1, 0, 1, 1, 0, 0,   0, 0, 0, 1, 1, 0, 0, 0},
  {0, 1, 1, 0, 0, 1, 1, 0,   0, 1, 1, 0, 0, 0, 0, 0,   1, 1, 0, 0, 0, 0, 1, 1},
  {0, 1, 1, 0, 0, 1, 1, 0,   0, 1, 1, 0, 0, 0, 0, 0,   0, 1, 1, 1, 1, 1, 1, 0},
  {0, 1, 1, 0, 0, 1, 1, 0,   0, 1, 1, 0, 1, 1, 0, 0,   0, 0, 1, 1, 1, 1, 0, 0}

};

void setup() {
  for (int i = 0; i < 8; i++) {                      // Alle Pins werden als OUTPUT declariert
    pinMode(reihenPins[i], OUTPUT);
    pinMode(spaltenPins[i], OUTPUT);
  }
}

void loop() {
  int bildLaenge = sizeof(bild[0])/sizeof(bild[0][0]) - 8;
  
  for (int offset = 0; offset <= bildLaenge; offset++) {
    for (int refresh = 0; refresh < 50; refresh ++) {
      for (int y = 0; y < 8; y++) {                  // zeilenweise werden
        for (int x = 0; x < 8; x++) {                // von links nach rechts alle Einträge des Bild-Arrays geprüft
          if (bild[x][y + offset] == 1) {            // ist der Eintrag = 1
            digitalWrite(spaltenPins[x], HIGH);      // wird der Spaltenpin eingeschalten
          } else {                                   // sonst
            digitalWrite(spaltenPins[x], LOW);       // abgeschalten
          }
        }
        digitalWrite(reihenPins[y], LOW);            // nun wird der Reihenpin auf LOW geschalten (da es die Kathode der LED betrifft bedeutet LOW eingeschalten)
        delayMicroseconds(700);                      // das Programm hält ein paar Mikrosekunden an
        digitalWrite(reihenPins[y], HIGH);           // danach wird der Reihenpin wieder auf HIGH (in diesem Fall also abge-) schaltet
      }
    }
  }
  delay(1000);
  
}
