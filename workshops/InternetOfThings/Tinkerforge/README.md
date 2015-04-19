# Workshop session Tinkerforge (Devoxx4Kids)

## Introduction
The Tinkerforge workshop's material used for the Devoxx4kids session organised by the Oliver Milke and Alexander Bischof.

## Requirements
This workshop uses the following Tinkerforge hardware http://http://www.tinkerforge.com/

    * Masterbrick
    * BrickletDistanceIR
    * BrickletPiezoSpeaker
    * BrickletRotaryPoti
    * BrickletSegmentDisplay4x7

and was used on a standard raspberry pi's.

## Standard Build
The standard build tool for the examples is maven which can be used as follows:

    1. <parent>: mvn clean install
    2. <parent/examplexyz>: mvn assembly:assembly

After that every example can be started with:

    java -jar examplexyz-1.0-jar-with-dependencies.jar
    
Note: The project BrickletReader is not an example but rather a helper project so that kids do not have to input
the individual sensor ids. It is a dependency of every example and therefore has to be build before.

## Shell Build
The workshop is used on raspberry pi's with no maven installed until now. In order to be flexible so that children
who are experienced enough can implement things with Tinkerforge we decide to provide a shell build with build.sh too.
The script takes the example name as a parameter and compiles the java classes and starts afterwards the example.

    ./build.sh examplexyz