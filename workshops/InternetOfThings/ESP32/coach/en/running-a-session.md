# Running a 45-minute session

## Before the children arrive

- Every laptop has MicroBlocks open, a board connected, and the **starter project** of today's mission open in the right language.
- The solution project of the mission is on your own laptop.
- For Mission 2, mark a start point and a safe zone (a sheet of paper) about 3 metres apart, next to each table. Children carry the board with two hands, walking.

## Timing

| Minutes | What happens | Your job |
|---|---|---|
| 0–5 | Welcome, show the finished project on your board | Keep it short and fun; let them guess how it works |
| 5–30 | The pair follows `mission.md`, steps ⭐1 to ⭐4 | Walk around; ask questions instead of grabbing the mouse |
| 30–40 | Bonus cards, chosen by the pair | Hand out cards; praise their own ideas |
| 40–45 | Show and tell: pairs show their board to the next table | Ask every pair what they changed |

A pair that is slower is fine: finishing ⭐3 is already a working Magic Ball / game.

## Pairs

- **Driver**: holds the mouse and builds the blocks.
- **Navigator**: reads the mission page aloud and checks every step.
- They swap at every ⭐. The mission page reminds them with 🔄.

## Radio groups (Mission 3)

Each table uses its own group number, from 1 upward, so 20 boards in the same room don't all receive each other's messages. Write the number on the table. Pairs set it in the first block of their starter project. For the "send to another table" bonus card, two tables agree on one shared group.

## Common problems

| Symptom | Fix |
|---|---|
| Board not found | Replug; use a data USB-C cable; reload the page or restart the app |
| Screen black | Press the power button on the left side; charge the board |
| Buttons don't react | Open the starter project, so the helper library is loaded |
| Messages don't arrive | Both boards must use the same group number |
| No sound | Check that the beep block is used; use the vibrate block instead |
| **board shaken?** is never true, no buzz | An update replaced the workshop firmware: install it again (see [setup](setup.md)) |
| Mission 2: the danger bar appears, but nothing else happens | `playing` was set with the typed word `true`: use the switch block from **Operators** |
| Bomb pictures missing | Install the workshop firmware again with both files (see [setup](setup.md)) |

When a pair is stuck for more than two minutes, open the solution project on your laptop and compare their script with it, one block at a time.

## Known limits

- Accents: lowercase accented letters (é, è, ê, à, ç, ù…) display correctly with the workshop firmware. Capitals: É, Ç, Ä, Ö and Ü display; À, È, Ê, Î, Ô, Ù, Û, œ and Œ are not in the screen font and show as a filled rectangle, so write those in lowercase.
- Radio: tested with two boards. ESP Now does not guarantee delivery, so in a full room an occasional message can be lost; just send it again.
- Without `firmware/bomb-images.bin` the Bomb still works, but shows no pictures, and the board then holds 21 empty picture files; installing the firmware again with both files replaces them (see [setup](setup.md)).
