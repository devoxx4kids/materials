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

        try {
            while (true) {
                System.out.print("Gib einen Text zum Morsen ein: ");
                String stringToMorse = System.console().readLine();

                String morseCode = "";
                for (int i = 0; i < stringToMorse.length(); i++) {
                    morseCode += encode(stringToMorse.substring(i,i+1))+" ";
                }

                System.out.println(morseCode);
                ps.morseCode(morseCode, 800);
            }
        } finally {
            ipcon.disconnect();
        }
    }

    public static String encode(String toEncode) {
        String morse = toEncode;

        if (toEncode.equalsIgnoreCase("a"))
            morse = ".-";
        if (toEncode.equalsIgnoreCase("b"))
            morse = "-...";
        if (toEncode.equalsIgnoreCase("c"))
            morse = "-.-.";
        if (toEncode.equalsIgnoreCase("d"))
            morse = "-..";
        if (toEncode.equalsIgnoreCase("e"))
            morse = ".";
        if (toEncode.equalsIgnoreCase("f"))
            morse = "..-.";
        if (toEncode.equalsIgnoreCase("g"))
            morse = "--.";
        if (toEncode.equalsIgnoreCase("h"))
            morse = "....";
        if (toEncode.equalsIgnoreCase("i"))
            morse = "..";
        if (toEncode.equalsIgnoreCase("j"))
            morse = ".---";
        if (toEncode.equalsIgnoreCase("k"))
            morse = "-.-";
        if (toEncode.equalsIgnoreCase("l"))
            morse = ".-..";
        if (toEncode.equalsIgnoreCase("m"))
            morse = "--";
        if (toEncode.equalsIgnoreCase("n"))
            morse = "-.";
        if (toEncode.equalsIgnoreCase("o"))
            morse = "---";
        if (toEncode.equalsIgnoreCase("p"))
            morse = ".--.";
        if (toEncode.equalsIgnoreCase("q"))
            morse = "--.-";
        if (toEncode.equalsIgnoreCase("r"))
            morse = ".-.";
        if (toEncode.equalsIgnoreCase("s"))
            morse = "...";
        if (toEncode.equalsIgnoreCase("t"))
            morse = "-";
        if (toEncode.equalsIgnoreCase("u"))
            morse = "..-";
        if (toEncode.equalsIgnoreCase("v"))
            morse = "...-";
        if (toEncode.equalsIgnoreCase("w"))
            morse = ".--";
        if (toEncode.equalsIgnoreCase("x"))
            morse = "-..-";
        if (toEncode.equalsIgnoreCase("y"))
            morse = "-.--";
        if (toEncode.equalsIgnoreCase("z"))
            morse = "--..";
        if (toEncode.equalsIgnoreCase("0"))
            morse = "-----";
        if (toEncode.equalsIgnoreCase("1"))
            morse = ".----";
        if (toEncode.equalsIgnoreCase("2"))
            morse = "..---";
        if (toEncode.equalsIgnoreCase("3"))
            morse = "...--";
        if (toEncode.equalsIgnoreCase("4"))
            morse = "....-";
        if (toEncode.equalsIgnoreCase("5"))
            morse = ".....";
        if (toEncode.equalsIgnoreCase("6"))
            morse = "-....";
        if (toEncode.equalsIgnoreCase("7"))
            morse = "--...";
        if (toEncode.equalsIgnoreCase("8"))
            morse = "---..";
        if (toEncode.equalsIgnoreCase("9"))
            morse = "----.";
        if (toEncode.equalsIgnoreCase("."))
            morse = ".-.-";
        if (toEncode.equalsIgnoreCase(","))
            morse = "--..--";
        if (toEncode.equalsIgnoreCase("?"))
            morse = "..--..";

        return morse;
    }

    public static String decode(String toEncode) {
        String morse = toEncode;

        if (toEncode.equalsIgnoreCase(".- "))
            morse = "a";
        if (toEncode.equalsIgnoreCase("-..."))
            morse = "b";
        if (toEncode.equalsIgnoreCase("-.-."))
            morse = "c";
        if (toEncode.equalsIgnoreCase("-.."))
            morse = "d";
        if (toEncode.equalsIgnoreCase("."))
            morse = "e";
        if (toEncode.equalsIgnoreCase("..-."))
            morse = "f";
        if (toEncode.equalsIgnoreCase("--."))
            morse = "g";
        if (toEncode.equalsIgnoreCase("...."))
            morse = "h";
        if (toEncode.equalsIgnoreCase(".."))
            morse = "i";
        if (toEncode.equalsIgnoreCase(".---"))
            morse = "j";
        if (toEncode.equalsIgnoreCase("-.-"))
            morse = "k";
        if (toEncode.equalsIgnoreCase(".-.."))
            morse = "l";
        if (toEncode.equalsIgnoreCase("--"))
            morse = "m";
        if (toEncode.equalsIgnoreCase("-."))
            morse = "n";
        if (toEncode.equalsIgnoreCase("---"))
            morse = "o";
        if (toEncode.equalsIgnoreCase(".--."))
            morse = "p";
        if (toEncode.equalsIgnoreCase("--.-"))
            morse = "q";
        if (toEncode.equalsIgnoreCase(".-."))
            morse = "r";
        if (toEncode.equalsIgnoreCase("..."))
            morse = "s";
        if (toEncode.equalsIgnoreCase("-"))
            morse = "t";
        if (toEncode.equalsIgnoreCase("..-"))
            morse = "u";
        if (toEncode.equalsIgnoreCase("...-"))
            morse = "v";
        if (toEncode.equalsIgnoreCase(".--"))
            morse = "w";
        if (toEncode.equalsIgnoreCase("-..-"))
            morse = "x";
        if (toEncode.equalsIgnoreCase("-.--"))
            morse = "y";
        if (toEncode.equalsIgnoreCase("--.."))
            morse = "z";
        if (toEncode.equalsIgnoreCase("-----"))
            morse = "0";
        if (toEncode.equalsIgnoreCase(".----"))
            morse = "1";
        if (toEncode.equalsIgnoreCase("..---"))
            morse = "2";
        if (toEncode.equalsIgnoreCase("...--"))
            morse = "3";
        if (toEncode.equalsIgnoreCase("....-"))
            morse = "4";
        if (toEncode.equalsIgnoreCase("....."))
            morse = "5";
        if (toEncode.equalsIgnoreCase("-...."))
            morse = "6";
        if (toEncode.equalsIgnoreCase("--..."))
            morse = "7";
        if (toEncode.equalsIgnoreCase("---.."))
            morse = "8";
        if (toEncode.equalsIgnoreCase("----."))
            morse = "9";
        if (toEncode.equalsIgnoreCase(" "))
            morse = "";

        return morse;
    }
}
