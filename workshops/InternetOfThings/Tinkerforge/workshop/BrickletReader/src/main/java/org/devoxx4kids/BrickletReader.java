package org.javaland4kids;

import com.tinkerforge.BrickletPiezoSpeaker;
import com.tinkerforge.BrickletRotaryPoti;
import com.tinkerforge.BrickletSegmentDisplay4x7;
import com.tinkerforge.IPConnection;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by alexanderbischof on 23.09.14.
 */
public class BrickletReader {

    //Mapping von DeviceIdentifier auf Strings
    public final static Map<Integer, String> uidDeviceMap = new HashMap<>();

    static {
        uidDeviceMap.put(com.tinkerforge.BrickMaster.DEVICE_IDENTIFIER, "Masterbrick");
        uidDeviceMap.put(com.tinkerforge.BrickletDistanceIR.DEVICE_IDENTIFIER, "IR-Distanz-Bricklet");
        uidDeviceMap.put(BrickletPiezoSpeaker.DEVICE_IDENTIFIER, "PiezoSpeaker-Bricklet");
        uidDeviceMap.put(BrickletSegmentDisplay4x7.DEVICE_IDENTIFIER, "7Segment-Bricklet");
        uidDeviceMap.put(BrickletRotaryPoti.DEVICE_IDENTIFIER, "RotaryPoti-Bricklet");
    }

    private Map<Integer, Bricklet> brickletMap = new HashMap<>();

    public BrickletReader readBricklets(String host, int port) throws Exception {
        IPConnection ipcon = new IPConnection();
        ipcon.connect(host, port);

        // Register enumerate listener and print incoming information
        ipcon.addEnumerateListener(new IPConnection.EnumerateListener() {
                                       @Override
                                       public void enumerate(String uid, String connectedUid, char position, short[] hardwareVersion, short[] firmwareVersion, int deviceIdentifier, short enumerationType) {
                                           if (enumerationType == IPConnection.ENUMERATION_TYPE_DISCONNECTED) {
                                               return;
                                           }
                                           brickletMap.put(deviceIdentifier, new Bricklet(uidDeviceMap.get(deviceIdentifier), uid));
                                       }
                                   }
        );

        ipcon.enumerate();

        //Wait to get result
        Thread.sleep(2000l);
        ipcon.disconnect();

        return this;
    }

    public Map<Integer, Bricklet> getBrickletMap() {
        return brickletMap;
    }

    public Bricklet getBrickletByDeviceId(int deviceId) {
        return brickletMap.get(deviceId);
    }
}
