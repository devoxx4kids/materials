package org.javaland4kids;

import com.tinkerforge.BrickletPiezoSpeaker;
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
        Bricklet bricklet = brickletReader.getBrickletByDeviceId(BrickletPiezoSpeaker.DEVICE_IDENTIFIER);

        IPConnection ipcon = new IPConnection();
        BrickletPiezoSpeaker ps = new BrickletPiezoSpeaker(bricklet.getUid(),
                ipcon);
        ipcon.connect(HOST, PORT);
        ps.calibrate();

        ps.beep(2000, 2000);
        ipcon.disconnect();
    }
}
