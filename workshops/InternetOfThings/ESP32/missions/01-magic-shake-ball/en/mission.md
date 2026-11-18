# Mission 1: Magic Shake Ball 🎱

Turn your board into a magic ball that answers every question. Ask it something, shake it, and it decides for you!

**You need:** a Core2 board, a laptop with MicroBlocks, and the project [magic-ball-start-en.ubp](../starter/magic-ball-start-en.ubp) (your coach has opened it).

**Roles:** the **driver** uses the mouse, the **navigator** reads this page aloud. Swap at every 🔄.

Our special blocks are in the **Core2Buttons** library, in the list of blocks on the left.

## ⭐1 The ball speaks

1. Go to **Control** and drag a **when** block onto the empty space.
2. From **Core2Buttons**, drag **middle button touched?** into the hole of the **when** block.
3. From **Core2Buttons**, drag **show big text _ colour _** under it.
4. Click in the text field and type `Ask me a question!`. Pick a colour you like.

**🧪 Try it!** Touch the **middle red circle** under the screen. Does the text appear?

**🔄 Swap**

## ⭐2 A random answer

A magic ball needs answers. We keep them in a **list**.

1. Go to **Variables**, click **Add a variable** and name it `answers`.
2. Under **when started** (it is already there), add **set answers to _**.
3. Put a **list** block (from **Data**) in the hole. Click the arrow on the list until it has 4 spaces and type: `Yes!`, `No way!`, `Maybe...`, `Ask again`.
4. Click the **when started** script once, so the list is made.
5. In your **when** script, replace the text `Ask me a question!` with **item _ of _** (from **Data**): in the first hole put **random 1 to _** (from **Operators**), and in the last hole of **random** put **length of answers** (from **Data**). In the second hole of **item** put **answers**.

**🧪 Try it!** Touch the middle circle a few times. Do you get different answers?

**🔄 Swap**

## ⭐3 Shake it!

A real magic ball is shaken.

1. From **Operators**, take an **_ or _** block.
2. Move **middle button touched?** into its left side, and put **board shaken?** (from **Core2Buttons**) into its right side.
3. Put the **or** block into the hole of your **when** block.

**🧪 Try it!** Hold the board in two hands and shake it firmly. Does an answer appear?

**🔄 Swap**

## ⭐4 Colours, beeps and buzzes

1. From **Variables**, put **initialize local n to** at the top of the **when** script and set it to **random 1 to length of answers**. Now use **item n of answers** to show the answer.
2. Add an **if** block (Control) and click its arrow until it shows **if … else if … else**. Then: **if n = 1** show the answer in green, **else if n = 2** in red, **else** in yellow.
3. Under the **if**, add **beep 880 Hz for 150 ms** and **vibrate for 200 ms**.
4. Add **wait 1500 millisecs** and then **show big text** `Ask me a question!` in white.

**🧪 Try it!** Ask a question out loud, then shake. Does the board beep, buzz and show a coloured answer?

**🔄 Swap**

## You did it! 🎉

You built a magic ball with **events** (when), a **list**, **random** numbers, a **sensor** (shaking) and **outputs** (screen, sound, vibration). Pick a [bonus card](bonus-cards.md) to make it even better!
