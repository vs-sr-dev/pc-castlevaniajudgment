# wiikit: what this port asks of it

The port takes wiikit as a submodule at `wiikit/`, pinned first at d9d14c0, the
other ports' commit, then at cbd441b, this session's fog and NAND fix
(checked on the eight other ports), then at ce8560e (its README names
this port).

The game boots, plays its movie, and reaches its menus on wiikit as it
was. Its layer (`tools/cvj.cpp`) asks only for what wiikit already offers:
`wpad_set_kpad_status_size(0x84)` and `wpad_set_classic(true)`, with the
Classic read from KPAD's status.

Session 1 added two things, game-agnostic:

**1. GX fog** (gxshader.cpp, video.cpp). BP 0xEE-0xF2 (A, B's magnitude
and shift, C, projection, type, colour) and 0xE8-0xED (the range
adjustment). In the fragment shader, after the alpha test: the EFB's 24-bit
Z; ze = A / (B_mag - (Z >> B_shift)) in perspective, A * Z in orthographic;
times sqrt(x^2 + k^2) / k with the range on; f = clamp(ze - C, 0, 1),
through the exponential curves (types 4 to 7); the colour toward the fog
colour by f in 1/256ths, alpha untouched. The type, the projection and the
range enable are in the program's key; the rest are uniforms. After
Dolphin's software renderer (`Tev.cpp`).

**2. ReadDir on a file is "invalid"** (ios.cpp). The SDK's `NANDGetType`
reads a path as a directory to tell a file (-101, `FS_EINVAL`) from a
directory (0) from nothing (-106). wiikit answered -106 for a file, so a
game that checks its save so found none.

What this port brought that may move into wiikit:

- **Names by kin** (`tools/kinmatch.py`): a stripped DOL named from
  another stripped DOL already named, when both have the same SDK builds.
  With `tools/sigmatch.py` it belongs in wiikit's planned `sig` (layer 3,
  "names by signature in stripped executables"), together with the
  release-build strings that say which ports are kin.
