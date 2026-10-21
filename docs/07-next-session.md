# Next session

## Where it stands

The game plays (session 1): menus, the save kept, fights, fog. The click
at stage loads is the one sound fault heard.

Run (from `build/run1`, or `sh build/play.sh` from anywhere):

    ../recomp-build/wiiboot ../extract --symbols ../recomp/symbols.tsv --nand ../nand --fonts ../fonts

Rebuild: `sh build/rebuild.sh` from the root. `build/nand` keeps the save
file the game created.

## Plan

1. **Play.** The user, with the pad: the modes (Story, Arcade, Versus,
   Castle mode), several characters and stages, a whole match. Note
   anything wrong in the picture (effects, transparency, fog, the
   models' outlines), the sound, the timing and the controls.
2. Whatever that finds. Candidates, from the other ports:
   - Z textures, still to come in wiikit (none reported yet);
   - the click at stage loads (shader links? the AI interrupt?);
   - EFB copies read by the CPU (the report counts "EFB peeks": 0 so far);
   - the frame rate in fights (two models, effects, stage);
   - the Story mode's cut-scenes.
3. The controls: the Classic's mapping on the pad (attacks on the face
   buttons, guard and sub-weapon on the shoulders); the game's own button
   configuration first.
4. Then publish: the repo `pc-castlevaniajudgment`, and the line in
   wiikit's README port table (what it asked of wiikit: GX fog, the
   NAND's answer to a directory read on a file; names by kin, if they
   move into wiikit). Until then wiikit's commits call it "a stripped 2008
   game".
