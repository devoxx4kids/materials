# MicroBlocks firmware for the M5Stack Core2 v1.3

The standard MicroBlocks Core2 firmware (`m5core2_1.0`) does not read the motion sensor of the **Core2 v1.3 (K010-V13)**, and it cannot switch the vibration motor. This folder holds a patched build that fixes both, until the fix is included in MicroBlocks itself.

| File | What it is |
|---|---|
| `microblocks-core2-v1.3.bin` | Complete flash image (bootloader, partition table, boot selector, MicroBlocks VM), to be written at address `0x0` |
| `microblocks-core2-v1.3.patch` | The source change, against MicroBlocks `dev` at commit `f4767a3` (Codeberg, IDE 3.0.0 / VM 425) |
| `bomb-images.bin` | LittleFS file system with the 21 bomb frames and their colour palette (Mission 2), to be written at address `0x210000` |
| `images/` | The 21 frames and `bomb_palette.data` as separate files (made by `tools/convert_images.py`) |
| `build.sh` | Rebuilds both images from source |

SHA-256 (build of 2026-11-16):

| File | SHA-256 |
|---|---|
| `microblocks-core2-v1.3.bin` | `41b2cd3b4278e5838f30c9d7c7a320b21185c69d91ee217fced423d415730071` |
| `bomb-images.bin` | `c53b7406a199214390f66e6edd7957c7a5439bbde57927ff79b6c5eba47f64f3` |

ESP32 builds embed the build time, so a rebuild from the same source gives a different SHA-256 for `microblocks-core2-v1.3.bin`.

## What the patch changes

- **Motion sensor:** at start-up, the Core2 build checks which chip is at I2C address 0x68 on the internal bus. If it is a BMI270 (chip ID 0x24, Core2 v1.3) instead of an MPU6886 (older Core2), it loads the BMI270 configuration and reads it. `acceleration`, `tilt x/y/z` and the Core2Buttons block `board shaken?` work with the same scale as before (100 = 1 g). The older Core2 boards keep their original code path.
- **Vibration:** a new primitive, `[tft:setVibration] true/false`, switches the motor (output LDO3 of the AXP192 power chip). The Core2Buttons block `vibrate for _ ms` uses it.
- **Accents:** the lowercase accented letters of MicroBlocks' 5 × 7 screen font (à á â ä ç è é ê ë ì í î ï ò ó ô ö ù ú û ü) are redrawn with a two-row accent above the plain letter. The original glyphs used a single pixel row, so at text size 4 every accent looked like a flat bar. Capitals are unchanged (the font has no room above them).

Tested on 2026-11-13 on a Core2 v1.3: acceleration reads 99 at rest and changes when the board is tilted or shaken; the motor switches on and off on command.

## Install on a board

You need Python 3 and esptool 5 or newer (`pip install "esptool>=5"`; older versions use other command names). Close MicroBlocks first, so that it does not hold the USB port.

```bash
esptool --chip esp32 --port <PORT> --baud 460800 write-flash 0x0 microblocks-core2-v1.3.bin 0x210000 bomb-images.bin
```

On macOS the port looks like `/dev/cu.usbserial-XXXXXXXX`. After flashing, unplug the USB cable, switch the board off (hold the left button about 6 seconds) and on again (about 2 seconds), then plug the cable back in and connect from MicroBlocks.

The screen stays black and the green LED stays off until a program draws something: that is normal with MicroBlocks.

## Rebuild from source

Run `firmware/build.sh` from the workshop folder. It clones MicroBlocks `dev` at `f4767a3` (VM 425), applies the patch, copies `firmware/images/*.data` into the file system, builds both images and prints their SHA-256. It needs git, and Python 3 with `platformio` and `esptool`.

MicroBlocks is licensed under the Mozilla Public License 2.0; this patch and image keep that license.

Bomb and explosion animations: Noto Animated Emoji by Google, CC BY 4.0 (https://googlefonts.github.io/noto-emoji-animation/).
