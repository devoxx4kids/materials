# Core2Buttons library

Helper blocks for the M5Stack Core2, used by every mission.

## Tested on hardware

Board: Core2 v1.3 (K010-V13), two boards. Firmware: MicroBlocks `dev` b40b74d with the
Devoxx4Kids patch (`../firmware/`). IDE: MicroBlocks pilot (2.5.15) and the 3.0 preview.
Date: 2026-11-13.

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

### Bomb spike

Tested on board #1 on 2026-11-13 (firmware e4d90571…, bomb-images c303da82…).

| Check | Result | Notes |
|---|---|---|
| B1 pictures | pass | calm, nervous, explode and safe recognisable, colours correct, centred |
| B2 explode animation time | pass | not timed with a script; the tester found it smooth |
| B3 careful walk | pass | measured jolt: still 5, careful walk up to 25 |
| B4 clumsy walk | pass | normal walk 50–60, bumps and jumps 80–100: explodes |
| B5 without bomb-images.bin | pass | board #2 erased, firmware only (2026-11-16): no pictures, no error; danger bar, beeps, explosion sound, buzz and texts all work |

Measured `jolt` values (Jolt meter, board held in two hands): still 5 · careful walk 25 ·
normal walk 50–60 · clumsy walk or small jumps 80–100.

Final constants in `src/projects/bomb-done.ubp.tmpl`: jolt ignored below 15, increase
`(jolt − 15) / 2`, the meter drains by 1 per pass only while the board is held still
(jolt below 10), nervous at 50, explode at 100. The first setting (ignore below 15,
increase `jolt / 5`, drain whenever jolt ≤ 15) was far too insensitive.

The explosion is also audible: a 50 Hz boom for 200 ms, then a 30–90 Hz rumble of 50 ms
after each explosion frame (tuned with the tester: deeper sounds better).
