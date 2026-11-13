# MicroBlocks firmware for the M5Stack Core2 v1.3

The standard MicroBlocks Core2 firmware (`m5core2_1.0`) does not read the motion sensor of
the **Core2 v1.3 (K010-V13)**, and it cannot switch the vibration motor. This folder holds a
patched build that fixes both, until the fix is included in MicroBlocks itself.

| File | What it is |
|---|---|
| `microblocks-core2-v1.3.bin` | Complete flash image (bootloader, partition table, boot selector, MicroBlocks VM), to be written at address `0x0` |
| `microblocks-core2-v1.3.patch` | The source change, against MicroBlocks `dev` at commit `b40b74d` (Codeberg) |

SHA-256 of the image:
`b1a4e25a61b92775c91c4a2083f43a0a0e417c2d0cb828e86bd5924cbf0ed4e8`

## What the patch changes

- **Motion sensor:** at start-up, the Core2 build checks which chip is at I2C address 0x68
  on the internal bus. If it is a BMI270 (chip ID 0x24, Core2 v1.3) instead of an MPU6886
  (older Core2), it loads the BMI270 configuration and reads it. `acceleration`, `tilt x/y/z`
  and the Core2Buttons block `board shaken?` work with the same scale as before (100 = 1 g).
  The older Core2 boards keep their original code path.
- **Vibration:** a new primitive, `[tft:setVibration] true/false`, switches the motor
  (output LDO3 of the AXP192 power chip). The Core2Buttons block `vibrate for _ ms` uses it.

Tested on 2026-11-13 on a Core2 v1.3: acceleration reads 99 at rest and changes when the
board is tilted or shaken; the motor switches on and off on command.

## Install on a board

You need Python 3 and esptool (`pip install esptool`). Close MicroBlocks first, so that it
does not hold the USB port.

```bash
esptool --chip esp32 --port <PORT> --baud 460800 write-flash 0x0 microblocks-core2-v1.3.bin
```

On macOS the port looks like `/dev/cu.usbserial-XXXXXXXX`. After flashing, unplug the USB
cable, switch the board off (hold the left button about 6 seconds) and on again (about
2 seconds), then plug the cable back in and connect from MicroBlocks.

The screen stays black and the green LED stays off until a program draws something: that is
normal with MicroBlocks.

## Rebuild from source

```bash
git clone --branch dev https://codeberg.org/MicroBlocks/smallvm.git
cd smallvm
git checkout b40b74d
git apply ../microblocks-core2-v1.3.patch
pip install platformio
pio run -e m5core2
```

The image above was made from the build output with:

```bash
esptool --chip esp32 merge-bin --flash-size 16MB -o microblocks-core2-v1.3.bin \
  0x1000 .pio/build/m5core2/bootloader.bin 0x8000 .pio/build/m5core2/partitions.bin \
  0xe000 <platformio>/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin \
  0x10000 .pio/build/m5core2/firmware.bin
```

MicroBlocks is licensed under the Mozilla Public License 2.0; this patch and image keep that
license.
