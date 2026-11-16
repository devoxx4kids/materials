# Mission 2: bonus cards 🃏

---

## 🃏 Card A: Bomb squad training (reaction duel)

**Goal:** who reacts fastest? The board stays on the table.

**How:** a **when** script with **right button touched?**: show `Get ready...`, wait a **random** 2000 to 5000 ms, show `GO!` and beep. Then **repeat until** someone touches: left circle → `Left wins!`, right circle → `Right wins!`. Touching before GO! → `Too early!`.

---

## 🃏 Card B: Expert mode

**Goal:** a more sensitive bomb.

**How:** change the limits: nervous at **30**, explode at **60**.

---

## 🃏 Card C: Record

**Goal:** remember the fastest safe time.

**How:** a variable `best`, set to 99999 in **when started**. When the bomb is safe, if the time is smaller than `best`, set `best` to it and show `NEW RECORD!`.

---

## 🃏 Card D: The long route

**Goal:** a route around the room; pairs take turns.

**How:** no new blocks: agree with your coach on a longer route. Who keeps the danger bar the lowest?

**Coach hint:** keep the route clear of chairs and bags; always walk.
