# pc-castlevaniajudgment

Toward a native PC port of **Castlevania Judgment** (Wii, Konami, 2008),
the series' one fighting game, with characters designed by Takeshi Obata.
It stayed a Wii exclusive: no re-release, no remaster, no digital release.
The goal is the game running natively on PC, played with a gamepad as the
Classic Controller.

The route is static recompilation: the game's own PowerPC code, translated
to C++ and built for the PC, running on a replacement for the Wii's
hardware and system software. Nothing is emulated at the instruction
level, and nothing of the game is rewritten.

This repository documents the port and holds its own tools and layer. It is
built on **[wiikit](https://github.com/vs-sr-dev/wiikit)**, the
game-agnostic Wii toolkit, taken here as a submodule at `wiikit/`. Where
this game needs something every Wii game would need, it goes into wiikit,
not here.

## Where it stands

After one session **the game plays**, recompiled at the first try; wiikit
gained GX fog and a NAND answer the game's save check needed:

- The strap screen, the logos, the opening movie (THP), the title.
- The save file created on the NAND, the user data and name screens.
- Picture and sound right, at 30 frames a second; the stages' fog.
- Fights: Simon against Alucard, played by the user; scripted runs to a
  Story fight.
- A gamepad (or the keyboard) as the Classic Controller.

See [docs/00-sessions.md](docs/00-sessions.md) and the plan in
[docs/07-next-session.md](docs/07-next-session.md).

## BYOA — Bring Your Own Assets

This repository contains **documentation and tools only**. No game data, no
executables, no assets. You need your own original disc. The work is done on
the North American release, RDGE; the addresses in `tools/` and `docs/` are
that executable's.

## Layout

    docs/     the executable, the plan, the session log
    tools/    Castlevania Judgment-specific tools, the port's layer (cvj.cpp)
    wiikit/   game-agnostic Wii toolkit (submodule: github.com/vs-sr-dev/wiikit)
    build/    (not in git) the disc, everything derived from it, the build

## Building

As for the other wiikit ports: Python 3.8+, CMake, Ninja, clang (MSYS2) and
SDL3; OpenGL 4.5 to run. From the root:

```sh
python -m wiikit.disc GAME.rvz --extract build/extract
python tools/sigmatch.py build/extract/sys/main.dol --dsy <Dolphin>/Sys/totaldb.dsy \
    --out build/sig_guess.tsv
python tools/kinmatch.py build/extract/sys/main.dol \
    --kin <arc rise fantasia>/build/extract/sys/main.dol <arc rise fantasia>/build/names.tsv \
    --out build/kin_guess.tsv
python tools/names.py build/extract/sys/main.dol          # -> build/names.tsv
python -m wiikit.recomp build/extract/sys/main.dol --out build/recomp \
    --symbols build/names.tsv --hooks tools/cvj-hooks.txt
cmake -S build/recomp -B build/recomp-build -G Ninja -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE=-O1 -DWIIKIT_EXTRA=$PWD/tools/cvj.cmake
ninja -C build/recomp-build
cd build/run1 && ../recomp-build/wiiboot ../extract --symbols ../recomp/symbols.tsv \
    --nand ../nand --fonts ../fonts
```

`build/fonts` holds the boot ROM's fonts and `dsp_coef.bin` (Dolphin's
`Sys/GC` has free ones). The names come from Dolphin's `totaldb.dsy`, from
a kin (Arc Rise Fantasia's named executable, whose KPAD, WPAD and PAD are
the very same builds; `tools/kinmatch.py`), and from
`tools/names-manual.tsv`, each with its evidence. `tools/look.py` is
`wiikit.ppc` on the stripped DOL.

## Documentation

    00-sessions.md            progress log
    03-executable.md          the stripped DOL, its SDK, its names, its input
    07-next-session.md        the plan for the next session
    10-wiikit.md              how this port uses and grows wiikit

Playing: wiikit's Classic Controller mapping (the pad's buttons by
position; `build/keys.txt` for the keyboard). F11 fullscreen, F12 a GX
trace.

## Licence

MIT. This covers the documentation and tools in this repository only. It
says nothing about Castlevania Judgment, which remains the property of its
rights holders.
