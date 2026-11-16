# Mission 1: bonus cards 🃏

Pick any card. Each one works on its own.

---

## 🃏 Card A: Your own answers

**Goal:** the ball gives your own funny answers.

**How:** click the arrow on the **list** block to add more spaces, and type new answers, like `Ask your cat` or `Only on Tuesdays`.

**Tip:** long answers are split over several lines, so they still fit.

---

## 🃏 Card B: A face for every answer

**Goal:** draw a face next to the answer.

**How:** add the **TFT** library (**Add Library** → **Graphics and Displays** → **TFT**). Use **draw circle** for the head and two small filled circles for the eyes. Draw a smile for yes, a frown for no.

**Coach hint:** the screen is 320 wide and 240 high; draw after **show big text**, because it clears the screen.

---

## 🃏 Card C: The secret cheat button

**Goal:** when *you* touch the left circle, the ball always says yes. Your friends won't know!

**How:** make a new **when** script with **left button touched?** that shows `Yes!` in green.

---

## 🃏 Card D: Question counter

**Goal:** the ball counts how many questions it answered.

**How:** add a variable `count`. Set it to 0 in **when started**. Add **change count by 1** in your **when** script. Show it with **join** `Questions: ` and **count**.

**Coach hint:** show the count after the answer, after the wait.
