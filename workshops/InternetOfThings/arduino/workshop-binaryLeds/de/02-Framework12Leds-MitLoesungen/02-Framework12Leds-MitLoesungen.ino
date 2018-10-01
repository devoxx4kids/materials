// wie viele LEDs haben wir? Wenn ihr weniger LEDs braucht, einfach die Zahl ändern (mehr als 12 geht nicht!)
#define LED_ANZAHL 12

// die Hälfte davon rechnen wir automatisch aus
#define LED_ANZAHL_HALB LED_ANZAHL / 2

void schalteAn(int led) {
  int pinHigh, pinLow;
  if (led >= LED_ANZAHL_HALB) {
    pinLow = (led - LED_ANZAHL_HALB + 1) * 2;
    pinHigh = pinLow + 1;
  }
  else {
    pinHigh = (led + 1) * 2;
    pinLow = pinHigh + 1;
  }

  digitalWrite( pinHigh, LOW);
  digitalWrite( pinLow, LOW);
  
  digitalWrite( pinHigh, LOW);
  digitalWrite( pinLow, HIGH);
}

void setup() {
  Serial.begin(9600);
  Serial.println("Start");
  
  for (int i=0; i < 12; i++) {
    pinMode( i+2, OUTPUT);
  }
}

bool ledAn[LED_ANZAHL];

void schalteLeds() {
  // alle LEDs ausschalten
  for(int x=0; x < LED_ANZAHL; x++) {
    digitalWrite(x+2, LOW);
  }
  
  // alle ungeraden LEDs anschalten, die an sein sollen
  for( int x = 0; x < LED_ANZAHL + 2; x+= 2) {
    if (ledAn[x])
      schalteAn(x);
  }
  
  // alle geraden LEDs anschalten, die an sein sollen
  for( int x = 1; x < LED_ANZAHL + 2; x+= 2) {
    if (ledAn[x])
      schalteAn(x);
  }
}

// wie lange soll eine Runde dauern?
// AUFGABE: spielt mit dieser Zahl und guckt mal, was passiert (dafür muss ein Lichtmuster im loop() aktiv sein!
int rundenDauer = 1000;

int countDown = rundenDauer;

// Die Funktion loop() wird immer wieder ausgeführt, so schnell es geht.
// Deshalb könnt ihr hier sagen, was sich verändern soll.
// damit es übersichtlich bleibt, rufen wir stattdessen einfach eine andere Funktion auf,
// die entscheidet, welche LEDs als nächstes an sein sollen.
// einfach die // am Anfang der Zeile rausnehmen. Es darf aber immer nur eine Funktion gleichzeitig ausgeführt werden.
void loop() {
  //AlleAn();
  //AlleAbwechselnd();
  //Zaehlen();
  //Uhr();
  //NightRider();

  schalteLeds();
}

int zaehler = 1;
void AlleAbwechselnd() {
  ledAn[zaehler] = true;

  // muss beim nächsten mal was anderes berechnet werden?
  countDown--;
  if (countDown == 0) {
    // die Lampe, die bis jetzt an war, machen wir aus:
    ledAn[zaehler] = false;
    
    // zaehler + 1 wäre die nächste Lampe - aber wenn die Zahl zu groß wird, leuchtet nichts mehr
    // % ist wie Teilen mit Rest - genau der Rest. Wenn also LED_ANZAHL 10 ist und zaehler + 1 ist 11, 
    // dann ist der Rest 1, also leuchtet die zweite Lampe.
    zaehler = (zaehler + 1) % LED_ANZAHL;

    // den CountDown müssen wir zurücksetzen, damit nicht sofort was anderes gemacht wird
    countDown = rundenDauer;
  }
}

// hier schalten wir einfach alle LEDs an.
void AlleAn() {
  // wir starten mit 0 (und nennen die Zahl i), und machen das, was zwischen den {} steht
  // dann wird i eins größer
  // nun wird geprüft, ob die Zahl, die wir i genannt haben, kleiner ist als unsere LED_ANZAHL. (i<LED_ANZAHL).
  // wenn ja, dann wiederholen wir das, was zwischen den {} steht, und so weiter.
  for(int i=0; i<LED_ANZAHL; i = i + 1) {
    ledAn[i] = true;
  }
}

void Uhr() {
  // berechne LED-Status:
  int minuten = zaehler / 60;
  for (int i=0; i<6; i++) {
    ledAn[i] = (minuten % 2 == 1);
    minuten = minuten / 2;
  }

  int sekunden = zaehler % 60;
  for (int i=6; i<=13; i++) {
    ledAn[i] = (sekunden % 2 == 1);
    sekunden = sekunden / 2;
  }

  // muss beim nächsten mal was anderes berechnet werden? - das funktioniert so wie bei AlleAbwechselnd()
  countDown--;
  if (countDown == 0) {
    zaehler++;
    countDown = rundenDauer;
  }
}

// AUFGABE: schafft ihr es, rückwärts zu zählen?
void Zaehlen() {
  // muss beim nächsten mal was anderes berechnet werden?  
  countDown--;
  if (countDown <= 0) {
    // mache den Zaehler eins größer
    // AUFGABE: was passiert, wenn ihr hier statt "+ 1" zum Beispiel "* 2" benutzt?
    zaehler = zaehler + 1;
    
    countDown = rundenDauer;

    // berechne LED-Status:
    int rest = zaehler;
    for (int i=0; i<LED_ANZAHL; i++) {
      ledAn[i] = (rest % 2 == 1);
      rest = rest / 2;
    }
  }
}





// wir brauchen die LEDS 1, 2, 3 und 7, 8, 9 - das ist genau 455
int night = 455; 
int runde = 0;
void NightRider() {
  countDown--;
  if (countDown <= 0) {
    runde = (runde % 6) +1;

    // berechne LED-Status:
    int rest = night;
    for (int i=0; i<LED_ANZAHL; i++) {
      ledAn[i] = (rest % 2 == 1);
      rest = rest / 2;
    }

    countDown = rundenDauer;

    if (runde < 4 ) {
      night = night * 2;
    }
    else {
      night = night / 2;
    }
  }
}
