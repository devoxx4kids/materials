# Option: our own Blockly editor for the Core2 workshop

Date: 2026-11-13
Status: **Option under consideration, not approved.** Nothing in this document may be built
until it has been reviewed and approved as a spec.
Related spec: `2026-11-11-esp32-magic-ball-workshop-design.md` (the workshop itself)

## 1. Why this option exists

The hardware test on two M5Stack Core2 v1.3 boards (K010-V13), done on 2026-11-13, showed:

- **MicroBlocks** (`vm_m5core2_1.0.bin`) does not work on the Core2 v1.3. The app runs, but
  the screen stays black, the LED is off, and the board never answers the IDE. A bug report
  has been drafted for the MicroBlocks maintainers.
- **UiFlow2 firmware 2.5.4** works on the Core2 v1.3: screen, the three touch circles (one
  event per touch, screen taps ignored), the BMI270 motion sensor, speaker, vibration, and
  ESP-NOW broadcast between two boards (5 of 5 messages received).
- The **UiFlow2 IDE**, M5Stack's own Blockly website, was rejected by the workshop owner for
  four reasons: its look, its English-only interface (EN, Chinese, Japanese), its very large
  number of blocks, and the need to be online.

This option keeps the firmware that works and replaces only the editor.

## 2. Idea

```
Our editor (static web page, works offline)        M5Stack Core2 v1.3
┌──────────────────────────────────────┐   USB    ┌─────────────────────────────┐
│ Google Blockly, "zelos" renderer      │ ───────▶ │ UiFlow2 firmware            │
│ (looks like Scratch)                  │   Web    │ (MicroPython + M5Stack      │
│ ~15 workshop blocks, labels EN/FR/NL  │  Serial  │  drivers, tested on v1.3)   │
│ generates MicroPython                 │          │                             │
└──────────────────────────────────────┘          └─────────────────────────────┘
```

- **Run:** sends the generated program to the board's MicroPython prompt (raw paste mode),
  so it starts at once. This is the method used for every hardware test on 2026-11-13.
- **Save to board:** writes the program as `main.py`, so it keeps running on battery without
  the laptop. Mission 2 (passing the Hot Potato around the table) needs this.
- **Save / open project:** a local file, with no account and no cloud.

## 3. What the option promises

| The workshop owner's objection to UiFlow2 | How this option answers it |
|---|---|
| The look | Blockly's "zelos" renderer, which is close to Scratch |
| English only | Blockly's built-in translations for its own blocks (French and Dutch to be verified), and our blocks' labels from `i18n/<lang>.json` (EN, FR, NL), following the rule that no text is hardcoded in the front end |
| Too many blocks | A toolbox with only the blocks the missions need, with names that make sense to children (e.g. `when middle button touched`, `board shaken?`, `vibrate for _ ms`) |
| Online only | A static page that can run from the laptop; the libraries are copied into the project, not loaded from a CDN |

## 4. Candidate block set

Events: `when started`, `when left/middle/right button touched`, `when board shaken`,
`when a message arrives`.
Screen: `show big text _ colour _`, `clear screen`.
Sound and feel: `beep _ Hz for _ ms`, `vibrate for _ ms`.
Radio: `set radio group _`, `send message _ number _`, `message text`, `message number`.
Plus Blockly's standard blocks, limited to: logic (if/else, compare, and/or/not), loops
(repeat, repeat until), maths (number, random, arithmetic), text (join), lists (create,
item, length), variables, wait.

Each block generates MicroPython for the UiFlow2 firmware API (`M5`, `BtnA`/`BtnB`/`BtnC`,
`Imu.getAccel()`, `Speaker.tone()`, `Power.setVibration()`, `espnow` broadcast with the
group number inside each message). All of these were verified on the Core2 v1.3.

## 5. Alternatives considered

| Approach | Verdict |
|---|---|
| Our own editor on the UiFlow2 firmware (this option) | Recommended: least new code, drivers already proven |
| Our own editor on plain MicroPython firmware with our own drivers | Rejected for now: we would have to write and maintain drivers for the screen, touch, BMI270, power chip and speaker |
| Adapt BIPES (Blockly + MicroPython + Web Serial) | Ideas only: BIPES is GPL-3.0, so reusing its code would make our editor GPL; its look, blocks and languages would also need rework |
| Use the UiFlow2 IDE as is | Rejected by the workshop owner (see section 1) |

## 6. Licences

- Google Blockly: Apache-2.0.
- UiFlow2 firmware (m5stack/uiflow-micropython): MIT.
- BIPES: GPL-3.0. Do not copy its code.

## 7. Decomposition, if approved

- **Project A: the editor.** Its own spec, plan and review. Must come first, because the
  workshop pages show its blocks.
- **Project B: the workshop materials.** The existing workshop spec, revised for the
  editor's block names. Missions, the 45-minute rhythm, pairs, the EN/FR/NL pages, and the
  optional AiFlow "Mission 4" (coach-led) stay.

## 8. Open questions and risks, to settle before approval

1. **Web Serial needs Chrome or Edge,** and a "secure context". Check whether the page works
   when opened as a local file (`file://`), or needs `localhost` or https.
2. **macOS USB quirk:** on the Core2's CH9102 chip, resets triggered while the port is open
   enter download mode. Opening the port with UiFlow2 firmware did start normally during the
   tests, but the editor must never toggle the reset lines itself.
3. **Firmware installation for coaches:** UiFlow2 2.5.4 was written with esptool
   (`write-flash 0x0`, SHA-256 `46b55991…6ce4`). Decide between M5Burner, esptool, or a
   flash button in the editor (esptool-js).
4. **Blockly FR/NL:** confirm that Blockly's current release ships French and Dutch message
   files.
5. **Effort:** a first usable version is estimated at a few days of work. Maintenance against
   UiFlow2 firmware updates is ongoing; pin a tested firmware version.
6. **MicroBlocks:** if the maintainers fix Core2 v1.3 support, MicroBlocks would also answer
   all four objections (Scratch-like, FR/NL, few blocks, offline) without building an editor.
   The MicroBlocks work from Tasks 1–6 is kept in git for that case.
