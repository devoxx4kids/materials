package org.javaland4kids;

import com.tinkerforge.BrickletDistanceIR;
import com.tinkerforge.BrickletPiezoSpeaker;
import com.tinkerforge.IPConnection;

public class Main {

    private static final String HOST = "localhost";
    private static final int PORT = 4223;
    private static final String UID_Distance = "nTP";
    private static final String UID_Speaker = "mtA";

    public static void main(String args[]) throws Exception {
        BrickletReader brickletReader = new BrickletReader();
        brickletReader.readBricklets(HOST, PORT);
        Bricklet distanceBricklet = brickletReader.getBrickletByDeviceId(BrickletDistanceIR.DEVICE_IDENTIFIER);
        Bricklet piezoBricklet = brickletReader.getBrickletByDeviceId(BrickletPiezoSpeaker.DEVICE_IDENTIFIER);

        IPConnection ipcon = new IPConnection();
        BrickletDistanceIR dir = new BrickletDistanceIR(distanceBricklet.getUid(), ipcon);
        BrickletPiezoSpeaker ps = new BrickletPiezoSpeaker(piezoBricklet.getUid(),
                ipcon);
        ipcon.connect(HOST, PORT);

        // Einstellen einer unteren Grenze, wenn ich näher als 20cm bin, soll er
        // trotzdem immer 20cm ausgeben
        dir.setDistanceCallbackThreshold('<', (short) 200, (short) 200);
        ps.calibrate();

        System.out.println("Hörbare Distanz gestartet. Verändere den Abstand am Distanzsensor.");

        //Jetzt soll meine Orgel unendlich lange spielen
        while (true) {
            //Es soll immer ein Ton herauskommen, wenn ich näher als 80cm bin
            if (dir.getDistance() < 800) {
                //Hier piepe ich eine zehntel Sekunde und berechne die Tonhöhe
                ps.beep(100, dir.getDistance() / 100 * 585);
            }
        }
    }
}
