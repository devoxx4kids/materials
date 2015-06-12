package org.javaland4kids;

import com.tinkerforge.BrickletSegmentDisplay4x7;
import com.tinkerforge.IPConnection;

import java.util.Random;

/**
 * Created by alexanderbischof on 18.09.14.
 */
public class Main {

    private static final String HOST = "localhost";
    private static final int PORT = 4223;

    private static final byte[] ZAHLEN = {0x3f, 0x06, 0x5b, 0x4f,
            0x66, 0x6d, 0x7d, 0x07,
            0x7f, 0x6f}; // 0~9,

    public static void main(String args[]) throws Exception {

        //Find UID
        BrickletReader brickletReader = new BrickletReader();
        brickletReader.readBricklets(HOST, PORT);
        Bricklet segmentBricklet = brickletReader.getBrickletByDeviceId(BrickletSegmentDisplay4x7.DEVICE_IDENTIFIER);

        IPConnection ipcon = new IPConnection();
        BrickletSegmentDisplay4x7 sd4x7 = new BrickletSegmentDisplay4x7(segmentBricklet.getUid(), ipcon); // Create device object
        ipcon.connect(HOST, PORT);

        Random r = new Random();

        while (true) {

            //Erzeuge neue Zufallszahl
            int zufallszahl = Math.abs(r.nextInt()) % 10000;

            int ersteZahlIndex = (zufallszahl / 1000);
            int zweiteZahlIndex = (zufallszahl / 100 % 10);
            int dritteZahlIndex = (zufallszahl / 10 % 10);
            int vierteZahlIndex = (zufallszahl % 10);

            System.out.println(ersteZahlIndex+", " + zweiteZahlIndex+", " +dritteZahlIndex+", " +vierteZahlIndex);

            //Schicke Zahl an Display
            short[] segments = {ZAHLEN[ersteZahlIndex], ZAHLEN[zweiteZahlIndex],
                    ZAHLEN[dritteZahlIndex], ZAHLEN[vierteZahlIndex]};
            sd4x7.setSegments(segments, (short) 7, false);

            //Warte 2s
            Thread.sleep(2000l);
        }
    }
}
