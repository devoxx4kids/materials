# Vendored MicroBlocks libraries

These files are unchanged copies of libraries that ship with MicroBlocks. They are embedded into the generated workshop projects so that children never have to add a library by hand during a session.

| File | Source | Downloaded | SHA-256 |
|---|---|---|---|
| `Tone.ubl` | https://codeberg.org/MicroBlocks/smallvm/raw/commit/f4767a3f0db6654f84ce20c4095cb3f9aabbc32e/Libraries/Tone.ubl | 2026-11-11 (identical at f4767a3) | `9cfc896d4daaa4943ba17b90ef77d4a72c34eb248a59e9e69fe268aa4f469403` |
| `ESP Now.ubl` | https://codeberg.org/MicroBlocks/smallvm/raw/commit/f4767a3f0db6654f84ce20c4095cb3f9aabbc32e/Libraries/Network/ESP%20Now.ubl | 2026-11-11 (identical at f4767a3) | `a4fa55cd0ba7eb66e5eaf2a544494f5996b198eeeacb6a09eb79dbaa0ea43fcb` |

MicroBlocks is licensed under the Mozilla Public License 2.0 (https://mozilla.org/MPL/2.0/). These files keep that license.

To update, from the workshop folder (replace the commit in the URLs with the one the firmware is built on, `BASE` in `../firmware/build.sh`):

    curl -fsSL -o vendor/Tone.ubl "https://codeberg.org/MicroBlocks/smallvm/raw/commit/f4767a3f0db6654f84ce20c4095cb3f9aabbc32e/Libraries/Tone.ubl"
    curl -fsSL -o "vendor/ESP Now.ubl" "https://codeberg.org/MicroBlocks/smallvm/raw/commit/f4767a3f0db6654f84ce20c4095cb3f9aabbc32e/Libraries/Network/ESP%20Now.ubl"
    shasum -a 256 vendor/*.ubl

Update the table above with the new SHA-256 values, run `python3 tools/build.py`, and re-test on a Core2.

## Where to buy the board

The workshop needs the **M5Stack Core2 v1.3** (part number **K010-V13**); do not buy the Core2 v1.1 (K010-V11). Search for the part number at one of these distributors:

- Mouser: https://www.mouser.be/
- RS Components: https://benl.rs-online.com/web/c/?searchTerm=esp32
- DigiKey: https://www.digikey.be/en/
