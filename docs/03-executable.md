# The executable

## The disc

RDGEA4, the North American release, as RVZ. `wiikit.disc` extracts its
DATA partition in 27 s: 4 695 files, 1.8 GB.

- NW4R formats throughout: `brres`, `brtex`/`brplt` (textures and
  palettes kept apart), `breff`/`breft`, `brsca`, `brsar`, and 2 140
  `brstm` streams (voices, both languages).
- The game's own: `fpk` packs (170), `dah` (187), `seq` (309, the story's
  and the effects' scripts), `mot` (102), `col` (117), `arc`.
- Three THP movies (the opening is one).
- The developer's leftovers: `files/makefile` and 172 `fpkbat/*.bat`
  (paths under `P:/ev0718/dracula/`; "dracula" was the project's name),
  and `files/test/init.txt`, a debug start-up file: the start mode (`MENU`,
  `GAME`, `TEST`), up to four characters (type, colour, life, a mode of
  `U` undying, `E` endless EX gauge, `G` unguardable, sub-weapon, CPU or
  player, team), the stage and area, rounds, round time, CPU level and
  volumes. The retail DOL holds no "init.txt" string, so it probably does
  not read it; whether its parser survives is a lead for scripted tests.

## The DOL

Stripped. Entry `80006124`; text `80004000`-`800064E0` and
`80016300`-`802D9D40` (2.9 MB, 726 000 instructions); BSS `80331E80`
(1.1 MB); small data after it, at `8043D720`.

`__init_registers` (`8000630C`) sets r13 = `80445720` and r2 =
`80447A60`; `tools/look.py` uses them.

### The SDK

RVL SDK `0x4199_60831`, the builds of late 2007 and early 2008:

| Library | Build |
|---|---|
| AI, AX, DSP, DVD, EXI, KPAD, SC, SI, VI, THP | Aug 8 2007 |
| PAD | Oct 3 2007 |
| GX, NAND, WPAD | Dec 11 2007 |
| OS | Jan 30 2008 |
| NWC24, SO, SOCKET, NCD | Dec 10 2007 |
| MP | Mar 13 2008 |
| DWC (Nintendo Wi-Fi Connection) | May 9 2008 |
| REX-PPC (RevoEX-2.1plus), NHTTP, SSL | 2007-08 |

NW4R for the graphics, the effects and the sound (asserts in `g_camnw.c`,
`eft_*.c`, `glib_anim*.cpp`). The online play (DWC) is gone with
Nintendo's servers; the game only probes `/dev/net/kd`.

### The names

1 573 names (`tools/names.py` -> `build/names.tsv`):

- **1 484 by kin** (`tools/kinmatch.py`). Arc Rise Fantasia (2008) has
  the very builds of KPAD, WPAD and PAD this game has, and its named DOL is
  at hand. A function here whose words hash as one there (Dolphin's
  checksum, immediates and branch targets masked), of the same size, takes
  its name; then, by place, a name between two such matches moved by the
  same distance, where a function of the same size and hash is.
- 80 by signature (Dolphin's `totaldb.dsy`, Victorious's ELF), 2 by debug
  string.
- 7 by hand (`tools/names-manual.tsv`): the WPAD thunks after `WPADInit`
  (here one more `li r3,1; blr` before them and one more thunk among
  them than in Arc Rise Fantasia), and KPAD's two parameter setters.

Every runtime hook this SDK has resolves. The others (`KPADInitEx`,
`KPADReadEx`, the 2009 SDK's KPAD/WPAD functions, `kpad_wpad_status`,
`WPADGetLatestIndexInBuf`) are not in this executable: the SDK lacks them,
or the linker dropped them unused.

## The input

One function reads every controller each frame (`800F972C`):

- The GameCube controllers first: `801BDE00` (`PADRead`, by its use) into
  `80370E90`, then `PADClampCircle`.
- Then the four Remotes: `KPADRead(chan, 803710D0 + chan * 0x840, 16)`.
  `KPADStatus` is **0x84** bytes, the 2007 SDK's. A read of zero samples
  resets KPAD and reads again.
- The Classic Controller is read from KPAD's status (its `ex_status`), not
  from WPAD's raw samples as in Arc Rise Fantasia.

The game plays with the Remote alone, the Remote and Nunchuk, the Classic
Controller or the GameCube controller. The port takes the Classic.
