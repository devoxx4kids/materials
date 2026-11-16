# ESP32 Workshop: Magic Shake Ball 🎱

A Devoxx4Kids workshop for children aged 10 to 14. Working in pairs, they program an **M5Stack Core2** (an ESP32 board with a touch screen, motion sensor, speaker and vibration motor) with **MicroBlocks**, a free block language that looks like Scratch and runs the program on the board straight away.

Every mission takes **45 minutes** and works on its own, so you can run one, two or all three.

| Mission | What the pair builds | 🇬🇧 | 🇫🇷 | 🇳🇱 |
|---|---|---|---|---|
| 1. Magic Shake Ball | Ask a question, shake the board, get a random answer | [EN](missions/01-magic-shake-ball/en/mission.md) | [FR](missions/01-magic-shake-ball/fr/mission.md) | [NL](missions/01-magic-shake-ball/nl/mission.md) |
| 2. The Bomb | Carry the bomb to the safe zone without jolting it, or BOOM | [EN](missions/02-bomb/en/mission.md) | [FR](missions/02-bomb/fr/mission.md) | [NL](missions/02-bomb/nl/mission.md) |
| 3. Emoji Messenger | Send emojis to other tables by radio, no Wi-Fi needed | [EN](missions/03-emoji-messenger/en/mission.md) | [FR](missions/03-emoji-messenger/fr/mission.md) | [NL](missions/03-emoji-messenger/nl/mission.md) |

## For coaches

Read these before the event:

| | 🇬🇧 | 🇫🇷 | 🇳🇱 |
|---|---|---|---|
| Preparing laptops and boards | [EN](coach/en/setup.md) | [FR](coach/fr/setup.md) | [NL](coach/nl/setup.md) |
| Running a 45-minute session | [EN](coach/en/running-a-session.md) | [FR](coach/fr/running-a-session.md) | [NL](coach/nl/running-a-session.md) |
| The Core2 hardware | [EN](coach/en/hardware.md) | [FR](coach/fr/hardware.md) | [NL](coach/nl/hardware.md) |

## What you need

- One M5Stack Core2 and one laptop per pair, plus two spare boards.
- One USB-C cable **that carries data** per board.
- Chrome or Edge, or the MicroBlocks desktop app (https://microblocks.fun/download).

## For maintainers

The MicroBlocks files are generated. Do not edit `library/*.ubl` or the `.ubp` files in `missions/*/starter` and `missions/*/solution` by hand.

| Change | Edit | Then run |
|---|---|---|
| A block label or an on-screen text | `i18n/en.json`, `fr.json`, `nl.json` | `python3 tools/build.py` |
| Library behaviour | `src/library/Core2Buttons.ubl.tmpl` | `python3 tools/build.py` |
| A mission project | `src/projects/*.ubp.tmpl` | `python3 tools/build.py` |
| Bomb pictures | `src/images/*.gif`, frame lists in `tools/convert_images.py` | `python3 tools/convert_images.py`, then `firmware/build.sh` |
| Firmware patch | `firmware/microblocks-core2-v1.3.patch` | `firmware/build.sh` |
| Documentation | the `.md` files | `python3 tools/check_docs.py` |

Run the tests with `python3 -m pytest tools/tests -q` (needs `pip install -r tools/requirements-dev.txt`). More about the helper blocks: [library/README.md](library/README.md). Vendored MicroBlocks libraries: [vendor/README.md](vendor/README.md). Firmware: [firmware/README.md](firmware/README.md). History: [CHANGELOG.md](CHANGELOG.md).

## Credits

Bomb and explosion animations: Noto Animated Emoji by Google, CC BY 4.0 (https://googlefonts.github.io/noto-emoji-animation/).
