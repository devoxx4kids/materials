# Changelog

All notable changes to the ESP32 workshop. One version entry per day.

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
