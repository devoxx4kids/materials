#!/bin/bash -e

PROGRAM=$1

cd $PROGRAM
echo $PROGRAM

#Check wether target directory exists
if [ ! -d "target" ]; then
 mkdir target
fi

#Check wether brickletreader.jar exists
if [ ! -f "../brickletreader.jar" ]; then

    echo "Creating brickletreader.jar"

    cd ../BrickletReader
    echo "Switching to BrickletReader"

    #brickletreader/target exists
    if [ ! -f "target" ]; then
        mkdir target
    fi

    #Compile
    javac -d target -cp ../tinkerforge-2.1.4.jar src/main/java/org/devoxx4kids/*.java
    echo "BrickletReader compiled"

    #Create jar
    pwd
    jar cvf ../brickletreader.jar -C target org/devoxx4kids

    cd ../$PROGRAM
fi

#Compile and start program
javac -d target -cp ../tinkerforge-2.1.4.jar:../brickletreader.jar src/main/java/org/devoxx4kids/*.java
java -classpath ../tinkerforge-2.1.4.jar:../brickletreader.jar:target org.devoxx4kids.Main

