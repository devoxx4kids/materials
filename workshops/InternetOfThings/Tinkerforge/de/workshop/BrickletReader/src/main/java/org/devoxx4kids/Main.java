package org.javaland4kids;

import com.tinkerforge.BrickletPiezoSpeaker;
import com.tinkerforge.BrickletRotaryPoti;
import com.tinkerforge.BrickletSegmentDisplay4x7;
import com.tinkerforge.IPConnection;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by alexanderbischof on 22.09.14.
 */
public class Main {

    //build: jar cvf brickletreader.jar -C src org
    public static void main(String[] args) throws Exception {

        //Standard localhost und Port 4223 kann über Kommandozeilen-Parameter überschrieben werden.
        String host = "localhost";
        int port = 4223;
        if (args.length>=2){
            host = args[0];
            port = Integer.valueOf(args[1]);
        }

        BrickletReader brickletReader = new BrickletReader();
        System.out.println(brickletReader.readBricklets(host, port).getBrickletMap().values());
    }
}
