# wiikit: what this port asks of it

The port takes wiikit as a submodule at `wiikit/`, pinned at d9d14c0, the
other ports' commit.

So far, nothing new. The game boots, plays its movie, and reaches its menus
on wiikit as it was. Its layer (`tools/cvj.cpp`) asks only for what wiikit
already offers: `wpad_set_kpad_status_size(0x84)` and
`wpad_set_classic(true)`, with the Classic read from KPAD's status.

What this port brought that may move into wiikit:

- **Names by kin** (`tools/kinmatch.py`): a stripped DOL named from
  another stripped DOL already named, when both have the same SDK builds.
  With `tools/sigmatch.py` it belongs in wiikit's planned `sig` (layer 3,
  "names by signature in stripped executables"), together with the
  release-build strings that say which ports are kin.
