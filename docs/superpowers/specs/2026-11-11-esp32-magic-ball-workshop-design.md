# ESP32 Workshop: Magic Shake Ball, Bomb & Emoji Messenger — Design

Date: 2026-11-11
Status: Approved in conversation, pending written-spec review
Location of the workshop: `workshops/InternetOfThings/ESP32/`

> **Platform status (2026-11-13, updated): MicroBlocks, with our Core2 v1.3 firmware patch.**
> The stable MicroBlocks firmware (VM 411) does not run on the Core2 v1.3. The pilot firmware
> (VM 424, `m5core2_1.0` from the pilot channel) does: connection, screen, touch circles,
> beep, and ESP Now between two boards all pass. Two gaps remained, the BMI270 motion
> sensor (read as 0) and the vibration motor (unreachable); both are fixed by our patch in
> `firmware/` (tested: acceleration 99 at rest, motor on and off, Magic Ball and Emoji
> Messenger fully working). The patch is to be offered to the MicroBlocks maintainers
> (`docs/superpowers/reports/`). UiFlow2's IDE was rejected (look, English only, too many
> blocks, online only); our own Blockly editor stays a parked option
> (`2026-11-13-core2-blockly-editor-option.md`, not approved). Optional, coach-led
> Mission 4 with M5Stack AiFlow: decided, to be specified.

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
| Hardware | M5Stack Core2 v1.3, part K010-V13 (ESP32, touch screen, BMI270 IMU, speaker, vibration motor, AXP192 power chip), one per pair plus two spares per session. Not the Core2 v1.1 (K010-V11, AXP2101 power chip). |
| Programming tool | MicroBlocks (Scratch-like, live programming, runs in Chrome/Edge or as an offline app), pilot release (IDE 2.5.15 / 3.0 preview, VM 424 or later), with the Devoxx4Kids firmware for the Core2 v1.3 from `firmware/` until the patch is included upstream |
| Board-to-board communication | MicroBlocks `ESP Now` library (peer-to-peer, no Wi-Fi router needed, groups 0–255) |
| Missions | 1. Magic Shake Ball (core) → 2. Bomb → 3. Emoji Messenger (→ optional 4. Ask the AI, coach-led) |
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
│   │   ├── starter/   magic-ball-start-en.ubp  -fr.ubp  -nl.ubp   (generated)
│   │   ├── solution/  magic-ball-done-en.ubp   -fr.ubp  -nl.ubp   (generated)
│   │   └── images/
│   ├── 02-bomb/              (same layout: bomb-start-<lang>.ubp, bomb-done-<lang>.ubp)
│   └── 03-emoji-messenger/   (same layout: emoji-messenger-start-<lang>.ubp, emoji-messenger-done-<lang>.ubp)
├── library/
│   ├── Core2Buttons-en.ubl  -fr.ubl  -nl.ubl   (generated)
│   └── README.md
├── i18n/          en.json  fr.json  nl.json   all translatable strings (block labels, on-screen texts)
├── src/           templates: library/Core2Buttons.ubl.tmpl, projects/*.ubp.tmpl
├── vendor/        pinned copies of the MicroBlocks Tone and ESP Now libraries (MPL-2.0)
└── tools/         build.py (generates the files above), check_docs.py, tests/
```

Amendment (2026-11-11, during planning): a MicroBlocks library cannot reliably carry its
own FR/NL translations. The loader for localized libraries exists in the IDE source but
nothing calls it, and the IDE's `.po` files are maintained upstream. So translations live
in `i18n/<lang>.json`, and `tools/build.py` generates one library file and one starter and
solution project per language from the templates. No label or on-screen text is
hardcoded in a template.

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

### Mission 2 — Bomb (amendment 2026-11-13, replaces Hot Potato)

Hot Potato was dropped because children passing the board around would drop it. In the
Bomb, carefulness is the game: the pair carries the board ("the bomb") from a start point
to a safe zone marked on the table by a coach, without jolting it.

| Step | The pair builds | New idea |
|---|---|---|
| ⭐1 | `when started` → `show bomb calm`; touch the middle circle → "Go!" and the timer starts | events, images |
| ⭐2 | A `forever` loop shows the `jolt` value as a number while the children move the board | sensors, live numbers |
| ⭐3 | Danger meter: variable `danger` goes up with every jolt and slowly back down while the board is held steadily. Over 50 → `show bomb nervous` and faster beeps; over 100 → `show bomb explode`, a long buzz, game over. `show danger bar (danger)` along the bottom of the screen | variables that change over time, if/else, thresholds |
| ⭐4 | Safe place: touching the middle circle there → `show bomb safe` (confetti) and "SAFE!" with the time in seconds | timer, end of game |

The limits 50 and 100 and the per-jolt increase are starting values; they are tuned on
the hardware during the Bomb spike (section 8).

Bonus cards: reaction duel as "bomb squad training" (right circle, "GO!", first touch
wins; the board stays on the table) · expert mode (nervous at 30, boom at 60) · record:
the fastest safe time · a longer route around the room, pairs taking turns.

Safety notes for coaches: carry the board with two hands, above the table or close to the
floor, walking, never running.

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
| `board shaken?` | acceleration magnitude above a threshold (value set during the spike) |
| `vibrate for (ms)` | switching the AXP192-driven vibration motor on and off |
| `beep (frequency) for (ms)` | sound on the I2S speaker via the Tone library; falls back to vibration if the spike shows the speaker stays silent |
| `show big text (text) colour (c)` | centred, large text on the TFT display |
| `show bomb [calm / nervous / explode / safe]` | drawing the bomb images and animations (Mission 2) |
| `jolt` | how strongly the board moves right now (0 = still): the difference between `acceleration` and 100 |
| `show danger bar (value)` | a green → orange → red bar along the bottom of the screen |

Amendment 2026-11-13: `vibrate for (ms)` uses the `[tft:setVibration]` primitive of the
patched firmware; `beep` works with the Tone library on the pilot firmware. Every beep and
buzz also flashes a yellow frame around the screen.

### Images (amendment 2026-11-13)

The bomb pictures are frames of Google's Noto Animated Emoji, licensed CC BY 4.0:
💣 bomb (frame 6 = calm, frames 10–21 = nervous, frames 25 onward = the confetti used for
"safe") and 💥 collision (explode). They are converted to the screen's palette format by
`tools/build.py` and credited in `README.md` and `coach/<lang>/hardware.md`:
"Bomb and explosion animations: Noto Animated Emoji by Google, CC BY 4.0
(https://googlefonts.github.io/noto-emoji-animation/)". The source GIFs are kept in
`src/images/` with their licence.

The three button reporters are edge-detected: they report true once per touch. Children
combine them with MicroBlocks' built-in `when` hat block, so a separate custom hat block
is not needed (amendment 2026-11-11: none of the bundled MicroBlocks libraries define their
own hat blocks, so we use the built-in one children already know).

Translations: block labels and on-screen texts come from `i18n/<lang>.json` and are
written into one generated library file per language (see the amendment in section 3).
No label text is hardcoded in a single language.

Starter projects already include this library and an empty "start here" script.
Solution projects contain the finished core of the mission, for coaches. Each bonus card
carries a short hint for coaches and fast pairs instead of a full solution project
(amendment 2026-11-11, to keep the generated projects small and testable).

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

Platform decision (amendment 2026-11-11, after checking the Core2 revisions): MicroBlocks'
Core2 firmware reads the motion sensor as an MPU6886, but the Core2 v1.3 has a BMI270, so
shaking is expected to fail until verified on a real board. The hardware test therefore
ends with a decision:

- MicroBlocks, when all checks pass or have a fallback;
- MicroBlocks with a firmware patch, when only shaking fails because of the BMI270
  (MicroBlocks already contains a BMI270 driver for another board; the patch enables it
  for the Core2 and is offered upstream);
- UiFlow2 (M5Stack's own block tool, official support for the Core2 v1.3) as the
  fallback, when the screen, touch or several outputs fail. UiFlow2 is Blockly rather
  than Scratch-like, needs MAC-address peers for ESP-NOW, and its interface exists only
  in English and Japanese (github.com/m5stack/uiflow-i18n, uiflow-2.x), so choosing it
  requires a spec revision before the materials are written.

Mind+ was also evaluated and rejected: no Core2 support (a full custom extension would be
needed), compile-and-upload on every change, no Dutch interface, and an outdated macOS
version.

### Bomb spike (amendment 2026-11-13)

To be done on a Core2 v1.3 with the patched firmware before the Mission 2 materials are
written:

1. Whether the images fit embedded in the project, or must be stored as files on the
   board's flash and drawn from there; frame size about 140 px for the bomb and 200 px for
   the explosion.
2. How many frames per second MicroBlocks can draw at those sizes.
3. Realistic `jolt` values when carrying the board carefully and clumsily, to set the
   per-jolt increase and the limits 50 and 100.

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
