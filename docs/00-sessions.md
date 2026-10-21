# Session log

## Session 1 — set up, recompiled, played

Goal: the port set up on wiikit, the executable named and recompiled, and
as far as it would go.

Results:

* **The port set up** on wiikit (submodule, pinned at d9d14c0, the other
  ports' commit). The disc (RVZ) extracted by `wiikit.disc` in 27 s.
* **The executable** (`03-executable.md`): RDGE, stripped, the RVL SDK of
  2007-08, NW4R, DWC.
* **Names by kin.** Arc Rise Fantasia has the same KPAD, WPAD and PAD
  builds, and its DOL is named. `tools/kinmatch.py` carries its names
  over by code hash, then by place: 1 484 of 1 573. Every runtime hook
  this SDK has resolves, seven of them by hand.
* **Recompiled at the first try**: 11 543 units, 336 switch tables (4 not
  resolved), no bad target. Built in 40 s.
* **Booted at the first try**, on wiikit as it was, with only the port's
  layer (`tools/cvj.cpp`: `KPADStatus` of 0x84, the Classic Controller):
  - the strap screen, the logos, the opening movie, the title, at 30
    frames a second, picture and sound right (the user, by eye and ear);
  - scripted presses of the Classic (`WIIKIT_PAD`): past the title, the
    Wii system memory checked, the save file created, the user data and
    the name entry.
* **Played by the user**: Simon against Alucard, won. Sound right but for a
  click at stage loads.
* **Fog** (wiikit). The game fogs its stages (GX fog, linear and
  exponential); wiikit drew none. The renderer now draws GX fog, every
  type, perspective and orthographic, with the range adjustment, after
  Dolphin's software renderer. Checked by two scripted runs to the same
  fight, fog on and off: the distant ruins sink into the night's blue, the
  fighters and the HUD unchanged.
* **The save** (wiikit). The game asked to create its save file at every
  boot. It tells a file from a directory as the SDK's `NANDGetType` does,
  by reading the path as a directory: on a file IOS answers "invalid"
  (-101), wiikit answered "no such file" (-106). Now the profile made in
  one run is there in the next, and scripted runs reach a fight by
  themselves (Story: Simon against Aeon).
* **"To play this game with a Wii Remote, you must have a Nunchuk or
  Classic Controller plug attached"**, after the title, at every boot. Not
  a fault: a watch on the game's controller structures (`8036FB20`, 0x3CC
  each) shows channel 1 as a Classic (type 3, from `800FBC48`'s mapping of
  KPAD's `dev_type`) from the first second to the end, the screen
  included. A reminder the game shows: a longplay of the console game
  (World of Longplays) shows it too, as the user saw.
