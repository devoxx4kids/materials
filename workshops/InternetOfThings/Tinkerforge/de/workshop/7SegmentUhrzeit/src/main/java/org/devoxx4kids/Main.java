package org.javaland4kids;

import com.tinkerforge.BrickletSegmentDisplay4x7;
import com.tinkerforge.IPConnection;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Created by alexanderbischof on 18.09.14.
 */
public class Main {

    private static final String HOST = "localhost";
    private static final int PORT = 4223;

    public static void main(String args[]) throws Exception {

        //Find UID
        BrickletReader brickletReader = new BrickletReader();
        brickletReader.readBricklets(HOST, PORT);
        Bricklet segmentBricklet = brickletReader.getBrickletByDeviceId(BrickletSegmentDisplay4x7.DEVICE_IDENTIFIER);

        IPConnection ipcon = new IPConnection();
        BrickletSegmentDisplay4x7 sd4x7 = new BrickletSegmentDisplay4x7(segmentBricklet.getUid(), ipcon); // Create device object
        ipcon.connect(HOST, PORT);

        //Hilfsklasse für Datumswerte, stellt Uhrzeit 14:30 -> 1430 dar
        SimpleDateFormat dateformatter = new SimpleDateFormat("HHmm");

        try {
            while(true){

                //Hole neu Uhrzeit
                String uhrzeit = dateformatter.format(new Date());

                //Stelle Uhrzeit dar
                short[] segments = {
                        getByteForCharacter(uhrzeit.charAt(0)),
                        getByteForCharacter(uhrzeit.charAt(1)),
                        getByteForCharacter(uhrzeit.charAt(2)),
                        getByteForCharacter(uhrzeit.charAt(3)),
                };
                sd4x7.setSegments(segments, (short) 7, true);

                //warte 1min
                Thread.sleep(60/*Sekunden*/ * 1000l);
            }
        } finally {
            ipcon.disconnect();
        }
    }

    public static byte getByteForCharacter(char c){
        switch (c){
            //Zahlen
            case '0': return 0x3f;
            case '1': return 0x06;
            case '2': return 0x5b;
            case '3': return 0x4f;
            case '4': return 0x66;
            case '5': return 0x6d;
            case '6': return 0x7d;
            case '7': return 0x07;
            case '8': return 0x7f;
            case '9': return 0x6f;

            //Kleinbuchstaben
            case 'a':return 0x5f;
            case 'b':return 0x7c;
            case 'c':return 0x58;
            case 'd':return 0x5e;
            case 'e':return 0x7b;
            case 'f':return 0x71;
            case 'g':return 0x6f;
            case 'h':return 0x74;
            case 'i':return 0x02;
            case 'j':return 0x1e;
            case 'k':return 0x00; //npr
            case 'l':return 0x06;
            case 'm':return 0x00; //npr
            case 'n':return 0x54;
            case 'o':return 0x5c;
            case 'p':return 0x73;
            case 'q':return 0x67;
            case 'r':return 0x50;
            case 's':return 0x6d;
            case 't':return 0x78;
            case 'u':return 0x1c;
            case 'v':return 0x00;//npr
            case 'w':return 0x00;//npr
            case 'x':return 0x00;//npr
            case 'y':return 0x6e;
            case 'z':return 0x00;//npr

            //Großbuchstaben
            case 'A':return 0x77;
            case 'B':return 0x7c;
            case 'C':return 0x39;
            case 'D':return 0x5e;
            case 'E':return 0x79;
            case 'F':return 0x71;
            case 'G':return 0x6f;
            case 'H':return 0x76;
            case 'I':return 0x06;
            case 'J':return 0x1e;
            case 'K':return 0x00; //npr
            case 'L':return 0x38;
            case 'M':return 0x00; //npr
            case 'N':return 0x54;
            case 'O':return 0x3f;
            case 'P':return 0x73;
            case 'Q':return 0x67;
            case 'R':return 0x50;
            case 'S':return 0x6d;
            case 'T':return 0x78;
            case 'U':return 0x3e;
            case 'V':return 0x00;//npr
            case 'W':return 0x00;//npr
            case 'X':return 0x00;//npr
            case 'Y':return 0x6e;
            case 'Z':return 0x00;//npr
        }
        return 0;
    }
}
