/*
  Matrix-Delphin

  LED-Matrix zeigt eine Delphin-Animation.
*/

// Pinbelegung für Arduino UNO
int reihenPins[8] = {9, 3, 2, 12, 15, 11, 7, 6};       // Anschlüsse der Reihenpins am Arduino
int spaltenPins[8] = {13, 8, 17, 10, 5, 16, 4, 14};    // Anschlüsse der Spaltenpins am Arduino


// Bilder, die auf der Matrix gezeigt werden. 1 = LED an, 0 = LED aus
int bilder[][8][8] =
{
  { // Bild 1
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 1, 0, 0, 0},
    {0, 0, 1, 1, 1, 1, 0, 0},
    {0, 1, 1, 1, 1, 1, 1, 0},
    {0, 0, 0, 1, 0, 0, 0, 1},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
  },
  { // Bild 2
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 1, 0, 0, 1},
    {0, 0, 1, 1, 1, 1, 1, 0},
    {0, 1, 1, 1, 1, 1, 0, 0},
    {0, 0, 0, 1, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
  },
  { // Bild 3
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 1, 0, 0, 0},
    {0, 0, 1, 1, 1, 1, 0, 1},
    {0, 1, 1, 1, 1, 1, 1, 0},
    {0, 0, 0, 1, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
  },
  { // Bild 1
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 1, 0, 0, 0},
    {0, 0, 1, 1, 1, 1, 0, 0},
    {0, 1, 1, 1, 1, 1, 1, 0},
    {0, 0, 0, 1, 0, 0, 0, 1},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
  },
  { // Bild 2
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 1, 0, 0, 1},
    {0, 0, 1, 1, 1, 1, 1, 0},
    {0, 1, 1, 1, 1, 1, 0, 0},
    {0, 0, 0, 1, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
  },
  { // Bild 3
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 1, 0, 0, 0},
    {0, 0, 1, 1, 1, 1, 0, 1},
    {0, 1, 1, 1, 1, 1, 1, 0},
    {0, 0, 0, 1, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
  },
  { // Bild 4
    {0, 0, 0, 0, 1, 0, 0, 0},
    {0, 0, 1, 1, 1, 1, 0, 0},
    {0, 1, 1, 1, 1, 1, 1, 0},
    {0, 0, 0, 1, 0, 0, 0, 1},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
  },
  { // Bild 4
    {0, 0, 0, 0, 1, 0, 0, 0},
    {0, 0, 1, 1, 1, 1, 0, 0},
    {0, 1, 1, 1, 1, 1, 1, 0},
    {0, 0, 0, 1, 0, 0, 0, 1},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
  }
};


void setup() {
  for (int i = 0; i < 8; i++) {                      // Alle Pins werden als OUTPUT declariert
    pinMode(reihenPins[i], OUTPUT);
    pinMode(spaltenPins[i], OUTPUT);
  }
}

void loop() {
  int anzahlBilder = sizeof(bilder) / sizeof(bilder[0]);

  // für jedes Bild-Array
  for (int bildNummer = 0; bildNummer < anzahlBilder; bildNummer++) {

    for (int refresh = 0; refresh < 50; refresh ++) {

      for (int y = 0; y < 8; y++) {                     // zeilenweise werden (pro Bild)
        for (int x = 0; x < 8; x++) {                   // von links nach rechts alle Einträge des Arrays geprüft
          if (bilder[bildNummer][x][y] == 1) {          // ist der Eintrag = 1
            digitalWrite(spaltenPins[x], HIGH);         // wird der Spaltenpin eingeschalten
          } else {                                      // sonst
            digitalWrite(spaltenPins[x], LOW);          // abgeschalten
          }
        }
        digitalWrite(reihenPins[y], LOW);              // nun wird der Reihenpin auf LOW geschalten (da es die Kathode der LED betrifft bedeutet LOW eingeschaltet)
        delayMicroseconds(500);                        // das Programm hält ein paar Mikrosekunden an
        digitalWrite(reihenPins[y], HIGH);             // danach wird der Reihenpin wieder auf HIGH (in diesem Fall also abge-) schaltet
      }
    }
  }
}
