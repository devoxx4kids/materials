# Mission 3: Emoji Messenger 📡

Send emojis from your board to other boards, by radio. No internet, no Wi-Fi router: the boards talk to each other directly.

**You need:** a Core2 board, a laptop with MicroBlocks, the project [emoji-messenger-start-en.ubp](../starter/emoji-messenger-start-en.ubp), and another pair at your table.

**Roles:** the **driver** uses the mouse, the **navigator** reads this page aloud. Swap at every 🔄.

## ⭐1 Hello, radio!

1. In **when started**, change the group number `1` to your **table number**. Only boards with the same number hear each other.
2. Change `Team 1` to your own team name (short, no `|` sign).
3. Click **when started** once.
4. Make a **when** script with **middle button touched?** and add **espNow send pair myName = 1**.
5. Make another **when** script with **espNow pair received?** and add **show big text (espNow last string)** in yellow.

**🧪 Try it!** Both pairs at the table touch the middle circle. Do you see the other team's name?

**🔄 Swap**

## ⭐2 Choose an emoji

The list `emojis` is already in your project: `:-)` `:-D` `;-)` `<3` `:-O` `:-(` `B-)` `:-P`. Turn your head to the left to see the faces!

1. Make a **when** script with **right button touched?**: **change choice by 1**, **if choice > length of emojis** set choice to 1, then **show big text (item choice of emojis)** (**item** and **length of** are in **Data**).
2. Do the same with **left button touched?**: change choice by -1, and if choice < 1 set it to **length of emojis**.
3. In the middle-button script, send **choice** instead of 1: **espNow send pair myName = choice**.

**🧪 Try it!** Scroll with left and right. Does the emoji change?

**🔄 Swap**

## ⭐3 Show what arrives

1. In the **espNow pair received?** script, add **initialize local n to (espNow last number)**.
2. **If n >= 1 and n <= length of emojis**: show **item n of emojis** big in yellow, **beep 660 Hz for 100 ms** and wait 2000 ms. Other numbers are ignored: that keeps your board safe from strange messages.
3. At the end, show your own emoji again: **show big text (item choice of emojis)**.

**🧪 Try it!** Send emojis to each other. Do you hear the beep when one arrives?

**🔄 Swap**

## ⭐4 Shake for a party!

Every board in your group hears every message. That is called a **broadcast**.

1. Make a **when** script with **board shaken?** and add **espNow send pair myName = 0**, **show big text** `Sent!` in green and **wait 500 millisecs** (so one shake sends one message, not dozens). Then show your emoji again: **show big text (item choice of emojis)**.
2. In the received script, add before the other test: **if n = 0**, **repeat 3**: show `PARTY!` in pink, **vibrate for 250 ms**, show `PARTY!` in light blue, wait 100 ms.

**🧪 Try it!** Shake your board. Does the whole table party?

**🔄 Swap**

## You did it! 🎉

You built a radio messenger with **groups**, **lists**, **messages** made of a name and a number, and a **broadcast**. Try a [bonus card](bonus-cards.md)!
