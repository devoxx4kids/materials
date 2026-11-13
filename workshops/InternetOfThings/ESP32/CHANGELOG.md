# Changelog

All notable changes to the ESP32 workshop. One version entry per day.

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
- `vibrate` no longer stops the program with an I2C error on the Core2; it skips the motor when the power chip cannot be reached.
- Patched MicroBlocks firmware for the Core2 v1.3 (BMI270 motion sensor, vibration primitive) in `firmware/`; `vibrate` now drives the real motor.
- Emoji Messenger party buzz lengthened to 250 ms so it can be felt.
