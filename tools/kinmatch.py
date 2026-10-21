"""Name a stripped DOL's functions from a kin: another stripped DOL, already
named, built with the same SDK libraries.

Arc Rise Fantasia's main.dol has the very builds of KPAD (Aug 8 2007), WPAD
(Dec 11 2007) and PAD (Oct 3 2007) that Castlevania Judgment has, and its
build/names.tsv names their functions (by hand, by string, by signature).
A function here whose words hash as one there, with immediates and branch
targets masked (Dolphin's checksum, tools/sigmatch.py) and of the same size,
is the same function. Spans are the recompiler's own units on both sides.

Only one-to-one matches are kept: a hash that lands on two functions in
either DOL says nothing.

    python tools/kinmatch.py build/extract/sys/main.dol \\
        --kin <pc-arcrisefantasia>/build/extract/sys/main.dol <pc-arcrisefantasia>/build/names.tsv \\
        --out build/kin_guess.tsv
"""
import argparse
import collections
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # wiikit/

from wiikit.dol import Image
from wiikit.recomp.discover import symbolise
from tools.sigmatch import checksum


def spans(img):
    units, _ = symbolise(img, log=lambda m: None)
    starts = sorted(s for s, _ in units)
    out = []
    for seg in img.text_segments():
        inside = [s for s in starts if seg.vaddr <= s < seg.vaddr + len(seg.data)]
        for a, b in zip(inside, inside[1:] + [seg.vaddr + len(seg.data)]):
            words = struct.unpack_from(f">{(b - a) // 4}I", seg.data, a - seg.vaddr)
            out.append((a, b - a, checksum(words)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dol")
    ap.add_argument("--kin", nargs=2, action="append", required=True, metavar=("DOL", "NAMES"))
    ap.add_argument("--min-size", type=int, default=0x10)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    mine = spans(Image(a.dol))
    here = collections.Counter((s, c) for _, s, c in mine)
    found = {}
    for kdol, knames in a.kin:
        names = {}
        with open(knames, encoding="utf-8") as f:
            next(f)
            for line in f:
                p = line.rstrip("\n").split("\t")
                names[int(p[0], 16)] = p[1]
        kin = spans(Image(kdol))
        there = collections.Counter((s, c) for _, s, c in kin)
        by_key = {(s, c): names[ad] for ad, s, c in kin if ad in names and there[(s, c)] == 1}
        tag = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(knames))))
        delta = {}                               # kin address -> this DOL's, for unique matches
        kin_at = {ad: (s, c) for ad, s, c in kin}
        mine_at = {ad: (s, c) for ad, s, c in mine}
        for ad, s, c in mine:
            if s >= a.min_size and here[(s, c)] == 1 and (s, c) in by_key:
                found.setdefault(ad, (by_key[(s, c)], tag))
        unique_kin = {(s, c): ad for ad, s, c in kin if there[(s, c)] == 1}
        for ad, s, c in mine:
            if s >= a.min_size and here[(s, c)] == 1 and (s, c) in unique_kin:
                delta[unique_kin[(s, c)]] = ad - unique_kin[(s, c)]
        # The rest by place: a kin's name between two unique matches that moved
        # by the same amount, where this DOL has a function of the same size
        # and hash at the same distance (the WPAD.o thunks, the setters).
        anchors = sorted(delta)
        import bisect
        for kad, n in names.items():
            if kad not in kin_at or kad in delta:
                continue
            i = bisect.bisect_left(anchors, kad)
            if i == 0 or i == len(anchors):
                continue
            lo, hi = anchors[i - 1], anchors[i]
            if delta[lo] != delta[hi]:
                continue
            ad = kad + delta[lo]
            if mine_at.get(ad) == kin_at[kad]:
                found.setdefault(ad, (n, tag + " (by place)"))
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("addr\tsize\tname\tkin\n")
        for ad in sorted(found):
            f.write(f"{ad:08X}\t-\t{found[ad][0]}\t{found[ad][1]}\n")
    print(f"{len(found)} functions named by kin -> {a.out}")


if __name__ == "__main__":
    main()
