/*

 
 Code to do an organ with four hc-sr04 sensors
 each sensor can trigger two notes, depending on the height of the hand in front of it (see MEDIUM and HIGHEST constants).
 
 Based on an example found on the internet, and fading memories of the laser harp/organ of Jean-Michel Jarre 
 
 May 2015,  @wadael
 */


/*************************************************
 * All the notes. Not all are used.
 * but at least, now you have them all
 *************************************************/

#define NOTE_B0  31
#define NOTE_C1  33
#define NOTE_CS1 35
#define NOTE_D1  37
#define NOTE_DS1 39
#define NOTE_E1  41
#define NOTE_F1  44
#define NOTE_FS1 46
#define NOTE_G1  49
#define NOTE_GS1 52
#define NOTE_A1  55
#define NOTE_AS1 58
#define NOTE_B1  62
#define NOTE_C2  65
#define NOTE_CS2 69
#define NOTE_D2  73
#define NOTE_DS2 78
#define NOTE_E2  82
#define NOTE_F2  87
#define NOTE_FS2 93
#define NOTE_G2  98
#define NOTE_GS2 104
#define NOTE_A2  110
#define NOTE_AS2 117
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_CS3 139
#define NOTE_D3  147
#define NOTE_DS3 156
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_FS3 185
#define NOTE_G3  196
#define NOTE_GS3 208
#define NOTE_A3  220
#define NOTE_AS3 233
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988
#define NOTE_C6  1047
#define NOTE_CS6 1109
#define NOTE_D6  1175
#define NOTE_DS6 1245
#define NOTE_E6  1319
#define NOTE_F6  1397
#define NOTE_FS6 1480
#define NOTE_G6  1568
#define NOTE_GS6 1661
#define NOTE_A6  1760
#define NOTE_AS6 1865
#define NOTE_B6  1976
#define NOTE_C7  2093
#define NOTE_CS7 2217
#define NOTE_D7  2349
#define NOTE_DS7 2489
#define NOTE_E7  2637
#define NOTE_F7  2794
#define NOTE_FS7 2960
#define NOTE_G7  3136
#define NOTE_GS7 3322
#define NOTE_A7  3520
#define NOTE_AS7 3729
#define NOTE_B7  3951
#define NOTE_C8  4186
#define NOTE_CS8 4435
#define NOTE_D8  4699
#define NOTE_DS8 4978


/*
* The values for the four TRIG connectors 
*/
#define trigPin1 8
#define trigPin2 9
#define trigPin3 10
#define trigPin4 11

/*
* The values for the four ECHO connectors 
*/
#define echoPin1 4
#define echoPin2 5
#define echoPin3 6
#define echoPin4 7

/*
* BUZZER PIN
*/
#define PIEZO_PIN 12


/* this is values expressed in centimeters (cm) because I love the metric system */
#define MEDIUM 30
#define HIGHEST 60

/*
* All measures under and above will not be treated. 
*/

#define DELAY_TIME 500  // Milliseconds 
#define NOTE_DURATION 2 //  4 = quarter note, 8 = eighth note, etc.:

void setup() {
  Serial.begin (9600); // speed of the communication ; value used in the example

  /* Setting the arduino pins for outpout or input */
  pinMode(trigPin1, OUTPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(trigPin3, OUTPUT);
  pinMode(trigPin4, OUTPUT);

  pinMode(echoPin1, INPUT);
  pinMode(echoPin2, INPUT);
  pinMode(echoPin3, INPUT);
  pinMode(echoPin4, INPUT);

  pinMode(PIEZO_PIN, OUTPUT);
}


void loop() {
  checkSensor(trigPin1, echoPin1,"do", NOTE_C4,"sol",NOTE_G3);
  checkSensor(trigPin2, echoPin2,"re",NOTE_D4,"la", NOTE_A3);
  checkSensor(trigPin3, echoPin3,"mi",NOTE_E4,"si",NOTE_B3);
  checkSensor(trigPin4, echoPin4,"fa",NOTE_F4,"do",NOTE_C3);
}



int checkSensor(int trigPin, int echoPin, char* lowKey, int iLowKey, char* highKey, int iHighKey){
  long duration, distance;
  
  digitalWrite(trigPin, LOW);  // Added this line
  delayMicroseconds(2); // Added this line

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10); // Added this line
  
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;


  if (distance > HIGHEST || distance <= 0){
   /*  
     Serial.print( trigPin );
     Serial.print(":");
     Serial.print("Out of range :");
   */  
  }
  else {
    Serial.print( trigPin );
     Serial.print( ";");
     Serial.print(distance);
     Serial.print(" cm " );
     
     
    if(distance >0 && distance <= MEDIUM){
      Serial.print(  "LOW" );
      Serial.println(  lowKey );
      playNote(iLowKey);
      }
    else{
      if(distance > MEDIUM  && distance <= HIGHEST){
        Serial.print(  "HIGH " );
        Serial.print(  distance );
        Serial.println(  highKey );
        playNote(iHighKey);
      }
    }

    delay(DELAY_TIME);  
    Serial.println(  "*******************************" );
  }
}

/*
* Method for playing a note
*/
void playNote(int note){
  tone(PIEZO_PIN, note,DELAY_TIME);
  
  int pauseBetweenNotes = DELAY_TIME * 1.30;
  
  delay(pauseBetweenNotes);
  
  // stop the tone playing:
  noTone(PIEZO_PIN);
  
  Serial.print(  "jouer ");
  Serial.println( note);
}



