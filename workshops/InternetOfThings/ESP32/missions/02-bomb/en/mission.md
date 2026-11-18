# Mission 2: The Bomb 💣

You are the bomb squad! Carry the bomb to the safe zone without jolting it... or BOOM!

**You need:** a Core2 board, a laptop with MicroBlocks, the project [bomb-start-en.ubp](../starter/bomb-start-en.ubp), and a safe zone on the table (your coach marks it).

**Roles:** the **driver** uses the mouse, the **navigator** reads this page aloud. Swap at every 🔄. **Always carry the board with two hands, and walk.**

## ⭐1 The bomb appears

1. Go to **Variables** and add a variable `playing`. Under **when started**, add **set playing to false** and **show bomb calm** (from **Core2Buttons**).
2. Make a **when** script with **middle button touched?**. In it: **reset timer** (from **Input**), **show danger bar 0**, and **set playing to true**.

**true / false:** take the switch block from **Operators** and put it in the hole of **set**. Click the switch to turn it off: that is false. On is true. Don't type the word `true`: then it is only text, and the game never starts.

**🧪 Try it!** Click ▶. Do you see the bomb? Touch the middle circle: the danger bar appears at the bottom, the game has started.

**🔄 Swap**

## ⭐2 How hard are you moving?

1. Make a second **when** script, this time with the variable **playing** inside the **when** (so it runs during the game). In it: **show big text (jolt)** in white and **wait 30 millisecs**.
2. Click ▶, touch the middle circle, and move the board slowly, then faster.

**🧪 Try it!** What number do you get when you hold it still? When you walk? When you bump it?

**🔄 Swap**

## ⭐3 The danger meter

1. Add variables `danger` and `mood`. In the middle-circle script, also **set danger to 0** and **set mood to 0**.
2. In the **when playing** script, remove the jolt text. First **initialize local j to (jolt)**, so you measure once. Then use **if / else**: if **j > 15**, change danger by **(j − 15) / 2**; else, if **j < 10** and danger > 0, change danger by -1. Tip: when the bomb gets nervous, **stand still** to calm it down.
3. Then an **if** block (click its arrow until it shows **if … else if … else**): **if danger >= 100**: **set playing to false**, **show bomb explode**, **vibrate for 800 ms**, **show big text** `BOOM!` in red. **Else if danger >= 50**: **show bomb nervous**, **beep 880 Hz for 40 ms** and **set mood to 1**. **Else**: only **if mood = 1**, **show bomb calm** and **set mood to 0** (drawing the bomb takes time, so we only draw it when it changes).
4. At the end of the script: **show danger bar (danger)** and **wait 30 millisecs**.

**🧪 Try it!** Walk to the safe zone. Does the bomb get nervous when you bump it?

**🔄 Swap**

## ⭐4 Safe!

1. Change the middle-circle script into an **if playing / else**:
   - **if playing** (the bomb is in the safe zone): **set playing to false**, **initialize local t to (timer / 1000)** (**timer** is in **Input**; read it first, so the safe animation doesn't count), **show bomb safe**, then **show big text (join `SAFE! ` t ` s`)** in green (**join** is in **Data**: click its arrow once to get a third hole);
   - **else** (start a new game): everything the script did before (reset timer, danger 0, mood 0, **show bomb calm**, danger bar 0, **set playing to true**).

**🧪 Try it!** How fast can you bring the bomb to safety without exploding it? (Wait until `BOOM!` or `SAFE!` is shown before you touch the middle circle again.)

**🔄 Swap**

## You did it! 🎉

You built a game with a **sensor** (movement), a **variable that changes over time** (the danger meter), **limits** (50 and 100), images and a **timer**. Try a [bonus card](bonus-cards.md)!

*Bomb and explosion animations: Noto Animated Emoji by Google, CC BY 4.0.*
