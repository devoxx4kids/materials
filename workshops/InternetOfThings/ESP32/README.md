# ESP32 Workshop: Program a Board with Blocks 📟

A Devoxx4Kids workshop for children aged 10 to 14. Working in pairs, they program an **M5Stack Core2** (an ESP32 board with a touch screen, motion sensor, speaker and vibration motor) with **MicroBlocks**, a free block language that looks like Scratch and runs the program on the board straight away.

Every mission takes **45 minutes** and works on its own, so you can run one, two or all three. Everything is available in English, French and Dutch.

## Missions, in the recommended order

| # | Mission | What the pair builds | What they learn | 🇬🇧 | 🇫🇷 | 🇳🇱 |
|---|---|---|---|---|---|---|
| 1 | Magic Shake Ball 🎱 | Ask a question, shake the board, get a random answer | Events, lists, random numbers, a sensor, screen/sound/vibration | [EN](missions/01-magic-shake-ball/en/mission.md) | [FR](missions/01-magic-shake-ball/fr/mission.md) | [NL](missions/01-magic-shake-ball/nl/mission.md) |
| 2 | The Bomb 💣 | Carry the bomb to the safe zone without jolting it, or BOOM | Variables that change over time, limits, a timer, pictures | [EN](missions/02-bomb/en/mission.md) | [FR](missions/02-bomb/fr/mission.md) | [NL](missions/02-bomb/nl/mission.md) |
| 3 | Emoji Messenger 📡 | Send emojis to other tables by radio, no Wi-Fi needed | Radio groups, messages, broadcast | [EN](missions/03-emoji-messenger/en/mission.md) | [FR](missions/03-emoji-messenger/fr/mission.md) | [NL](missions/03-emoji-messenger/nl/mission.md) |

**Start with Mission 1**: it introduces the blocks the other missions build on (the `when` block, the red circles, `show big text`, variables). Mission 2 adds variables that change while the program runs. Mission 3 comes last because it needs at least two boards per table and uses everything from before. A group that has never used MicroBlocks should always start with Mission 1; a group that already knows it can start with any mission.

Each mission has bonus cards for pairs that finish early, a starter project (`missions/*/starter/`, opened at the start of the session) and a finished version for coaches (`missions/*/solution/`).

## Step 1: Buy the hardware

Per session:

- **One M5Stack Core2 v1.3 per pair, plus two spares.** Buy the part number **K010-V13** (green power LED). Do not buy the Core2 v1.1 (K010-V11): its power chip is not supported by MicroBlocks.
- **One USB-C cable that carries data per board.** Charging-only cables are the most common reason a board "is not found".
- **One laptop per pair** (Windows, macOS, Linux or a Chromebook) with Chrome or Edge.

Distributors in Belgium (search for **K010-V13**):

- Mouser: https://www.mouser.be/
- RS Components: https://benl.rs-online.com/web/c/?searchTerm=esp32
- DigiKey: https://www.digikey.be/en/

Board details and handling rules: [coach/en/hardware.md](coach/en/hardware.md).

## Step 2: Install the workshop firmware on every board (once per board)

The boards need our **workshop firmware**, a build of MicroBlocks with a small patch, plus the Bomb pictures for Mission 2. Only the firmware on the board is patched: the MicroBlocks editor is the standard one, and our helper blocks travel inside the workshop projects.

1. On the computer you flash from, install Python 3 and the flashing tool (a virtual environment avoids conflicts with the system Python):

       python3 -m venv .venv
       . .venv/bin/activate
       pip install "esptool>=5"

   esptool 5 or newer is needed: older versions use other command names.
2. Download this workshop folder (it contains `firmware/microblocks-core2-v1.3.bin` and `firmware/bomb-images.bin`).
3. Close MicroBlocks, so that it does not hold the USB port, and connect the Core2 with a data cable.
4. Find the port: on macOS `/dev/cu.usbserial-…`, on Linux `/dev/ttyUSB0` or `/dev/ttyACM0`, on Windows `COM3` or similar (Device Manager). If no port appears on Windows, install the CH9102 USB driver linked from https://docs.m5stack.com/en/core/Core2_v1.3.
5. From the workshop folder, write both files (replace `<PORT>`):

       esptool --chip esp32 --port <PORT> --baud 460800 write-flash 0x0 firmware/microblocks-core2-v1.3.bin 0x210000 firmware/bomb-images.bin

6. Unplug the cable, switch the board off (hold the power button on the left side for 6 seconds) and on again (2 seconds), and plug the cable back in. On macOS this power cycle without USB is needed, otherwise the board does not start.

The board now shows the **Devoxx4Kids logo**: that is how you recognise the workshop firmware. It stays until a program draws something. A black screen at power-on means the board runs another firmware: flash it again. You can check the files with the SHA-256 values in [firmware/README.md](firmware/README.md).

**Never accept MicroBlocks' offer to update the board.** When the editor says *The MicroBlocks in your board is not current… Try to update MicroBlocks on the board?*, click **Cancel**: the update installs the standard firmware, without the vibration motor (and, until the next MicroBlocks release, without the motion sensor of the v1.3). If a board was updated anyway, flash it again as above.

## Step 3: Prepare the laptops (the day before)

1. Use MicroBlocks **3.0** (the tested version): open https://microblocks.fun and click **Run** in Chrome or Edge, or install the desktop app from https://microblocks.fun/download when the venue has no reliable internet.
2. Copy this workshop folder to every laptop, or at least the `missions/*/starter/*.ubp` files for your language.
3. Switch on a flashed board (the Devoxx4Kids logo appears), connect it, and check that MicroBlocks shows the board name **M5StackCore2**.
4. Click the **globe** icon and choose English, Français or Nederlands. Always open the starter project with the same language code (`-en`, `-fr`, `-nl`), so the helper blocks are in that language too.
5. Test each board: open `missions/01-magic-shake-ball/solution/magic-ball-done-en.ubp` (or `-fr`, `-nl`), click ▶ and shake the board. An answer appears, with a beep and a buzz.
6. For Mission 3, test the radio: open `missions/03-emoji-messenger/solution/emoji-messenger-done-en.ubp` on two boards and send an emoji from one to the other.
7. Charge every board, stick a number on the back of each board, and number the tables (in Mission 3 the table number is the radio group).

The same steps, in more detail and in three languages: [coach/en/setup.md](coach/en/setup.md), [coach/fr/setup.md](coach/fr/setup.md), [coach/nl/setup.md](coach/nl/setup.md).

## Step 4: Run the session

On the day: every laptop has MicroBlocks open, a board connected and the starter project open. Pairs swap roles (driver and navigator) at every step; coaches walk around and ask questions instead of taking the mouse. For Mission 2, mark a start point and a safe zone about 3 metres apart next to each table.

| | 🇬🇧 | 🇫🇷 | 🇳🇱 |
|---|---|---|---|
| Preparing laptops and boards | [EN](coach/en/setup.md) | [FR](coach/fr/setup.md) | [NL](coach/nl/setup.md) |
| Running a 45-minute session (timing, roles, radio groups, common problems) | [EN](coach/en/running-a-session.md) | [FR](coach/fr/running-a-session.md) | [NL](coach/nl/running-a-session.md) |
| The Core2 hardware | [EN](coach/en/hardware.md) | [FR](coach/fr/hardware.md) | [NL](coach/nl/hardware.md) |

## The firmware patch and MicroBlocks

The standard MicroBlocks firmware for the Core2 (`m5core2_1.0`) has three gaps on the Core2 v1.3. Our patch (`firmware/microblocks-core2-v1.3.patch`, against MicroBlocks `dev` at commit `f4767a3`, VM 425) fixes them. We reported each one to the MicroBlocks team on Codeberg (https://codeberg.org/MicroBlocks/smallvm, issues #1116, #1117 and #1118):

| Change | Why | Status in MicroBlocks |
|---|---|---|
| Motion sensor: read the BMI270 of the v1.3 | The v1.3 replaced the MPU6886, so shaking always read 0 | **Accepted**: added to the `dev` branch, in the next pilot release |
| Screen font: redrawn lowercase accents (é, è, ê, à…) | Accents looked like flat bars at large text sizes | **Accepted**: in the next pilot release |
| Vibration: a `setVibration` primitive for the motor | MicroBlocks has no block for the Core2's built-in motor | **Declined**: MicroBlocks only adds features that work across many boards, and this motor sits behind the Core2's AXP192 power chip. It stays in our patch |
| Start-up logo: the Devoxx4Kids logo at power-on | Shows at a glance that a board has the workshop firmware | Not proposed: specific to Devoxx4Kids |

What this means for the workshop:

- **Keep using the workshop firmware**, also after the next MicroBlocks release: only our build can switch the built-in vibration motor that the `vibrate for _ ms` block uses, and it shows the Devoxx4Kids logo at start-up.
- When the motion sensor and font fixes are in a MicroBlocks release, the patch can shrink to the vibration part only (see "Updating to a newer MicroBlocks" below).
- The MicroBlocks team suggests an external vibration motor, such as the M5Stack Vibration Motor Unit (https://shop.m5stack.com/products/vibration-motor-unit), for projects that should run on any board. The workshop does not need one: the built-in motor works with our firmware.
- Ideas for new MicroBlocks features are best discussed first on the MicroBlocks Discord; the team only accepts small, localized bug fixes as code.

### Rebuilding the firmware from source

You only need this to change the patch, the bomb pictures or the MicroBlocks version; the ready-made `.bin` files are in `firmware/`.

1. Install git and, in a virtual environment, the build tools:

       python3 -m venv .venv
       . .venv/bin/activate
       pip install platformio "esptool>=5"

2. From the workshop folder, run:

       firmware/build.sh

   The script clones MicroBlocks from Codeberg, checks out the commit in `BASE` (`f4767a3`), applies `firmware/microblocks-core2-v1.3.patch`, copies the bomb pictures (`firmware/images/*.data`) into the file system, builds the `m5core2` firmware and file system with PlatformIO, merges them into `firmware/microblocks-core2-v1.3.bin` and `firmware/bomb-images.bin`, and prints their SHA-256.
3. Flash a board as in Step 2 and run the hardware checks listed in [library/README.md](library/README.md).

### Updating to a newer MicroBlocks

1. Set `BASE` in `firmware/build.sh` to the new MicroBlocks commit.
2. Run `firmware/build.sh`. If `git apply` fails because MicroBlocks now contains the motion sensor or font fix, remove those parts from the patch (they touch `vm/sensorPrims.cpp`, `vm/bmi270config.h` and `vm/mbFont.c`) and keep the vibration and start-up logo parts (`vm/tftPrims.cpp`, `vm/ioPrims.cpp`, `vm/interp.h`).
3. Update the vendored libraries from the same commit (commands in [vendor/README.md](vendor/README.md)) and run `python3 tools/build.py`.
4. Update the commit and SHA-256 values in [firmware/README.md](firmware/README.md), flash a board and redo the hardware checks.

## For maintainers

The MicroBlocks files are generated. Do not edit `library/*.ubl` or the `.ubp` files in `missions/*/starter` and `missions/*/solution` by hand.

| Change | Edit | Then run |
|---|---|---|
| A block label or an on-screen text | `i18n/en.json`, `fr.json`, `nl.json` | `python3 tools/build.py` |
| Library behaviour | `src/library/Core2Buttons.ubl.tmpl` | `python3 tools/build.py` |
| A mission project | `src/projects/*.ubp.tmpl` | `python3 tools/build.py` |
| Bomb pictures | `src/images/*.gif`, frame lists in `tools/convert_images.py` | `python3 tools/convert_images.py`, then `firmware/build.sh` |
| Firmware patch | `firmware/microblocks-core2-v1.3.patch` | `firmware/build.sh` |
| Start-up logo | `src/images/devoxx4kids-logo.png` | `python3 tools/convert_logo.py`, then `firmware/build.sh` |
| Documentation | the `.md` files | `python3 tools/check_docs.py` |

Run the tests with `python3 -m pytest tools/tests -q` (needs `pip install -r tools/requirements-dev.txt`), and `python3 tools/build.py --check` to see whether the generated files are up to date. More about the helper blocks: [library/README.md](library/README.md). Vendored MicroBlocks libraries: [vendor/README.md](vendor/README.md). Firmware: [firmware/README.md](firmware/README.md). Design documents: `design/`. History: [CHANGELOG.md](CHANGELOG.md).

## Credits

Bomb and explosion animations: Noto Animated Emoji by Google, CC BY 4.0 (https://googlefonts.github.io/noto-emoji-animation/). MicroBlocks (https://microblocks.fun) is free software under the Mozilla Public License 2.0.
