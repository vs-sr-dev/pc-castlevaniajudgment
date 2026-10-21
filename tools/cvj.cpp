// Castlevania Judgment — the port's own layer over the wiikit runtime.
//
// Linked into wiiboot by cvj.cmake; the functions it replaces are listed in
// cvj-hooks.txt, which the recompiler takes with --hooks. What belongs here
// is what only this game needs.
#include "rt.h"

namespace {

void install() {
    // The 2007 SDK's KPAD (Aug 8 2007): KPADStatus is 0x84 bytes, and the
    // game reads 16 of them a channel (800F97E4, strides of 0x840).
    wpad_set_kpad_status_size(0x84);
    // Played with the Classic Controller, read from KPAD's status.
    wpad_set_classic(true);
}

RtGameLayer layer("Castlevania Judgment", install);

}  // namespace
