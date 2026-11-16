# Preparing laptops and boards

Do this the day before. Allow about 5 minutes per board.

## 1. Laptops

- Install Chrome or Edge, or the MicroBlocks desktop app from https://microblocks.fun/download (use the app when the venue has no reliable internet).
- Download this workshop folder to each laptop, or put the `missions/*/starter/*.ubp` files for your language on a USB stick.
- Check each cable: a charging-only USB-C cable is the most common reason a board "is not found". Label the cables that work.

## 2. Install the workshop firmware on each Core2 (once)

The standard MicroBlocks firmware does not support the Core2 v1.3 fully. Use the workshop firmware from `firmware/` (MicroBlocks with a small patch for the v1.3 motion sensor and vibration motor, plus the bomb pictures for Mission 2).

1. Install Python 3 and esptool once: `pip install "esptool>=5"` (older esptool versions use other command names).
2. Close MicroBlocks, connect the Core2 with a data cable, and run from the workshop folder (replace `<PORT>`; on macOS it looks like `/dev/cu.usbserial-…`):

       esptool --chip esp32 --port <PORT> --baud 460800 write-flash 0x0 firmware/microblocks-core2-v1.3.bin 0x210000 firmware/bomb-images.bin

3. Unplug the cable, switch the board off (hold the left button 6 seconds) and on again (2 seconds), and plug the cable back in.
4. Open MicroBlocks (https://microblocks.fun → **Run**), connect, and check that the board name is **M5StackCore2**.
5. Open `missions/01-magic-shake-ball/solution/magic-ball-done-en.ubp`, click ▶ and shake the board: an answer appears, with a beep and a buzz. The board is ready.

The screen stays black and the green LED stays off until a program draws something: that is normal.

## 3. Language

Click the **globe** icon in MicroBlocks and choose English, Français or Nederlands. Then open the starter project with the same language code (`-en`, `-fr` or `-nl`), so the helper blocks are in that language too.

## 4. Boards

- Charge every board fully (the battery lasts a session; bring chargers anyway).
- Stick a number on the back of every board, and number the tables. In Mission 3 the table number is the radio group.
- Keep two spare boards ready with the firmware installed.

## 5. Quick test of the radio (only for Mission 3)

Open `missions/03-emoji-messenger/solution/emoji-messenger-done-en.ubp` on two boards and send an emoji from one to the other. See [running a session](running-a-session.md) for the group numbers.
