# ESP32 Workshop: Magic Shake Ball, Hot Potato & Emoji Messenger — Design

Date: 2026-11-11
Status: Approved in conversation, pending written-spec review
Location of the workshop: `workshops/InternetOfThings/ESP32/`

## 1. Intent

A new Devoxx4Kids workshop in which children aged 10–14 program an ESP32 board with
Scratch-like blocks and build something fun they can show their friends.

Success criteria:

- Every pair finishes the core of the mission they attend and has a working program on
  the board.
- Every pair changes the program to make it their own (answers, colours, sounds).
- A volunteer coach with no prior ESP32 knowledge can run a session from the coach docs.
- Each mission fits a 45–50 minute session and can be run on its own.

## 2. Decisions

| Topic | Decision |
|---|---|
| Audience | Children 10–14, working in pairs (driver / navigator, swap at each step) |
| Session format | Modular: three standalone missions of 45–50 minutes each |
| Hardware | M5Stack Core2 (ESP32, touch screen, IMU, speaker, vibration motor), one per pair plus two spares per session |
| Programming tool | MicroBlocks (Scratch-like, live programming, runs in Chrome/Edge or as an offline app) |
| Board-to-board communication | MicroBlocks `ESP Now` library (peer-to-peer, no Wi-Fi router needed, groups 0–255) |
| Missions | 1. Magic Shake Ball (core) → 2. Hot Potato / Duel → 3. Emoji Messenger |
| Documentation | Markdown only, own structure (not the AsciiDoc layout of other workshops) |
| Languages | English, French, Dutch |

Rejected alternatives:

- Mind+ (real Scratch 3 look): ESP32 runs only in upload mode, so every change costs a
  compile-and-flash cycle, which does not fit a 45-minute session.
- UIFlow2: official M5Stack support, but Blockly/MicroPython looks less like Scratch.
- M5StickC Plus2: cheaper, but not explicitly supported by MicroBlocks firmware.
- One long linear ladder or free-choice quest cards only: neither gives a complete,
  standalone 45-minute session.

## 3. Folder structure

```
workshops/InternetOfThings/ESP32/
├── README.md                       entry point: what it is, missions, links per language
├── CHANGELOG.md                    one version entry per day
├── coach/
│   ├── en/  setup.md  running-a-session.md  hardware.md
│   ├── fr/  (same files)
│   └── nl/  (same files)
├── missions/
│   ├── 01-magic-shake-ball/
│   │   ├── en/  mission.md  bonus-cards.md
│   │   ├── fr/  (same files)
│   │   ├── nl/  (same files)
│   │   ├── starter/   magic-ball-start.ubp
│   │   ├── solution/  magic-ball-done.ubp
│   │   └── images/
│   ├── 02-hot-potato/        (same layout: hot-potato-start.ubp, hot-potato-done.ubp)
│   └── 03-emoji-messenger/   (same layout: emoji-messenger-start.ubp, emoji-messenger-done.ubp)
└── library/
    ├── Core2Buttons.ubl
    └── README.md
```

Rules:

- `mission.md` is written for the children: short numbered steps, large screenshots,
  a "Try it!" checkpoint after each step, and a role-swap reminder at each step.
- `bonus-cards.md` contains self-contained challenges, each one short enough to print
  as a single card.
- Coach material lives only in `coach/`, never in the children's pages.
- Images are shared between languages and contain no text. When a screenshot must show
  block labels, one file per language is provided, named `<name>-en.png`,
  `<name>-fr.png`, `<name>-nl.png`.
- Every language folder contains the same file names.

## 4. Session rhythm (all missions)

| Minutes | Activity |
|---|---|
| 0–5 | Intro and live demo of the finished mission by the coach |
| 5–30 | Core steps ⭐1–⭐4 (swap driver/navigator at each ⭐) |
| 30–40 | Bonus cards, chosen freely by each pair |
| 40–45 | Show & tell: pairs demo to their neighbours |

## 5. Mission content

### Mission 1 — Magic Shake Ball

| Step | The pair builds | New idea |
|---|---|---|
| ⭐1 | Touch the middle button → the screen says "Ask me a question!" | events, display |
| ⭐2 | Touch → show a random answer from a list (Yes / No / Maybe / Ask again) | lists, random |
| ⭐3 | Shake the board instead of touching → an answer appears | sensors (IMU) |
| ⭐4 | Add a sound or vibration and a colour per answer | output, if/else |

Bonus cards: own funny answers · emoji faces drawn with shapes · secret cheat button
that always says YES · counter of questions asked.

### Mission 2 — Hot Potato / Duel

| Step | The pair builds | New idea |
|---|---|---|
| ⭐1 | Touch "start" → wait a random 5–15 s → "BOOM!" with vibration | timers, wait |
| ⭐2 | Ticking sound that speeds up as the time runs out | loops, variables |
| ⭐3 | Pass the board around the table; whoever holds it at BOOM loses a life; lives shown on screen | variables, game state |
| ⭐4 | Reaction duel: after a beep, left vs right button, first touch wins; touching before the beep shows "Too early!" | comparison, fairness |

Bonus cards: tilt to defuse · high score · pair-vs-pair duel over ESP Now (the start
signal is sent to both boards), which leads into Mission 3.

### Mission 3 — Emoji Messenger

| Step | The pair builds | New idea |
|---|---|---|
| ⭐1 | Set the ESP Now group to the table number; touch → send "hello"; show what arrives | radio, groups |
| ⭐2 | Left/right buttons scroll through a list of emojis, middle button sends the chosen one | lists, index |
| ⭐3 | A received emoji pops up with a sound and the sender's pair name | name = value pairs |
| ⭐4 | Shake to send to everyone in the group | broadcast |

Bonus cards: secret code (Caesar shift) · team channels · fortune delivery: send a
Magic Ball answer to another table (links back to Mission 1).

Emojis are drawn with simple shapes and characters on the screen; no image or font
files are loaded onto the board.

Each mission starts from its own starter project, so it does not require the previous
mission to have been done.

## 6. Helper library `library/Core2Buttons.ubl`

The Core2's three red circles under the screen are touch zones, not physical buttons, and
MicroBlocks defines no `button A` pin for the Core2. The library hides this and other
board details behind child-friendly blocks:

| Block | Hides |
|---|---|
| `left button touched?`, `middle button touched?`, `right button touched?` | touch Y below the display area and X ranges of the three circles |
| `when <left/middle/right> button touched` (hat block) | edge detection, fires once per touch |
| `board shaken?` | acceleration magnitude above a threshold (value set during the spike) |
| `vibrate for (ms)` | switching the AXP192-driven vibration motor on and off |
| `beep (note) for (ms)` | sound on the I2S speaker; only added if the built-in `play tone` block does not sound on the Core2 |
| `show big text (text) colour (c)` | centred, large text on the TFT display |

Translations: block labels are provided through MicroBlocks translation entries for EN,
FR and NL, so the blocks follow the language chosen in MicroBlocks. No label text is
hardcoded in a single language.

Starter projects already include this library and an empty "start here" script.
Solution projects contain the finished core plus every bonus card, for coaches.

## 7. Coach documentation

- `setup.md`: installing the MicroBlocks firmware on each Core2 before the event (browser
  in Chrome/Edge, or offline app); laptop checklist (browser or app, USB-C cable that
  carries data); charging the boards.
- `running-a-session.md`: the 45-minute timing plan, driver/navigator roles, ESP Now
  group numbering per table, and the five most common problems:

  | Symptom | Fix |
  |---|---|
  | Board not found | Replug; use a data USB-C cable; reload the page or restart the app |
  | Screen black | Press the power button; charge the board |
  | Buttons don't react | Open the starter project so the helper library is loaded |
  | Messages don't arrive | Both boards must use the same ESP Now group |
  | No sound | Check volume; use the vibration block instead |

- `hardware.md`: what the Core2 contains, how to handle and charge it, quantities
  (one per pair plus two spares), optional cases.

## 8. Risks and spike checks

To be verified on two real Core2 boards before the final screenshots are made:

1. MicroBlocks firmware installs and connects, both from the browser and the offline app.
2. The touch-zone button blocks detect each of the three circles reliably.
3. The built-in `play tone` block makes sound on the Core2; otherwise the `beep` block is
   added to the library.
4. A shake threshold that triggers on a deliberate shake but not when a child just holds
   the board.
5. ESP Now messages between two boards using groups; behaviour with as many nearby
   boards as are available.
6. FR and NL labels show for both the built-in blocks and the helper library blocks.

Results are recorded in `library/README.md` (library behaviour) and `coach/*/setup.md`
(setup steps).

## 9. Validation of the materials

- Every starter project opens in MicroBlocks without errors.
- Every solution project runs its mission end to end on a Core2.
- One adult dry-runs each mission with a timer; the core must take at most 20 minutes
  for an adult (children take about 1.5× longer, which fits the 25-minute core slot).
- All Markdown links resolve, and the EN, FR and NL folders contain the same files.
- `CHANGELOG.md` gets one entry per day of changes.

## 10. Out of scope

- Other boards than the M5Stack Core2.
- Wi-Fi router, internet or cloud features (MQTT, web dashboards).
- PDF or slide exports of the materials.
- Languages other than EN, FR and NL.
