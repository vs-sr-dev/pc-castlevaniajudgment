# Session log

## Session 1 — set up, recompiled, to the menus

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
* Nothing in wiikit changed.
