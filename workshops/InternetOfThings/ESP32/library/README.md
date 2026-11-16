# Core2Buttons library

Helper blocks for the M5Stack Core2, used by every mission. They hide the board details children don't need: the three red circles under the screen are touch zones rather than real buttons, and the vibration motor sits behind the power chip.

## Blocks

| Block (English label) | Type | What it does |
|---|---|---|
| `left button touched?` / `middle button touched?` / `right button touched?` | reporter | True **once** when the circle is touched. Use it in a `when` hat block. |
| `board shaken?` | reporter | True while the board is shaken firmly (acceleration above 140; needs the workshop firmware on the Core2 v1.3). |
| `vibrate for _ ms` | command | Buzzes the vibration motor. |
| `beep _ Hz for _ ms` | command | Plays a tone on the speaker. |
| `show big text _ colour _` | command | Clears the screen and writes the text in the middle, as big as possible; long texts are split over lines. |
| `show bomb _` (calm / nervous / explode / safe) | command | Draws the bomb pictures from files on the board; explode also rumbles on the speaker. |
| `jolt` | reporter | How hard the board moves right now (0 = still). |
| `show danger bar _` | command | A green → orange → red bar along the bottom of the screen. |

The library uses the MicroBlocks **Tone** library, which every workshop project already contains.

## Files

- `Core2Buttons-en.ubl`, `Core2Buttons-fr.ubl`, `Core2Buttons-nl.ubl`: generated, one per language. Coaches normally don't need them, because every starter project already contains the library.
- Source: `../src/library/Core2Buttons.ubl.tmpl`. Labels and comments: `../i18n/*.json`.

## Translating

1. Add or change the `blk.*` and `comment.*` values in `../i18n/<lang>.json`. Keep every `_` (an input slot) in a label; the build refuses labels with a different number of slots than English.
2. Run `python3 tools/build.py` from the workshop folder.
3. Open a starter project in MicroBlocks with that language selected and check the labels.

## Built-in block labels (English)

The exact English labels of the MicroBlocks blocks used in the mission pages, as defined in MicroBlocks 3.0.0 (`chromeApp/webapp/engine/mb-specs.js`, `dev` f4767a3). The French and Dutch pages use MicroBlocks' own translations of these labels.

| Block | Label | Palette |
|---|---|---|
| when started | `when started` | Control |
| when (condition) | `when _` | Control |
| wait | `wait _ millisecs` | Control |
| if / else if / else | `if _` (click the arrow to add `else if` and `else`) | Control |
| repeat, repeat until, forever | `repeat _`, `repeat until _`, `forever` | Control |
| random | `random _ to _` | Operators |
| compare | `_ = _`, `_ ≠ _`, `_ < _`, `_ > _`, `_ >= _`, `_ <= _` | Operators |
| logic | `_ and _`, `_ or _`, `not _` | Operators |
| list | `list` (click the arrow for more items) | Data |
| item of, length of | `item _ of _`, `length of _` | Data |
| join | `join _ _` | Data |
| set, change, local | `set _ to _`, `change _ by _`, `initialize local _ to _` | Variables |
| timer | `reset timer`, `timer` | Input |
| new variable | button `Add a variable` | Variables |
| add a library | button `Add Library` | Libraries |

## Tested on hardware

Board: Core2 v1.3 (K010-V13), two boards. Firmware: MicroBlocks `dev` b40b74d (VM 424) with the Devoxx4Kids patch (`../firmware/`). IDE: MicroBlocks pilot (2.5.15) and the 3.0 preview. Date: 2026-11-13.

| Check | What was tested | Result | Notes |
|---|---|---|---|
| H1 | Install, connection, screen | pass | Stable VM 411 fails on the v1.3 (no reply); pilot VM 424 and the patched build work. The firmware menu has no Core2 entry: advanced mode → install ESP firmware from microblocks.fun → m5core2_1.0, or esptool with `../firmware/`. On macOS, power-cycle without USB after flashing. Green LED is off by design (MicroBlocks turns it off) |
| H2 | Circles react, other circles ignored | pass | screen tap above the circles: no answer (2026-11-16) |
| H3 | One event per touch (hold) | pass | finger held 5 s on the middle circle: one answer, no new one until the finger is lifted and touches again (2026-11-16) |
| H4 | Beep | pass | Tone library works on the pilot firmware |
| H5 | Shake and vibration | pass (patched) | Stock firmware: acceleration 0 (BMI270 not read), no motor. Patched: acceleration 99 at rest; motor on/off via `[tft:setVibration]` |
| H6 | ESP Now between two boards | pass | both directions, emoji, name, beep; party with buzz (250 ms; 100 ms was not felt) |
| H7 | Hot Potato | pass | replaced by the Bomb (see below) |
| H8 | Long text and accents | pass (patched) | a 39-character answer was unreadable at size 1 → `show big text` now wraps over lines at the largest size; accents looked like flat bars in the stock 5 × 7 font → redrawn in the firmware patch (2026-11-16): ê, é, è, à, ù, ç correct |
| H9 | FR and NL labels | pass | MicroBlocks 3.0 pilot (IDE 3.0.0) with VM 424: Core2Buttons and built-in blocks translated; global variable names were English → now translated too (réponses, enJeu, occupé, antwoorden…); accented names work (2026-11-16) |

**Decision (plan Task 7, Step 8):** MicroBlocks + firmware patch.

**Re-check after the rebase on VM 425 (2026-11-16, board #2):** patch applied unchanged on MicroBlocks `dev` f4767a3 (IDE 3.0.0, VM 425). The IDE no longer shows the "not current (v424 vs v425)" popup; board name M5StackCore2; Bomb (French) with pictures, shake, rumble, buzz and confetti, and the accent test all pass.

### Bomb spike

Tested on board #1 on 2026-11-13 (firmware e4d90571…, bomb-images c303da82…).

| Check | Result | Notes |
|---|---|---|
| B1 pictures | pass | calm, nervous, explode and safe recognisable, colours correct, centred |
| B2 explode animation time | pass | not timed with a script; the tester found it smooth |
| B3 careful walk | pass | measured jolt: still 5, careful walk up to 25 |
| B4 clumsy walk | pass | normal walk 50–60, bumps and jumps 80–100: explodes |
| B5 without bomb-images.bin | pass | board #2 erased, firmware only (2026-11-16): no pictures, no error; danger bar, beeps, explosion sound, buzz and texts all work |

Measured `jolt` values (Jolt meter, board held in two hands): still 5 · careful walk 25 · normal walk 50–60 · clumsy walk or small jumps 80–100.

Final constants in `src/projects/bomb-done.ubp.tmpl`: jolt ignored below 15, increase `(jolt − 15) / 2`, the meter drains by 1 per pass only while the board is held still (jolt below 10), nervous at 50, explode at 100. The first setting (ignore below 15, increase `jolt / 5`, drain whenever jolt ≤ 15) was far too insensitive.

The explosion is also audible: a 50 Hz boom for 200 ms, then a 30–90 Hz rumble of 50 ms after each explosion frame (tuned with the tester: deeper sounds better).
