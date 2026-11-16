# Mission 3: bonus cards 🃏

---

## 🃏 Card A: Secret code

**Goal:** send a secret word that only your partners can read.

**How:** use the number as a key. Before sending, turn every letter of your word into the letter 3 places later (A → D, B → E). The receivers turn it back. Use **join** and the letters of a word one by one.

**Coach hint:** this is the Caesar cipher. Let them do it on paper first.

---

## 🃏 Card B: Team channels

**Goal:** switch between your table's group and a shared group for the whole room.

**How:** the right circle already goes round all the emojis, so the left circle is free. Change your **left button touched?** script: add a variable `group`; if `group` is your table number, set it to `99`, otherwise set it back to your table number. Then run **espNow set group** with `group` and show it with **join** `Group ` and **group**.

**Coach hint:** agree on one shared extra group number for the whole room.

---

## 🃏 Card C: Fortune delivery 🎱

**Goal:** send a Magic Ball answer to another table.

**How:** add the answers list from Mission 1. Pick a **random** answer and send it as the text of the pair (with number 9, for example). The receiving board shows the text when the number is 9.

**Coach hint:** the receiving pair must add a test for 9 before the emoji test.
