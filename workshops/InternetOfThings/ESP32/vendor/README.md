# Vendored MicroBlocks libraries

These files are unchanged copies of libraries that ship with MicroBlocks. They are embedded into the generated workshop projects so that children never have to add a library by hand during a session.

| File | Source | Downloaded | SHA-256 |
|---|---|---|---|
| `Tone.ubl` | https://bitbucket.org/john_maloney/smallvm/src/HEAD/Libraries/Tone.ubl | 2026-11-11 | `9cfc896d4daaa4943ba17b90ef77d4a72c34eb248a59e9e69fe268aa4f469403` |
| `ESP Now.ubl` | https://bitbucket.org/john_maloney/smallvm/src/HEAD/Libraries/Network/ESP%20Now.ubl | 2026-11-11 | `a4fa55cd0ba7eb66e5eaf2a544494f5996b198eeeacb6a09eb79dbaa0ea43fcb` |

MicroBlocks is licensed under the Mozilla Public License 2.0 (https://mozilla.org/MPL/2.0/). These files keep that license.

To update: download the files again with the commands in this folder's history (`curl` from the URLs above), run `python3 tools/build.py`, and re-test on a Core2.
