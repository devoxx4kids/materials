# Changelog

All notable changes to the ESP32 workshop. One version entry per day.

## [0.4.0] - 2026-11-18

### Fixed
- `show bomb calm` clears the screen first, so the old BOOM!/SAFE! text no longer stays around the bomb in a new round.
- Mission 2 pages (EN/FR/NL) say where the true/false switch is (Operators): a typed `true` is only text and the game never started.
- Coach setup names the tested MicroBlocks version (3.0) and says to click Cancel on the board-update prompt, which would replace the workshop firmware; two new troubleshooting rows.
- Bomb solution: the SAFE time is read before the safe animation, SAFE waits until a nervous picture is fully drawn (new `drawing` variable), and "Touch middle to start" shows again after BOOM! and SAFE!.
- Mission 2 pages read the time first too, and the English `SAFE! ` text has its space before the time.
- Mission 3 pages: the party buzz is 250 ms (100 ms was not felt), and the shake script shows `Sent!` and waits 500 ms, so one shake sends one message.
- Bonus cards: coach hint for "Too early!" in the reaction duel; the `group` variable of Team channels starts at the table number.
- Coach pages: which capital accents display and which show a rectangle; the 21 empty picture files left without `bomb-images.bin`; the safe zone is marked next to each table.

### Changed
- Kids' pages name the palette of list, item, length, join, random, reset timer and timer, and say that join needs one arrow click for a third hole.
- `build.py` names the file when a translation file is not valid JSON, and `--check` also reports unused translation keys and stray .ubp/.ubl files.
- New test: every script and function stays under 1000 bytes of source, so each compiles within MicroBlocks' chunk limit.
- `library/README.md` explains that each circle needs a single `when` script, and its test header names the VM 425 build; `vendor/README.md` points to Codeberg at f4767a3 with the curl and shasum commands.

## [0.3.0] - 2026-11-16

### Changed
- Bomb check B5 recorded: the mission runs without the bomb pictures and without errors.
- `show big text` splits long texts over several lines at the largest size that fits, instead of shrinking them (a 39-character answer was unreadable at size 1).
- Firmware patch redraws the lowercase accented letters of the screen font, so é, è, ê, à, ù, ç are readable at text size 4.
- Global variable names in the projects are translated (FR: réponses, danger, enJeu…; NL: antwoorden, gevaar, speelt…), so no English shows in the French and Dutch projects.
- Firmware patch rebased on MicroBlocks 3.0 (VM 425, commit f4767a3): the IDE no longer asks to update the board.
- The design documents (specs and implementation plans) moved into `design/` inside the workshop folder; the docs checker does not link-check them.

### Fixed
- `show big text` no longer cuts off a single long word (e.g. Gefeliciteerd!): it also checks the width before choosing a size.

### Added
- English entry page, coach guides (setup, running a session, hardware) and library reference.
- Mission 1 (Magic Shake Ball) kids' page and bonus cards (English), and the table of MicroBlocks 3.0 block labels in library/README.md.
- Mission 2 (The Bomb) kids' page and bonus cards (English).
- Mission 3 (Emoji Messenger) kids' page and bonus cards (English).
- French translation of all pages.
- Dutch translation of all pages.

## [0.2.0] - 2026-11-13

### Added
- Patched MicroBlocks firmware for the Core2 v1.3 (BMI270 motion sensor, vibration primitive) in `firmware/`; `vibrate` now drives the real motor.
- Bomb images (Noto Animated Emoji, CC BY 4.0) converted to Core2 frames by tools/convert_images.py.
- Bomb blocks in Core2Buttons: show bomb, jolt, show danger bar (EN, FR, NL).
- firmware/build.sh rebuilds the patched firmware and the bomb image file system (bomb-images.bin).

### Fixed
- `vibrate` no longer stops the program with an I2C error on the Core2; it skips the motor when the power chip cannot be reached.
- Emoji Messenger party buzz lengthened to 250 ms so it can be felt.
- Bomb pictures: the colour palette is now a file on the board (a function that large could not be sent to the board); a tap during BOOM or SAFE no longer starts a broken round; a picture file left open by a stopped program is closed before the next one.

### Changed
- Mission 2 is now the Bomb (carry it to the safe zone without jolting it); Hot Potato removed, its duel becomes a bonus card.
- Bomb tuned on hardware (jolt counts from 15, the meter drains only while the board is held still) and the explosion now rumbles on the speaker.

## [0.1.0] - 2026-11-11

### Added
- Build tool that generates the MicroBlocks library and projects for English, French and Dutch.
- Documentation checker: language parity, local links, no AsciiDoc, mission pages present.
- `Core2Buttons` helper library (touch circles, shake, vibrate, beep, big text) in EN, FR and NL.
- Pinned copies of the MicroBlocks Tone and ESP Now libraries.
- Mission 1 (Magic Shake Ball) starter and solution projects.
- Mission 2 (Hot Potato and Duel) starter and solution projects.
- Mission 3 (Emoji Messenger) starter and solution projects using ESP Now.
- Every beep and buzz also flashes a yellow frame on the screen, so children see it even when the speaker or motor stays silent.
