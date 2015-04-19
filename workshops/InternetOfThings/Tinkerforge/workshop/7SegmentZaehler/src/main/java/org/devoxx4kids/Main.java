package org.javaland4kids;

import com.tinkerforge.BrickletSegmentDisplay4x7;
import com.tinkerforge.IPConnection;

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

        try {
            System.out.print("Bis wohin soll gezählt werden: ");
            String counter_end = System.console().readLine();

            //Zählt von 0 bis counter durch erhöhen von 1 und 1 Sekunde pause
            sd4x7.startCounter((short) 0, Short.valueOf(counter_end), (short) 1, 1000l);

            sd4x7.addCounterFinishedListener(new BrickletSegmentDisplay4x7.CounterFinishedListener() {
                @Override
                public void counterFinished() {
                    System.out.println("Fertig gezählt");
                }
            });

            System.out.println("Press key to exit");
            System.in.read();
        } finally {
            ipcon.disconnect();
        }
    }
}
