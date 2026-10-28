/*
 * Nutrimatic Website - desk-scene.js
 * Version 0.27.3
 *
 * Created: 2026-10-01 - Living pixel-art scene of the co-founders at their desk (v0.1.0)
 * Modified: 2026-10-01 - Likeness pass (v0.2.0); browline glasses, desk lamp, blazer (v0.3.0); redraw at a larger scale (v0.4.0)
 * Modified: 2026-10-01 - Seated proportions with jointed arms; two layouts (wide desk on desktop, closer on phones);
 *   name plates; articulated lamp that swings over whoever is soldering or writing and casts a cone of light; New York
 *   skyline that lights up at night; scripted scenarios (Nintendo DS, paper airplane, pigeon, cat, coffee run,
 *   shake break, late night, solder spark); desk set per visit; no frame, no speech bubbles (v0.5.0)
 * Modified: 2026-10-02 - The figures are no longer drawn in code: they come from portraits generated from photos and
 *   finished as sprites (js/desk-sprites.js). A figure is a torso and a head (the head nods), a face built from blink /
 *   look / brow / mouth frames, and jointed arms drawn as capsules and posed by two-bone IK, so every behaviour and
 *   scenario from v0.5 still plays. Stage 160 pixels high (the phone layout is 240x160, a Game Boy Advance screen).
 *   The room: ceiling, pendant light, warm walls, a sun patch by day, blue dark with warm pools at night. The cat is
 *   Maker (v0.6.0)
 *
 * Modified: 2026-10-02 - No arm is drawn in code any more ("arms and hands look dreadful"). Every activity has a body pose
 *   generated as one picture (torso, arms, hands and what they hold) and drawn under the same head; the hands' part of a
 *   pose lies over the desk; a few poses have a front part over the face (v0.7.0)
 *
 * Modified: 2026-10-02 - Bodies no longer bob (a laptop moved with the breath); a nod is a forward tilt (the face
 *   shortens a pixel) rather than the head moving down; both tilt toward their work and look at it; Ilinca's head
 *   sits lower (her neck read too long); small expression changes for both, Ilinca at rest no longer smiling. The room
 *   is generated art now, like the figures (assets/desk/*.png): painted brick, a steel factory window onto Midtown
 *   (Empire State, Chrysler, One Vanderbilt; lit at night after the real skyline), shelves, a walnut desk, and an
 *   anglepoise lamp each, Cole's red and Ilinca's white. Writing moves the hand; the bottle is handed across with
 *   both arms out. Maker is a fifth bigger and shaded; she kneads her spot, lies on the desk for a while, gets
 *   petted, blinks, looks at them, sits on a laptop or the paper (and is petted anyway), keeps clear of the
 *   soldering, and they lift their hands when she walks past (v0.8.0)
 *
 * Modified: 2026-10-02 - A stretch shuts the eyes, turns the face up and opens the mouth, and they never stretch at the
 *   same time. Mondrian's Victory Boogie Woogie hangs where the poster was. Maker stands on the desk top in both
 *   layouts; lying down she lies at its front edge, a paw over it and her tail hanging down the front, swinging (a
 *   jointed chain, the tip trailing) (v0.9.0)
 *
 * Modified: 2026-10-03 - A click gets a brief look, a nod, a smile and a casual wave from the one clicked (now and then
 *   they tell the other, who says hello too); the hover hello is just a glance. A nod moves the face down a pixel inside
 *   the head instead of folding it. A stretch leans right back for a moment (that frame keeps the picture's own head).
 *   The laptop stays put while they wave. Maker can be shown with big stylized eyes (catStyle) to compare (v0.10.0)
 *
 * Modified: 2026-10-03 - The stretch keeps their own faces (no frame with a generated head). Maker on a keyboard: the
 *   typing hands stay put behind the screen, a look, then a resigned smile. Her hanging tail ends round (v0.10.1)
 *
 * Modified: 2026-10-03 - Maker's big stylized eyes are her look now; the comparison switch is gone (v0.11.0)
 *
 * Modified: 2026-10-03 - After a full audit of hands, objects and layering against reference photos: the room is drawn
 *   on its own layer so night shades whatever stands in front of the window; Maker walks in a four-frame cycle, her
 *   hanging tail is thicker and moves in steps with a flick; she steps up behind the laptop screen onto the keyboard;
 *   petting is rigged (she lies where the cat was in the petting picture, the hand strokes along her back), on the
 *   paper too; petting starts when she settles; shaking moves only the arms; Ilinca looks straight at her laptop (v0.12.0)
 * Modified: 2026-10-03 - Ilinca's phone lies on her right, clear of her (now larger) laptop (v0.12.1)
 * Modified: 2026-10-03 - Maker walks with twelve rigged frames (tools/desk/walk_rig.py), picked by how far she has moved,
 *   so her feet stay planted on the desk (v0.13.0)
 * Modified: 2026-10-03 - The test state reports whether Maker is behind a laptop screen (v0.13.1)
 * Modified: 2026-10-03 - Every activity moves a little (typing forearms behind the screen, the trackpad, thumbs on the
 *   console, a fidgeting hand, a scrolled phone, soldering changing position); hands go under the desk, not up in the
 *   air, as soon as Maker's body would reach them, also when she comes for a laptop or a paper (a mug is lifted to drink
 *   instead); the laptop or paper stays put meanwhile (it had vanished: kept before it was known); on a laptop she goes
 *   behind the screen as soon as she touches it and comes out once clear of it (v0.14.0)
 * Modified: 2026-10-03 - A solder spark starts at the iron's tip, in either way of holding it; the station and the board
 *   stay on the desk while he waves the smoke away (they vanished with the soldering pose) (v0.14.1)
 * Modified: 2026-10-03 - Cole's note 10: a looking-down head for both, drawn whenever they look down at something (the
 *   work, the DS, the cat, a pointer over the desk) and for a nod; the one petting Maker looks at her (v0.15.0)
 * Modified: 2026-10-03 - Maker's new walk (Cole's note 9e): ten frames a cycle, a cat's lateral-sequence walk built
 *   from tools/desk/docs/animal-walk-cycles.md (v0.16.0)
 * Modified: 2026-10-04 - Cole's note 11: looking down at the work their eyes are open, looking down; the shut lids are
 *   kept for a nod (and a blink) (v0.16.1)
 * Modified: 2026-10-04 - Cole's note 12 ("now that the desk is 3d"): the desk has a top, DESK_DEEP rows from the far
 *   edge to the front edge (DESK_FRONT); things stand on it at their depth (deskAt), the nameplates sit on the drawers,
 *   the lights reach the front edge; Maker walks on its front half, kneads, sits and lies at the front edge (paws and
 *   tail over it), petted with the new petedge poses, and curls up on Ilinca's paper at the back; Ilinca no longer
 *   stretches (v0.17.0)
 * Modified: 2026-10-04 - The shake handover skips Cole drinking from the shaker (to-do T18) (v0.17.1)
 * Modified: 2026-10-04 - No high five: their raised hands never met (Cole: make them smack or drop it, to-do T21) (v0.17.2)
 * Modified: 2026-10-04 - A ceiling light: a generated pendant between them, lit after dark (to-do T15) (v0.18.0)
 * Modified: 2026-10-04 - The pigeon is outside, behind the window's glass and bars (to-do T27) (v0.18.1)
 * Modified: 2026-10-04 - Cole's round of notes T29-T46: both type on the same laptop, drawn in front of the neck and the
 *   hair; a greeting holds one raised hand while the other arm stays where it was (the wave poses built per activity);
 *   the spark gets a start and a hand to his head instead of fanning; four pendants, hung higher; the pigeon walks the way
 *   it faces; no looking down over a coffee, no mouth drawn at a mug or bottle, eyes shut for a sip; the paper plane is
 *   folded in three steps and glides off out of the room; finger-drumming and call frames; solder2 retired (v0.19.0)
 * Modified: 2026-10-05 - Cole's notes a-o (to-do T49-T63): the phone layout's room no longer has a second desk top
 *   behind the figures (they looked seated in the desk) and Ilinca's lamp stands on the desk, she a little left of it;
 *   a layout switch keeps Maker, the pigeon, the plane and desk things beside whoever placed them; their typing never
 *   in step; a greeting is a nod or a wave, chosen at random; by day a working lamp lights only the desk (over his shirt
 *   it read as a third arm); only the hand on Maker's head is drawn over her; the thrown plane as big as the folded
 *   one (v0.20.0)
 * Modified: 2026-10-05 - Hooks for the approval page (to-do T64): .review({cole, ilinca, greet, relay, petter, pointer})
 *   holds each figure on one activity, stops scenarios and conversations starting by themselves and fixes the random
 *   choices (nod or wave, who pets Maker); .review(null) lets the scene run on its own again (v0.20.1)
 * Modified: 2026-10-05 - Round-30 audit: no talking arms from thinking (his shoulders jumped) and no conversation during a
 *   greeting; the phone layout's lamp in frame; clouds pass behind the window frame; the thrown plane leaves his hand
 *   where he held it, behind his fingers, and climbs clear of Ilinca's head; his waving arm in front of his lamp; no
 *   mouth drawn under a yawning hand, no looking-down head in a yawn; Ilinca's stroke frame redraws only her hand (v0.20.2)
 * Modified: 2026-10-05 - Final round-30 audit: the lamps stand behind the figures (their feet on the desk in front; the
 *   phone layout's red lamp had covered Cole's shoulder), so his waving arm needs no redraw; the plane is not drawn in its
 *   release frame; no cloud piece under four pixels; one phone: blue on the desk, and buzzing it hops in place (v0.20.3);
 *   a bulb glows at night only where no figure covers it; the plane first shows clear of his fingers; the soldering
 *   station stays on the desk while he greets from soldering (v0.20.4)
 * Modified: 2026-10-06 - Hook for the hand library (to-do round 31): .patchPoses(who, {pose: layers}) swaps poses in from
 *   candidate art (the same palette), .unpatchPoses(who) puts the originals back; .still(on) holds faces and clouds for
 *   exact captures (v0.21.0)
 * Modified: 2026-10-06 - Phone layout (T92, "red lamp is behind cole"): the figures a little right (Cole 74, Ilinca 156) and
 *   the lamps further out (2, 226), so the red lamp stands clear of him in every pose, neither behind nor in front (v0.21.1)
 * Modified: 2026-10-06 - Desktop layout likewise: the red lamp at 40 (its shade ended behind his raised elbow in a wave and
 *   the stretch), the left desk prop at 18 so the widest one clears the lamp's foot (v0.21.2)
 * Modified: 2026-10-06 - Phone layout (audit of T73/T82): the figures 92 px apart again (Cole 80, Ilinca 172; the
 *   lamp fix had brought them to 82, so her elbow met his arm), the lamps half out of the frame (-1, 241) so neither
 *   touches a figure in any pose; the shaker still passes hand to hand; on a phone the pigeon comes straight down to the
 *   sill, so it walks clear of her hair (v0.21.3)
 * Modified: 2026-10-06 - Ilinca typing (T73, "doesn't appear to move"): each forearm eases in a pixel, then two, and back
 *   (her new type3 frame), at her own times and never in step with Cole; her hand rests on the trackpad 1 s, not 2 (v0.21.4, merged from r31-arms)
 * Modified: 2026-10-06 - Layout audit of T92: on phones the red lamp at -4 (his fist pump met its shade, his waves kept one
 *   pixel; now every pose of his clears it by 3); in the wide layout the white lamp at 294 (her shoulder had touched its
 *   shade since 91d954b; now 2 clear pixels in every pose she takes); the shake handover with the two leaning toward each
 *   other, a pixel a frame (L.lean), so the shaker moves 2 px as it changes hands, both hands on it (it had jumped 18 px on
 *   a phone, 28 in the wide layout); her plate stands clear of Maker's hanging tail when she pets her; on a phone the
 *   pigeon walks the sill at half the pace, staying in one pane, clear of the middle bar (v0.21.5)
 * Modified: 2026-10-06 - Shake break (Cole's pick after the layout audit of e6ce904: "Slide it"): the lean is gone; he sets
 *   the shaker down on the desk and it slides across to her, slowing, 4 px a frame at most, to stop at her left in front of
 *   the desk's edge; she reaches for it, lifts it and drinks, and sets it down where she took it; nobody moves in their
 *   seat. Her laptop or paper stays on the desk while she does (T48, p.deskProp). Both name plates by one rule, 13 px right
 *   of their owner's middle (clear of Maker's tail and paw in either visit); on a phone the red lamp's foot corner is not
 *   drawn (it read as a stray blob) (v0.21.6)
 * Modified: 2026-10-06 - Round 31: soldering, every two or three seconds both hands and their tools move a pixel along
 *   the board and back (to-do T67: solderR, solderL and their lifted frames); after the spark, while his hands are off
 *   the board, his lamp's beam at night falls on the desk only, as by day (T84: over his shirt it read as an arm) (v0.22.0)
 * Modified: 2026-10-06 - Round-31 audit rework: while his hands are off the board (the spark's start and facepalm, a wave
 *   hello from soldering) his lamp stays on, the iron rests in the station's holder and the pick on the board, so the
 *   tools never vanish (restingIron, restingPick); at night the beam is kept off his own pixels only (figureMask), so the
 *   station and the board stay lit exactly as while he solders (the row cut had left the station half lit) (v0.22.1)
 * Modified: 2026-10-06 - Round-31 second audit rework (T67, T84): the resting iron stands in the holder socket at the
 *   station's top-right corner and leans over his shirt towards him (in the crossbar, leaning either way, it crossed the
 *   forearm he throws up in the start, his arm down in his lap in facepalm, or the lamp); the resting pick lies on the
 *   desk in front of the board at the length it has in his hand, 28 px (it was 17 on the board) (v0.22.2)
 * Modified: 2026-10-06 - Round-31 third spark rework (T67, T84): anywhere in or on the station the iron crossed his body,
 *   and in a wave the holder's crossbar is right under his raised elbow; the puff now makes him drop both tools on the
 *   desk, and in a wave he lays the iron down at the same place: flat, right of the board, 2 px of desk all round it in
 *   every frame and both layouts, its tip still pulsing (IRON_FLAT); the pick's handle end tapers as in his hand and it
 *   lies 9 px further left; at night the station's holder darkens to the station's own grey, so under the lamp it no
 *   longer melts into his hand behind it (v0.22.3)
 * Modified: 2026-10-06 - Round-31 fourth spark rework (T67, T84; audit of 99c05d7): the soldering station loses its T holder,
 *   which no longer takes the iron and stood where his arms go (in facepalm it framed his lap hand and left a pixel of skin
 *   beside it, in the start the same sliver, in a wave it lay on his raised elbow's outline); the box reads as a station by
 *   its face instead: a temperature knob, the heater's red light, an orange readout (STATION_FACE). The dropped pick lies
 *   three rows high in rows 138-140, 2 px of desk from the station, the board, the iron and the desk's front edge (v0.22.4)
 * Modified: 2026-10-06 - Round-31 fifth spark rework (T67, T84; audit of 658787a): the dropped pick is as thick as the pick in
 *   his hand again (2 rows of yellow handle and the 1 px steel point inside its outline, rows 138-141, 28 px), with a tapered
 *   point that keeps 2 px of desk from the station's corner and 1 row to the desk's front edge; the station's knob is a mid
 *   grey with a faint lighter top edge (it was the box's brightest pixel, a light dot at display size); where his outline
 *   meets the station's box a wedge of skin narrowed to a 1 px sliver (above the box in facepalm, at its left edge while
 *   soldering): those pixels take his line colour, so his line runs into the box (STATION_SEAL) (v0.22.5)
 * Modified: 2026-10-06 - Round-31 sixth spark rework (T67, T84; audit of 3176b99): the facepalm seal keeps his crease a clean
 *   diagonal (its last step one line pixel, his crease brown beside it, no 2x2 black foot); the seal pixels are drawn with
 *   his figure (drawSeal in drawCharacter), so at night they take his lighting, not the station's under the lamp; each is
 *   drawn only where his pose still shows a pixel of skin between one of his lines and the box's edge, so a later redraw of
 *   his hands cannot leave a stray line pixel (v0.22.6)
 * Modified: 2026-10-06 - Maker on a laptop (T89, "just make the laptop screen the frontmost object in the scene instead of
 *   moving maker around"): no step up onto the keyboard and never behind the desk; she walks on the desk top to its back,
 *   where the laptop stands, and the laptop is drawn over her, so she peeks over the screen. On his laptop, after a moment
 *   of looking annoyed, Cole strokes her back, his hand out of sight behind the screen (T88). With the hands off the paper
 *   the whole sheet stays on the desk (T91) (v0.21.2 on r31-maker)
 * Modified: 2026-10-06 - Round-31 audit of T88/T91: hands under the desk end on the desk's back edge in both layouts (the
 *   wide room draws that edge two rows higher, row 132, than the phone's, row 134: those poses are clipped there, and
 *   nothing of them is drawn on the desk); stroking Maker behind his laptop screen his arm reaches up to her back (a
 *   hand-drawn arm, T88); in the visit the laptop or the paper stays on the desk while they stroke her, the stroking arm
 *   in front of the screen as it reaches round it (or on the paper), the other hand at the keyboard (T91) (v0.21.3 on r31-maker)
 * Modified: 2026-10-07 - Layout audit of 80a0d7f (T48 in the shake): with her laptop left on the desk her hands at its
 *   keyboard stay behind it, none of them below its front edge; the paper left on the desk is whole and the shaker in his
 *   hands is the desk one (tools/desk/poses.py v1.11.3); a paper left on the desk (a greeting, Maker on the desk too) lies
 *   whole under the hands, not over them (v0.21.7)
 * Modified: 2026-10-07 - Layout audit of cf7f44a: his paper's sheet starts at the desk line (its top edge had drawn over his
 *   hand on row 133); her reach for the shaker has her body down to the desk (tools/desk/poses.py v1.11.4) (v0.21.8)
 * Modified: 2026-10-07 - Layout audit of f148c83: his kept sheet closed by its top edge again, that row drawn before the
 *   figures so he stays in front of it (on a phone the desk's back edge had looked broken beside the cat); her drink picture
 *   with her body down to the desk (tools/desk/poses.py v1.11.5) (v0.21.9)
 * Modified: 2026-10-07 - Layout audit of a426cd5: in the wide room his kept sheet runs up to the desk's own back-edge line
 *   (its own top edge under that line had made a doubled dark band); her take picture with her body down to the desk
 *   (tools/desk/poses.py v1.11.6) (v0.21.10)
 * Modified: 2026-10-07 - Round-31 integration (r31-int): r31-nonhand (v0.21.10: the phone layout, the lamps, the
 *   plates, the pigeon, the shake "Slide it", her work kept on the desk, merged with r31-arms and r31-body) and r31-spark
 *   (v0.22.6: T67 tools moving on the board and dropped on the desk, T84 the station without its holder, STATION_SEAL)
 *   merged; the station, the dropped tools and the seal follow Cole, so they keep their places in the phone layout
 *   (tools/desk/poses.py v1.13.0) (v0.23.0)
 * Modified: 2026-10-07 - Round-31 integration, T48 (desk things vanishing on activity changes), the coordinator's decision on
 *   the soldering station: the shake never starts while he solders (the shaker would slide through his tools on the desk);
 *   a scene that takes his hands off the board while he solders (scenario.bench: the DS) leaves the bench as the spark does,
 *   the station and the board on the desk and his tools lying flat at their audited places (p.benchFrom), and when it ends
 *   he goes back to soldering and picks them up (backToBench); caught with the DS he goes back to the board, not to a
 *   laptop; the station seal covers the DS poses ('hide' as facepalm, the DS poses at the box's top right corner) (v0.23.1)
 * Modified: 2026-10-07 - Round-31 integration, T48 (proposed, separable): the airplane, the late-night yawns, the coffee and
 *   the call do not start while he solders either: each puts his forearm, his mug or his hands flat on the desk right where
 *   the board and the dropped tools lie, so the bench cannot stay through them; while he solders only the spark, the
 *   pigeon and the DS can start (v0.23.2)
 * Modified: 2026-10-07 - Round-31 integration: r31-maker's audited core (0ad6b9d: hands under the desk clipped at the
 *   desk's edge, Cole stroking Maker behind his laptop screen, the visit keeping the laptop and paper, Maker behind a
 *   frontmost laptop screen) merged. One desk-edge setting per layout (art.deskEdge: 132 wide, 134 phone) for both the
 *   hands under the desk and his kept sheet's top; one sheet drawing, the whole paper under the hands (r31-nonhand's,
 *   closed by its top edge), so the visit and the laptop scenes draw no second sheet; the petting arm's 'over' layer
 *   after the props; a seal pixel is never drawn below the desk edge of a pose clipped there (v0.24.0)
 * Modified: 2026-10-07 - Round-31 integration fix: in the visit, stroking Maker from his paper, the sheet under his hands had lost
 *   its white to his petting pose's shirt hem on the desk's first row (a thin grey line was left: the paper read as gone);
 *   a pose with an arm drawn 'over' gets the paper's sheet over it once more and the arm over that, as r31-maker's audited
 *   visit drew it (v0.24.1)
 * Modified: 2026-10-08 - Round-31 integration audits: no looking-down head over the stretch (in a nod or a listening nod
 *   its outline left two pixels of wall beside his raised arm; the stretch keeps its own head and the nod tilts the face);
 *   the DS poses' two-deep skin wedge at the station's box top sealed (his crease brown and line, a two-deep case in the
 *   seal's guard); the scenes kept from starting while he solders ask soldering(), so a greeting from soldering counts, and
 *   no scene starts in the middle of a greeting; the shake's shaker stops 49 px from her in the wide room (2 clear px from
 *   every pose of hers and of his) and, on a phone where the two of them sit too close for it, she reaches for it 6 px
 *   before its stop and keeps it after drinking (L.shake) (v0.24.2)
 * Modified: 2026-10-27 - T128 (Cole: "For the moment, we can give them everlasting cups of coffee. They can sit on the table,
 *   steaming gently"): the coffee run is shelved (COFFEE_RUN, off; its code kept). Each of them has a red mug standing on
 *   the desk all the time, at the size of the mug in his hand (T94: one mug size, the bigger one), on their outer side by
 *   their lamp, where nothing else they do reaches (T48: the coffee poses' spot in front of them is where the laptop, the
 *   paper, the board and the hands go); a wisp of steam rises from each in a slow loop, out of step with the other. Their
 *   coffee lifts it from there to the lips (sip) and sets it back, the hands at rest between sips (the poses that hold it
 *   on the desk in front, mug and mugWave, are no longer drawn); no mug on the desk while one is held. To make room the
 *   lamps stand a little further out in the wide room (38, 298; the desk props at 16, 321, 345) and on a phone the white
 *   lamp shows only its arm and shade, like the red one; the buzzing phone's marks go to its lower right, clear of her mug (v0.25.0)
 * Modified: 2026-10-27 - Audit of T128 (6e92bba): her phone back where it lay (2 px in it came within a pixel of her sipping
 *   sleeve); buzzing it hops sideways on the desk without rising a row, so it keeps 2 px from every pose of hers and from her
 *   mug's foot. The steam is laid on last at every hour in one colour taken from the lit wall behind it, a little darker
 *   on a pale wall, lighter on a dark one (at dawn and dusk the day and night steam had cancelled out) (v0.25.1)
 * Modified: 2026-10-28 - T128 follow-up, Cole: "the coffee mugs should be nudged slightly down (forward) on the desk" and "On
 *   coffee drinking, what's missing is the mug in hand on table stage before the drink": the mugs stand 3 rows further
 *   forward (bottom row 138); Maker walking behind one (at a laptop) has it drawn in front of her. Their coffee is one sip
 *   now: the hands at rest, a reach, the hand round the mug where it stands (held a beat, still steaming), the lift in 21
 *   steps (the mug at most 4 px a step) to the sip (his M0-R; hers the same mirrored to her mouth, her left hand, her right
 *   in her lap), the same steps down, the mug set down and held a moment, the hand back (COFFEE_SEQ; frames from
 *   tools/desk/coffee_frames.py). Maker passing lifts the mug the same way and puts it back from where it was (holdcup).
 *   A pose's 'u' columns end at the desk's edge, as a pose under the desk does (her arm in her lap). Her phone lies 2 px in
 *   and buzzing hops a pixel to her side only, 2 px from her mug and from her in every pose (v0.26.0)
 * Modified: 2026-10-28 - Go-live (Cole: "let's focus on getting some scenes DONE so we can bring this live, then we can take
 *   our time improving it"; scenes not done: "switch off"): every unfinished scene or piece is off behind its own flag in
 *   SCENE_ON (his and her writing, the spark, the airplane, the shake break, drinking coffee, his wave, his talking hand, the
 *   high five, Maker's visits and laptop/paper scenes without a finished stroke), the code kept. His picks from the hand pages
 *   are in the art (tools/desk/hand_maps.py): his resting pose R2 everywhere, its hidden arm ending at each layout's desk
 *   edge (a pose's phone-layout body, 'bn'), thinking TB, the yawn Y1 with his face tipping back as he yawns, the handheld
 *   D1 (the station's seal no longer drawn on it), soldering S2 (the iron's tip where its tip is), petting E2 on his paper
 *   and E3 in the visit (their hand boxes); her phone P1. His red lamp 3 px further out in the wide room (35; the left desk
 *   prop with it, 13) so his shake will clear it; no scene starts while he stretches (a stretch was held through it) (v0.27.0)
 * Modified: 2026-10-28 - Audit of the go-live (Cole's standing rule: props never vanish): a short break from the laptop or the
 *   paper (a stretch, the late-night yawn, the fist pump, her phone ringing) leaves it on the desk where it stood (p.deskProp,
 *   as in the shake break), and the work goes on after it; anyone still at work when a scene ends works on a while; the DS
 *   waits while he types (its console is held where the screen stands). His mug's steam a pixel further out, 2 px clear of
 *   his lamp's shade (v0.27.1)
 * Modified: 2026-10-28 - Re-audit: at his laptop he yawns where he sits, hands at the keyboard (his raised wrist had sat
 *   exactly on the screen's top edge, as if resting on it; the hand to his mouth, Y1, when he is not typing); on the call
 *   she tells him the news with her hands back at her laptop (her talking forearm ran down its edge); the test state says
 *   whose laptop or paper is on the desk (.state().work), the kept ones included (v0.27.2)
 * Modified: 2026-10-28 - T141 ("paper moves under ilinca's hand", on the go-live page): with writing off, asked to write
 *   (the approval page's cards held her at her paper) they type, so no sheet is on the desk (v0.27.3)
 *
 * Markup: <div data-desk-scene><canvas></canvas> ...fallback... </div>, with js/desk-sprites.js loaded first.
 * Test hooks (.state().mugs: whether each one's mug stands on the desk): window.NutrimaticDesk.setHour(h), .activity(who, name, secs), .react(who), .scenario(name), .converse(i),
 *   .face(who, {mouth, brows, look}), .poses(who), .step(n), .state(), .review(o), .patchPoses(who, poses), .unpatchPoses(who), .still(on),
 *   .scenesOn() (a copy of SCENE_ON)
 */

(function () {
  "use strict";

  var FPS = 12, DESK_Y = 134, CEIL = 8;
  // The desk has a top (Cole's note 12): DESK_Y is its far edge, where the figures meet it; DESK_FRONT its front edge,
  // DESK_DEEP rows nearer. Things stand on it at a depth between the two (deskAt), Maker walks on its front half and
  // lies at its front edge with her paws and tail over it.
  var DESK_DEEP = 9, DESK_FRONT = DESK_Y + DESK_DEEP;
  function deskAt(d) { return DESK_Y + Math.round(d * DESK_DEEP); }
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // Go-live (Cole, 2026-10-28: "let's focus on getting some scenes DONE so we can bring this live, then we can take our time
  // improving it"; a scene not done at launch: "switch off"). One flag per unfinished scene or piece: its code stays as it is,
  // and true brings it back. (The coffee run keeps its own flag from T128, COFFEE_RUN.)
  var SCENE_ON = {
    coleWrite: false,       // his writing (WR6, one fix away: "sleeves are layered behind arms"): not one of his activities
    ilincaWrite: false,     // her writing ("needs work" on the round-31 page): not one of hers
    spark: false,           // the solder spark (K2, one fix away: the tools on the table too early, the board over his hands, the ending)
    airplane: false,        // the paper airplane (PL2, one fix away: "hands become very small during the fold ...")
    shake: false,           // the shake break: his shake, the slide, her take and drink (SK2, SL1, TK2, IS2 not all done)
    coffee: false,          // drinking coffee, both (her IM1 "very messy"; his resting left in it to be replaced): the mugs stay
                            // on the desk, steaming, and nobody lifts one (not as Maker passes either: that starts from a coffee)
    coleWave: false,        // his wave hello (no pick: W2's upper arm and shoulder not OK'd): his greeting is always a nod
    coleTalkHands: false,   // his talking hand (no TL pick): conversations go on, his hands stay at rest
    highFive: false,        // the high five (no H pick; no scene has played it since T21, the airplane's release used its pose)
    visitCole: true,        // Maker's visit, Cole stroking her (E3, OK'd)
    visitColeTyping: false, // ... while he types: one hand stays at the laptop (petedgeLap was drawn on his old petting pose, not
                            // on E3): the visit does not start while he types
    visitIlinca: false,     // Maker's visit, Ilinca stroking her (IE1, IE3 one fix away; IE2 needs work)
    laptopCole: false,      // Maker on his laptop (his arm reaching behind the screen, petlap: not on the hand pages)
    laptopIlinca: true,     // Maker on her laptop (OK'd on the round-31 page)
    paperCole: true,        // Maker on his paper, stroked with E2 (the pick); it only starts while he writes (coleWrite)
    paperIlinca: false,     // Maker on her paper (her stroke IE2 needs work; her writing is off too)
    lateNight: true         // the late-night yawn (his Y1, the pick)
  };

  var ART = window.NutrimaticDeskArt;
  var host = document.querySelector("[data-desk-scene]");
  var canvas = host && host.querySelector("canvas");
  if (!host || !canvas || !canvas.getContext || !ART || !ART.cole || !ART.ilinca) { return; }   // the photos stay as the fallback
  var ctx = canvas.getContext("2d");
  var off = document.createElement("canvas");
  var g = off.getContext("2d");
  // With the generated room the scene is drawn in two layers: the view through the window on `off`, everything in the
  // room on `fg` (left clear where the glass shows). The night darkens `fg` only, so whatever stands in front of the
  // window is in shadow too, while the city behind the glass stays lit.
  var fg = document.createElement("canvas"), fgx = fg.getContext("2d"), fgCopy = document.createElement("canvas"), fgCopyX = fgCopy.getContext("2d");

  /* ---------- layouts: a wide desk on desktop, the two of them closer on phones (240x160) ---------- */
  // With the generated room (assets/desk) the poster, clock and window are where that picture has them; `art` holds
  // those places, `win` etc. are the drawn room's (the fallback when the pictures do not load).
  var LAYOUTS = {
    wide:   { W: 360, H: 160, cole: 124, ilinca: 226, shake: { stop: 49 }, poster: { x: 14, y: 20, w: 58, h: 62 }, clock: { x: 88, y: 34 }, win: { x: 280, y: 22, w: 66, h: 74 }, lamp: 177, pendant: 121, slots: [36, 272, 338, 12, 306],
              art: { painting: { x: 7, y: 20 }, clock: { x: 88, y: 34, r: 7 }, win: { x: 262, y: 18, w: 88, h: 84 }, sky: { x: 254, y: 15 }, lamps: [35, 298], slots: [13, 321, 345], catY: 141, pendants: [96, 132, 216, 244], deskEdge: 132 } },
    narrow: { W: 240, H: 160, cole: 80, ilinca: 172, shake: { stop: 43, reach: 6, keep: true }, poster: { x: 1, y: 20, w: 51, h: 50 }, clock: { x: 98, y: 30 }, win: { x: 190, y: 22, w: 46, h: 66 }, lamp: 112, pendant: 126, slots: [226, 10],
              art: { painting: { x: 1, y: 18 }, clock: { x: 99, y: 31, r: 7 }, win: { x: 192, y: 20, w: 44, h: 70 }, sky: { x: 130, y: 3 }, lamps: [-4, 241], slots: [], catY: 141, pendants: [66, 118, 148, 175], deskEdge: 134 } }
  };
  // (T128: the wide room's lamps 2 px (red) and 4 px (white) further out than in round 31 (40, 294), and the desk props with
  // them (18, 318, 344), so each one's standing mug has 2 clear pixels from its lamp's foot, the props and every pose; see MUG)
  // (r33-live: his red lamp 3 px further out again, 35, so his shake will clear it when it comes back (SK2's cap kept 2 px
  // from the lamp at 35), and the left desk prop with it, 13: the papers, the widest at the foot, keep 2 clear px from it)
  // The environment pictures. Until they have loaded (or if they never do) the room is drawn in code as before.
  var ENV = { ready: false, img: {} };
  (function () {
    var base = "assets/desk/", names = ["room-wide", "desk-wide", "room-narrow", "desk-narrow", "sky-day", "sky-night", "lamp-red", "lamp-white", "prop-bottle", "prop-mug", "prop-papers", "prop-vase", "prop-plant", "painting-wide", "painting-narrow", "pendant-on", "pendant-off"], left = names.length;
    var inline = window.NutrimaticDeskAssets || {};                      // a self-contained preview hands the pictures over as data
    try { if (document.currentScript && document.currentScript.src) { base = new URL("../assets/desk/", document.currentScript.src).href; } } catch (e) { /* relative path */ }
    names.forEach(function (n) {
      var im = new Image();
      im.onload = function () { if (--left === 0) { ENV.ready = true; applyArt(); if (typeof render === "function") { render(frame); } } };
      im.onerror = function () { left = -1; };
      im.src = inline[n] || (base + n + ".png"); ENV.img[n] = im;
    });
  })();
  var L = LAYOUTS.wide, W = L.W, H = L.H, WIN = L.win, layoutName = "";

  /* ---------- palette (room and props; the figures carry their own) ---------- */
  var C = {
    wall: "#e9dfcc", wallD: "#d9ccb4", wallNight: "#1a1f3a", wallDusk: "#c47a4a", ceil: "#2d2a29", ceilL: "#4a4542", rail: "#b9a888",
    ink: "#111111", ink2: "#2a2a2c", ink3: "#3d3d40", grey: "#8d8d90", greyLight: "#c4c4c0", white: "#ffffff", red: "#e4002b", redDeep: "#a3001f", redLight: "#ff4d6a",
    deskTop: "#6b4a30", deskTopL: "#8a6442", deskTopD: "#4e3522", deskFront: "#3b2817", deskFrontD: "#2a1b0f", plate: "#efe9dc", plateS: "#b7ad99",
    green: "#2d6a3c", greenL: "#6fb57f", leaf: "#3f8f55", stem: "#4b7a3a", petalR: "#e4002b", petalW: "#ffffff", petalY: "#f2c744",
    pot: "#a3603c", potS: "#7c4428", board: "#2f6b3a", boardS: "#1f4a28", copper: "#d9a650",
    iron: "#9a9a9e", ironHot: "#ff6a3d", ironBlue: "#68aaf2", steel: "#cfd2d4", steelS: "#9a9ea2", pick: "#d9a650", knob: "#76787c", knobL: "#8c8e92", knobD: "#5c5e62", line: "#0f0503", crease: "#623e32", smoke: "#c9c6bf", smoke2: "#dedbd4", phone: "#3d5f99", phoneTop: "#6f93cf", phoneScreen: "#dfe9f5",
    paper: "#fbfaf5", paperLine: "#d9d5c8", mug: "#e4002b", mugS: "#a3001f", mugL: "#ff4d6a",
    laptop: "#cfd2d4", laptopS: "#9a9ea2", laptopL: "#eaeced", ds: "#d6162f", dsS: "#9d0f22", dsScreen: "#cfe3d4",
    lampBody: "#1b1b1b", lampShade: "#f2efe6", lampShadeOn: "#ffe9a8", bulb: "#fff1b8", pendant: "#1f1f22", pendantIn: "#ffe6a0", pendantOff: "#6d6d70", cord: "#2a2a2c",
    skyNight: "#0d1030", skyNight2: "#1a1f4a", star: "#ffffff", moon: "#f3f1d8", skyDawn1: "#f0a66a", skyDawn2: "#86a2d6",
    skyDay1: "#8dc5f0", skyDay2: "#cfe8fb", skyDusk1: "#f29a5c", skyDusk2: "#5d4e8c", sun: "#ffd84a", cloud: "#ffffff", cloudS: "#e8f1f8",
    bldg: "#6e7a8c", bldgFar: "#8f9bab", bldgNight: "#0b0d20", bldgNightFar: "#141735", winLit: "#ffd97a", winLit2: "#ffe9b0", beacon: "#ff3b3b",
    cat: "#7c8088", catD: "#5a5e66", catL: "#9ba0a8", catEye: "#c8d84a", catNose: "#4a4d54", catMouth: "#d98a92",
    pigeon: "#8a8f99", pigeonL: "#b4b8c0", pigeonD: "#5c6070", plane: "#ffffff", planeS: "#b9b9b5"
  };

  /* ---------- helpers: whole pixels only ---------- */
  function px(x, y, c) { g.fillStyle = c; g.fillRect(x | 0, y | 0, 1, 1); }
  function rect(x, y, w, h, c) { g.fillStyle = c; g.fillRect(x | 0, y | 0, w | 0, h | 0); }
  function hline(x, y, w, c) { rect(x, y, w, 1, c); }
  function vline(x, y, h, c) { rect(x, y, 1, h, c); }
  function outline(x, y, w, h, c) { hline(x, y, w, c); hline(x, y + h - 1, w, c); vline(x, y, h, c); vline(x + w - 1, y, h, c); }
  function limb(x1, y1, x2, y2, w, c) {
    var dx = Math.abs(x2 - x1), dy = Math.abs(y2 - y1), sx = x1 < x2 ? 1 : -1, sy = y1 < y2 ? 1 : -1, err = dx - dy, x = x1, y = y1, o = (w / 2) | 0;
    g.fillStyle = c;
    for (var guard = 0; guard < 600; guard++) {
      g.fillRect(x - o, y - o, w, w);
      if (x === x2 && y === y2) { break; }
      var e2 = 2 * err; if (e2 > -dy) { err -= dy; x += sx; } if (e2 < dx) { err += dx; y += sy; }
    }
  }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function hexToRgb(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  function mix(h1, h2, t) {
    var a = hexToRgb(h1), b = hexToRgb(h2);
    return "#" + [0, 1, 2].map(function (i) { return ("0" + Math.round(a[i] + (b[i] - a[i]) * t).toString(16)).slice(-2); }).join("");
  }
  function hash(a, b, c) { var n = (a * 73856093) ^ (b * 19349663) ^ (c * 83492791); n = (n ^ (n >>> 13)) * 1274126177; return ((n ^ (n >>> 16)) >>> 0) % 1000; }

  /* ---------- sprites: the art arrives as data (js/desk-sprites.js) and is baked to small canvases once ---------- */
  // A layer's pixels: one character per pixel (0-9a-z = palette index, "." = clear), row after row, with runs
  // written as the character followed by its length in capital letters (base 26, A = 0).
  function bake(layer, pal) {
    var c = document.createElement("canvas"); c.width = layer.w; c.height = layer.h;
    var k = c.getContext("2d"), img = k.createImageData(layer.w, layer.h), d = img.data, s = layer.d, i = 0, at = 0;
    while (i < s.length) {
      var code = s.charCodeAt(i++), n = 0, counted = false;
      while (i < s.length) { var u = s.charCodeAt(i); if (u < 65 || u > 90) { break; } n = n * 26 + (u - 65); counted = true; i++; }
      if (!counted) { n = 1; }
      if (code !== 46) {
        var rgb = hexToRgb(pal[code < 58 ? code - 48 : code - 87]);
        for (var q = 0; q < n; q++) { var j = (at + q) * 4; d[j] = rgb[0]; d[j + 1] = rgb[1]; d[j + 2] = rgb[2]; d[j + 3] = 255; }
      }
      at += n;
    }
    k.putImageData(img, 0, 0);
    return { c: c, x: layer.x, y: layer.y, w: layer.w, h: layer.h };
  }
  function blit(s, ox, oy) { g.drawImage(s.c, (ox + s.x) | 0, (oy + s.y) | 0); }
  function blitFlip(s, ox, oy) { g.save(); g.translate(((ox + s.x) | 0) + s.w, (oy + s.y) | 0); g.scale(-1, 1); g.drawImage(s.c, 0, 0); g.restore(); }
  function pixels(list, ox, oy, pal) { for (var i = 0; i < list.length; i += 3) { if (list[i + 2] >= 0) { px(ox + list[i], oy + list[i + 1], pal[list[i + 2]]); } } }

  /* ---------- 3x5 pixel font ---------- */
  var FONT = {
    A: "010101111101101", B: "110101110101110", C: "011100100100011", D: "110101101101110", E: "111100110100111", F: "111100110100100",
    G: "011100101101011", H: "101101111101101", I: "111010010010111", J: "001001001101010", K: "101101110101101", L: "100100100100111",
    M: "101111111101101", N: "110101101101101", O: "010101101101010", P: "110101110100100", Q: "010101101110011", R: "110101110101101",
    S: "011100010001110", T: "111010010010010", U: "101101101101111", V: "101101101101010", W: "101101111111101", X: "101101010101101",
    Y: "101101010010010", Z: "111001010100111", " ": "000000000000000"
  };
  function textWidth(s) { return s.length * 4 - 1; }
  function drawText(s, x, y, c) {
    s = String(s).toUpperCase();
    for (var i = 0; i < s.length; i++) { var bits = FONT[s[i]] || FONT[" "]; for (var j = 0; j < 15; j++) { if (bits[j] === "1") { px(x + i * 4 + (j % 3), y + ((j / 3) | 0), c); } } }
  }

  /* ---------- time of day ---------- */
  var hourOverride = null;
  function hourNow() { if (hourOverride !== null) { return hourOverride; } var d = new Date(); return d.getHours() + d.getMinutes() / 60; }
  function skyFor(h) {
    function pick(h) {
      if (h < 5 || h >= 21) { return [C.skyNight, C.skyNight2]; } if (h < 7) { return [C.skyDawn1, C.skyDawn2]; }
      if (h < 17.5) { return [C.skyDay1, C.skyDay2]; } if (h < 20) { return [C.skyDusk1, C.skyDusk2]; } return [C.skyNight, C.skyNight2];
    }
    var bounds = [5, 7, 17.5, 20, 21];
    for (var i = 0; i < bounds.length; i++) { var b = bounds[i]; if (Math.abs(h - b) < 0.5) { var t = h - (b - 0.5), a = pick(b - 0.6), z = pick(b + 0.6); return [mix(a[0], z[0], t), mix(a[1], z[1], t)]; } }
    return pick(h);
  }
  function isDark(h) { return h < 6.5 || h >= 18.5; }
  // How much of the night look applies (0 by day, 1 at night) and how much of the low warm sun (around sunrise and sunset).
  function nightAmount(h) { if (h >= 20.5 || h < 5) { return 1; } if (h >= 7 && h < 18) { return 0; } return h >= 18 ? (h - 18) / 2.5 : 1 - (h - 5) / 2; }
  function duskAmount(h) { return Math.max(0, 1 - Math.abs(h - 18.8) / 1.7, 1 - Math.abs(h - 6.2) / 1.2); }

  /* ---------- the room: ceiling, wall, poster, clock, pendant ---------- */
  var NU = ["wwwww.ww.ww", "ww.ww.ww.ww", "ww.ww.ww.ww", "ww.ww.ww.ww", "ww.ww.wwwww"];
  function drawPoster(P) {
    rect(P.x + 2, P.y + 3, P.w, P.h, "rgba(0,0,0,0.20)");                                        // drop shadow
    rect(P.x, P.y, P.w, P.h, C.ink); rect(P.x + 3, P.y + 3, P.w - 6, P.h - 6, "#f4f2ec");
    var mx = P.x + ((P.w - 22) / 2 | 0), my = P.y + (P.h > 55 ? 13 : 9);
    for (var r = 0; r < NU.length; r++) { for (var i = 0; i < NU[r].length; i++) { if (NU[r][i] === "w") { rect(mx + i * 2, my + r * 2, 2, 2, C.ink); } } }
    hline(P.x + 9, my + 16, P.w - 18, C.ink);
    drawText("NUTRIMATIC", P.x + ((P.w - 39) / 2 | 0), my + 22, C.ink);
    hline(P.x + ((P.w - 18) / 2 | 0), my + 31, 18, C.greyLight);
  }
  function drawClock(cx, cy, h) {
    rect(cx - 7, cy - 6, 17, 17, "rgba(0,0,0,0.18)");
    rect(cx - 8, cy - 8, 17, 17, "#f6f4ee"); outline(cx - 8, cy - 8, 17, 17, C.ink);
    px(cx, cy - 6, C.ink); px(cx, cy + 6, C.ink); px(cx - 6, cy, C.ink); px(cx + 6, cy, C.ink);
    var hr = (h % 12) / 12 * Math.PI * 2, mn = (h % 1) * Math.PI * 2;
    for (var i = 1; i <= 3; i++) { px(cx + Math.round(Math.sin(hr) * i), cy - Math.round(Math.cos(hr) * i), C.ink); }
    for (var j = 1; j <= 5; j++) { px(cx + Math.round(Math.sin(mn) * j), cy - Math.round(Math.cos(mn) * j), C.red); }
    px(cx, cy, C.ink);
  }
  function wallColours(h) {
    var n = nightAmount(h), d = duskAmount(h) * (1 - n * 0.6);
    var a = mix(mix(C.wall, C.wallDusk, 0.2 * d), C.wallNight, 0.62 * n), b = mix(mix(C.wallD, C.wallDusk, 0.24 * d), "#141830", 0.66 * n);
    return [a, b];
  }
  function drawRoom(h) {
    var wc = wallColours(h), band = Math.ceil((DESK_Y - CEIL) / 6);
    for (var i = 0; i < 6; i++) { rect(0, CEIL + i * band, W, band, mix(wc[0], wc[1], i / 5)); }
    rect(0, 0, W, CEIL - 2, C.ceil); hline(0, CEIL - 2, W, C.ceilL); hline(0, CEIL - 1, W, mix(C.ceilL, wc[0], 0.5));
    hline(0, DESK_Y - 22, W, mix(wc[1], C.rail, 0.5)); hline(0, DESK_Y - 21, W, mix(wc[0], C.white, 0.25));   // chair rail
    rect(0, DESK_Y - 8, W, 8, mix(wc[1], "#000000", 0.22));
    drawPoster(L.poster); drawClock(L.clock.x, L.clock.y, h);
  }
  function drawPendant(on) {
    var x = L.pendant;
    vline(x, CEIL - 2, 16, C.cord); vline(x + 1, CEIL - 2, 16, C.ink3);
    for (var r = 0; r < 8; r++) { hline(x - 3 - r, 20 + r, 8 + r * 2, C.pendant); }
    hline(x - 11, 28, 24, "#0e0e10");
    hline(x - 9, 27, 20, on ? C.pendantIn : C.pendantOff); rect(x - 2, 29, 6, 2, on ? C.bulb : C.grey);
    px(x - 7, 22, C.ink3); px(x - 6, 23, C.ink3);
  }

  /* ---------- the generated room (assets/desk): Mondrian's Victory Boogie Woogie where the poster was; the clock's hands ---------- */
  function applyArt() { if (layoutName) { WIN = ENV.ready ? L.art.win : L.win; makeStars(); } }
  // The ceiling lights (to-do T15; T41: "hang the pendant light a little higher, add more pendants for a total of 4"):
  // four generated pendants across the ceiling, clear of the painting, the clock and the window, their shades' rims at
  // row PENDANT_RIM where the night's light pools start; lit after dark, their insides cool grey by day.
  var PENDANT_RIM = 25;
  function drawPendantArt(dark) {
    var im = ENV.img[dark ? "pendant-on" : "pendant-off"]; if (!im) { return; }
    L.art.pendants.forEach(function (x) { g.drawImage(im, Math.round(x - im.width / 2), PENDANT_RIM - im.height); });
  }
  function drawClockArt(h) {
    var K = L.art.clock, cx = K.x, cy = K.y, r = K.r - 1;
    for (var dy = -r; dy <= r; dy++) { var half = Math.floor(Math.sqrt(r * r - dy * dy)); hline(cx - half, cy + dy, half * 2 + 1, "#f6f4ee"); }
    px(cx, cy - r + 1, C.ink); px(cx, cy + r - 1, C.ink); px(cx - r + 1, cy, C.ink); px(cx + r - 1, cy, C.ink);
    var hr = (h % 12) / 12 * Math.PI * 2, mn = (h % 1) * Math.PI * 2;
    for (var i = 1; i <= 3; i++) { px(cx + Math.round(Math.sin(hr) * i), cy - Math.round(Math.cos(hr) * i), C.ink); }
    for (var j = 1; j <= r - 1; j++) { px(cx + Math.round(Math.sin(mn) * j), cy - Math.round(Math.cos(mn) * j), C.red); }
    px(cx, cy, C.ink);
  }
  // Midtown through the window: the generated skyline by day, its lit-up twin by night (crossfaded at dusk), and the
  // red aircraft lights on the tallest tops, blinking (Empire State, Chrysler, One Vanderbilt and two more; in the
  // skyline picture's own pixels).
  var AIRCRAFT = [[16, 36], [80, 33], [94, 24], [123, 38], [110, 47]];
  function drawSkylineArt(h, f) {
    var A = L.art, n = clamp(nightAmount(h) * 1.25, 0, 1);
    g.save(); g.beginPath(); g.rect(WIN.x, WIN.y, WIN.w, WIN.h); g.clip();
    if (n < 1) { g.drawImage(ENV.img["sky-day"], A.sky.x, A.sky.y); }
    if (n > 0) { g.globalAlpha = n; g.drawImage(ENV.img["sky-night"], A.sky.x, A.sky.y); g.globalAlpha = 1; }
    if (n > 0.4 && (f % 18) < 9) { for (var i = 0; i < AIRCRAFT.length; i++) { px(A.sky.x + AIRCRAFT[i][0], A.sky.y + AIRCRAFT[i][1], C.beacon); } }
    g.restore();
  }
  // The anglepoise lamps stand on the desk at the outer sides, heads over each one's work: Cole's red on his left,
  // Ilinca's white (the same lamp, mirrored) on her right. On when it is dark, or when the owner solders or writes.
  // The picture is 43x47: base centred at x 9.5, the inside of the shade at (34..36, 10..13), its mouth at (39, 14).
  var BULB = [[36, 10], [35, 11], [36, 11], [35, 12], [36, 12], [34, 13], [35, 13], [36, 13]];
  function lampGeom(i) { var bx = L.art.lamps[i], flip = i === 1; return { x: flip ? bx - 33 : bx - 9, y: DESK_Y - 43, mx: flip ? bx - 30 : bx + 30, my: DESK_Y - 29, flip: flip }; }
  function lampIsOn(i, h) { var p = people[i]; return !p.hidden && (isDark(h) || p.activity === "solder" || p.activity === "write" || solderPaused(p)); }
  // T84/T67 (round-31 audit): his hands off the board for a moment (the spark's start and facepalm, a wave hello from
  // soldering): the lamp stays on and the tools rest on the bench (restingIron, restingPick); at night its beam keeps off him
  function solderPaused(p) { return p === cole && (!!p.benchFrom || (p.react === "greet" && p.greetAct === "solder")); }
  function handsOffWork(p) { return p.activity === "startle" || p.activity === "facepalm" || (p.activity === "wave" && p.react === "greet" && p.greetAct === "solder"); }
  function slantCone(q, strength, overlay, w1) {
    var y0 = q.my, y1 = DESK_FRONT + 3, x1 = q.mx + (q.flip ? -24 : 24);
    if (overlay) { g.save(); g.globalCompositeOperation = "overlay"; }
    for (var y = y0; y < y1; y++) {
      var t = (y - y0) / (y1 - y0), cx = Math.round(lerp(q.mx, x1, t)), half = Math.round(lerp(2, w1 || 24, t));
      rect(cx - half, y, half * 2, 1, "rgba(255,214,150," + ((overlay ? 0.9 - t * 0.25 : 1) * strength).toFixed(3) + ")");
    }
    if (overlay) { g.restore(); }
  }
  // The lamps stand behind the figures (part "back": everything above the desk line, drawn before them), their feet on the
  // desk top in front (part "front", after the desk): on a phone the red lamp's shade was drawn over Cole's shoulder, and
  // in any layout over a raised arm (final round-30 audit).
  function drawLampsArt(h, part) {
    for (var i = 0; i < 2; i++) {
      var q = lampGeom(i), im = ENV.img[i === 0 ? "lamp-red" : "lamp-white"], on = lampIsOn(i, h), back = part === "back";
      if (!back && on && !isDark(h)) { g.save(); g.beginPath(); g.rect(0, DESK_Y, W, H - DESK_Y); g.clip(); slantCone(q, 0.10, false, 20); g.restore(); }   // by day a working lamp shows only faintly, on the desk (over his shirt it read as a third arm: T56)
      var cut = L === LAYOUTS.narrow ? q.y + 29 : H;                    // on a phone only the lamps' arms and shades are in the frame: the corner of the red one's foot read as a stray red blob, and her standing mug needs the white one's place (T128)
      g.save(); g.beginPath(); if (back) { g.rect(0, 0, W, Math.min(DESK_Y, cut)); } else { g.rect(0, DESK_Y, W, Math.max(0, cut - DESK_Y)); } g.clip();
      if (q.flip) { g.translate(q.x + im.width, q.y); g.scale(-1, 1); g.drawImage(im, 0, 0); } else { g.drawImage(im, q.x, q.y); }
      g.restore();
      if (back && on) { drawBulb(q); }
    }
  }
  // The bulb pixels not covered by a figure (sampled before the night falls; a bulb behind his shoulder must not glow
  // through him: last round-30 audit)
  function bulbsShowing(h) {
    var out = [], want = C.bulb.toLowerCase();
    for (var k = 0; k < 2; k++) {
      if (!lampIsOn(k, h)) { continue; }
      var q = lampGeom(k);
      for (var i = 0; i < BULB.length; i++) {
        var x = q.flip ? q.x + 42 - BULB[i][0] : q.x + BULB[i][0], y = q.y + BULB[i][1];
        if (x < 0 || y < 0 || x >= W || y >= H) { continue; }
        var d = g.getImageData(x, y, 1, 1).data, hx = "#" + [d[0], d[1], d[2]].map(function (v) { return (v < 16 ? "0" : "") + v.toString(16); }).join("");
        if (hx === want) { out.push([x, y]); }
      }
    }
    return out;
  }
  function drawBulb(q) { for (var k = 0; k < BULB.length; k++) { px(q.flip ? q.x + 42 - BULB[k][0] : q.x + BULB[k][0], q.y + BULB[k][1], C.bulb); } }
  // T84 (round-31 audit, "mask by the figure, not by a row"): while his hands are off the board his lamp's beam at night
  // must not lie across him (over his shirt it read as an arm reaching for the board), and everything else under it stays
  // lit as while he solders (the station, the board, the desk). figMask holds his own pixels as they show in the frame:
  // his figure drawn alone, less what the scene drew over it later (the desk, the station, the bench) and less what his
  // pose holds as a prop (the board in a wave from soldering); drawNightArt puts those pixels back as they were before
  // the lamps' light.
  var figMask = document.createElement("canvas"), figMaskX = figMask.getContext("2d"), beamTmp = document.createElement("canvas"), beamTmpX = beamTmp.getContext("2d");
  var shadeFig = false;
  function figureMask(p, f) {
    figMask.width = W; figMask.height = H;
    var keep = g; g = figMaskX; drawCharacter(p, f); var d = p.drawn;
    if (d) { g.globalCompositeOperation = "destination-out"; Object.keys(d.pose.props || {}).forEach(function (n) { blit(d.pose.props[n], d.o.x, d.o.y + d.jig); }); g.globalCompositeOperation = "source-over"; }
    g = keep;
    var m = figMaskX.getImageData(0, 0, W, H), a = m.data, b = g.getImageData(0, 0, W, H).data;
    for (var i = 0; i < a.length; i += 4) { if (a[i + 3] && (a[i] !== b[i] || a[i + 1] !== b[i + 1] || a[i + 2] !== b[i + 2])) { a[i + 3] = 0; } }
    figMaskX.putImageData(m, 0, 0);
  }

  /* ---------- window with a New York skyline ---------- */
  var stars = [], clouds = [{ x: 0, y: 14, w: 14 }, { x: 30, y: 26, w: 9 }, { x: 52, y: 8, w: 11 }];
  function makeStars() {
    stars = []; var seed = 11; function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
    for (var i = 0; i < 26; i++) { stars.push({ x: 2 + ((rnd() * (WIN.w - 4)) | 0), y: 2 + ((rnd() * (WIN.h - 40)) | 0), p: (rnd() * 20) | 0 }); }
  }
  // Buildings in a 66-wide strip, left to right: x, width, height, kind. Heights from the window bottom.
  var FAR = [[2, 10, 22], [26, 9, 20], [44, 12, 24], [58, 8, 18]];
  var NEAR = [
    [0, 6, 12, "block"], [7, 10, 18, "empire"], [18, 4, 36, "slender"], [23, 8, 14, "block"], [31, 7, 24, "chrysler"],
    [39, 6, 10, "block"], [46, 8, 30, "wtc"], [55, 6, 16, "block"], [62, 5, 9, "block"]
  ];
  function drawBuilding(b, bx, by, dark, f, far) {
    var x = bx + b[0], w = b[1], h = b[2], kind = b[3] || "block", col = far ? (dark ? C.bldgNightFar : C.bldgFar) : (dark ? C.bldgNight : C.bldg);
    var top = by - h;
    if (x + w > bx + WIN.w) { w = bx + WIN.w - x; if (w <= 0) { return; } }
    rect(x, top, w, h, col);
    if (kind === "empire") {        // stepped setbacks and a spire
      rect(x + 1, top - 6, w - 2, 6, col); rect(x + 2, top - 11, w - 4, 5, col); rect(x + 3, top - 16, w - 6, 5, col); vline(x + (w / 2 | 0), top - 22, 6, col);
      if (dark) { rect(x + 3, top - 16, w - 6, 3, C.winLit2); px(x + (w / 2 | 0), top - 22, (f % 12 < 6) ? C.beacon : C.winLit2); }
    } else if (kind === "chrysler") { // the crown: narrowing tiers, lit arches at night
      rect(x + 1, top - 3, w - 2, 3, col); rect(x + 2, top - 6, w - 4, 3, col); vline(x + (w / 2 | 0), top - 11, 5, col);
      if (dark) { px(x + 1, top - 2, C.winLit2); px(x + w - 2, top - 2, C.winLit2); px(x + 2, top - 5, C.winLit2); px(x + w - 3, top - 5, C.winLit2); px(x + (w / 2 | 0), top - 7, C.winLit2); }
    } else if (kind === "wtc") {      // tapering tower, antenna with a beacon
      rect(x + 1, top - 4, w - 2, 4, col); rect(x + 2, top - 8, w - 4, 4, col); vline(x + (w / 2 | 0), top - 16, 8, col);
      if (dark) { px(x + (w / 2 | 0), top - 16, (f % 10 < 5) ? C.beacon : C.winLit2); rect(x + 2, top - 8, w - 4, 1, C.winLit2); }
    } else if (kind === "slender") {  // 432 Park: a thin grid
      if (dark) { for (var yy = top + 2; yy < by - 1; yy += 3) { if (hash(x, yy, f >> 6) % 3) { px(x + 1, yy, C.winLit); } if (hash(x + 2, yy, f >> 6) % 3) { px(x + 2, yy, C.winLit); } } }
      else { for (var y2 = top + 2; y2 < by - 1; y2 += 3) { hline(x, y2, w, mix(col, C.white, 0.18)); } }
      return;
    }
    if (!far) {
      if (dark) { for (var wy = top + 2; wy < by - 1; wy += 2) { for (var wx = x + 1; wx < x + w - 1; wx += 2) { if (hash(wx, wy, f >> 5) % 5 < 2) { px(wx, wy, (hash(wx, wy, 3) % 2) ? C.winLit : C.winLit2); } } } }
      else { for (var dy = top + 2; dy < by - 1; dy += 3) { for (var dx = x + 1; dx < x + w - 1; dx += 3) { px(dx, dy, mix(col, C.white, 0.22)); } } }
    }
  }
  function drawWindowView(h, f) {     // the sky and the skyline, inside the frame
    var sky = skyFor(h), bands = 8, dark = isDark(h);
    for (var i = 0; i < bands; i++) { rect(WIN.x, WIN.y + Math.round(i * WIN.h / bands), WIN.w, Math.ceil(WIN.h / bands) + 1, mix(sky[0], sky[1], i / (bands - 1))); }
    rect(WIN.x, WIN.y + WIN.h, WIN.w, 2, mix(sky[0], sky[1], 1));
    if (dark) {
      for (var s = 0; s < stars.length; s++) { var st = stars[s]; if (((f >> 3) + st.p) % 7 !== 0) { px(WIN.x + st.x, WIN.y + st.y, C.star); } }
      var mx = WIN.x + 8 + Math.round(((h + 3) % 24) / 24 * (WIN.w - 22)), my = WIN.y + 8;
      rect(mx, my, 6, 6, C.moon); px(mx, my, sky[0]); px(mx + 5, my, sky[0]); px(mx, my + 5, sky[0]); px(mx + 5, my + 5, sky[0]); rect(mx + 3, my + 1, 3, 3, mix(C.moon, sky[0], 0.35));
    } else {
      var sx = WIN.x + 4 + Math.round(Math.min(1, Math.max(0, (h - 6) / 13)) * (WIN.w - 14)), sy = WIN.y + 5 + Math.round(Math.abs((h - 12.5) / 6.5) * 20);
      rect(sx, sy, 6, 6, C.sun); px(sx, sy, sky[0]); px(sx + 5, sy, sky[0]); px(sx, sy + 5, sky[0]); px(sx + 5, sy + 5, sky[0]);
      for (var c = 0; c < clouds.length; c++) {                            // a cloud drifting in or out passes behind the frame: cut, not shrunk, and no piece under four pixels (a stub read as a speck)
        var cl = clouds[c], fx = WIN.x + ((cl.x + (still ? 0 : f) / 20) % (WIN.w + cl.w)) - cl.w;
        [[1, cl.w - 2, C.cloud], [0, cl.w, C.cloud], [0, cl.w, C.cloudS]].forEach(function (r, k) { var x0 = Math.max(WIN.x, Math.round(fx) + r[0]), x1 = Math.min(WIN.x + WIN.w - 1, Math.round(fx) + r[0] + r[1] - 1); if (x1 - x0 >= 3) { hline(x0, WIN.y + cl.y + k, x1 - x0 + 1, r[2]); } });
      }
    }
    if (ENV.ready) { drawSkylineArt(h, f); return; }
    var by = WIN.y + WIN.h - 4;
    for (var a = 0; a < FAR.length; a++) { drawBuilding(FAR[a], WIN.x, by - 2, dark, f, true); }
    for (var b = 0; b < NEAR.length; b++) { drawBuilding(NEAR[b], WIN.x, by, dark, f, false); }
    rect(WIN.x, by, WIN.w, 4, dark ? "#06071a" : mix(sky[1], "#3a4252", 0.7));                 // the river line
    if (dark) { for (var r = 0; r < WIN.w; r += 4) { if (hash(r, 1, f >> 4) % 3 === 0) { px(WIN.x + r + 1, by + 1, mix(C.winLit, "#06071a", 0.5)); } } }
  }
  function drawWindowFrame() {
    rect(WIN.x - 3, WIN.y - 3, WIN.w + 6, 3, C.ink); rect(WIN.x - 3, WIN.y + WIN.h, WIN.w + 6, 3, C.ink); rect(WIN.x - 3, WIN.y, 3, WIN.h, C.ink); rect(WIN.x + WIN.w, WIN.y, 3, WIN.h, C.ink);
    rect(WIN.x + (WIN.w / 2 | 0) - 1, WIN.y, 2, WIN.h, C.ink); rect(WIN.x, WIN.y + (WIN.h * 0.42 | 0), WIN.w, 2, C.ink);
    rect(WIN.x - 6, WIN.y + WIN.h + 3, WIN.w + 12, 3, C.ink2); hline(WIN.x - 6, WIN.y + WIN.h + 3, WIN.w + 12, C.ink3);
    rect(WIN.x - 5, WIN.y + WIN.h + 6, WIN.w + 10, 2, "rgba(0,0,0,0.16)");
  }
  function drawWindow(h, f) { drawWindowView(h, f); drawWindowFrame(); }
  function sillY() { return WIN.y + WIN.h + 3; }

  function drawDesk() {
    rect(0, DESK_Y, W, DESK_DEEP + 5, C.deskTop); hline(0, DESK_Y, W, C.deskTopD); hline(0, DESK_FRONT, W, C.deskTopL); hline(0, DESK_FRONT + 4, W, C.deskTopD);
    rect(0, DESK_FRONT + 5, W, H - DESK_FRONT - 5, C.deskFront); hline(0, DESK_FRONT + 5, W, C.deskFrontD);
    for (var x = 30; x < W; x += 74) { vline(x, DESK_FRONT + 7, H - DESK_FRONT - 7, C.deskFrontD); }
  }
  var PLATE_DX = 13;
  function drawNamePlate(p) {
    // On the drawer front, both plates by one rule: centred PLATE_DX right of the owner's middle. Maker lying to be petted
    // hangs her tail over a plate centred on Ilinca (her tail's swing reaches 4 px right of its root at the plate's rows)
    // and her paw over the edge comes within a pixel of one centred on Cole; 13 px right keeps both 2 clear px from them in
    // either visit and layout, and the plates never move.
    var name = p.name === "cole" ? "COLE" : "ILINCA", w = textWidth(name) + 9, x = p.x + PLATE_DX - (w / 2 | 0), y = DESK_FRONT + 8;
    rect(x + 1, y + 2, w, 9, "rgba(0,0,0,0.3)"); rect(x, y, w, 9, C.plate); hline(x, y + 8, w, C.plateS); vline(x + w - 1, y + 1, 8, C.plateS);
    drawText(name, x + 5, y + 2, C.ink);
  }

  /* ---------- the lamp: articulated, swings over whoever is working ---------- */
  var LAMP_JOINT = 44;
  var lamp = { base: 176, hx: 184, hy: 52, tx: 184, ty: 52, on: false };
  function lampIdle() { return { x: lamp.base + 9, y: 52 }; }
  function updateLamp(h) {
    var work = null;
    if (cole.activity === "solder") { work = { x: cole.x + 26, y: DESK_Y - 47 }; }       // from the side, so the shade never hides a face
    else if (ilinca.activity === "write") { work = { x: ilinca.x - 31, y: DESK_Y - 47 }; }
    else if (cole.activity === "write") { work = { x: cole.x + 24, y: DESK_Y - 47 }; }
    var t = work || lampIdle();
    lamp.tx = t.x; lamp.ty = t.y; lamp.on = isDark(h) || !!work;
    lamp.hx += (lamp.tx - lamp.hx) * 0.18; lamp.hy += (lamp.ty - lamp.hy) * 0.18;
  }
  function drawLampCone() {
    if (!lamp.on) { return; }
    var hx = Math.round(lamp.hx), hy = Math.round(lamp.hy), top = hy + 9, bottom = DESK_FRONT + 3;
    for (var y = top; y < bottom; y++) { var t = (y - top) / (bottom - top), half = Math.round(lerp(9, 26, t)); rect(hx - half, y, half * 2, 1, "rgba(255,214,120,0.20)"); }
    rect(hx - 30, DESK_Y, 60, DESK_DEEP + 3, "rgba(255,224,150,0.16)");
  }
  // Base and arm sit behind the figures (drawn before them); the head hangs in front (drawn after the props).
  function drawLampArm() {
    var bx = lamp.base, hx = Math.round(lamp.hx), hy = Math.round(lamp.hy), jy = LAMP_JOINT;
    limb(bx, DESK_Y - 5, bx, jy, 3, C.lampBody);
    limb(bx, jy, hx, hy, 3, C.lampBody);
    rect(bx - 2, jy - 2, 5, 5, C.lampBody); px(bx, jy, C.ink3);
  }
  function drawLampBase() { var bx = lamp.base; rect(bx - 8, DESK_Y - 4, 17, 4, C.lampBody); hline(bx - 7, DESK_Y - 5, 15, C.lampBody); hline(bx - 6, DESK_Y - 4, 13, C.ink3); }
  function drawLamp() {
    var hx = Math.round(lamp.hx), hy = Math.round(lamp.hy);
    rect(hx - 2, hy - 2, 5, 5, C.lampBody);
    var sh = lamp.on ? C.lampShadeOn : C.lampShade;
    for (var r = 0; r < 8; r++) { hline(hx - 5 - r, hy + r, 10 + r * 2, sh); px(hx - 6 - r, hy + r, C.lampBody); px(hx + 5 + r, hy + r, C.lampBody); }
    for (var k = 0; k < 6; k++) { px(hx - 4 + k, hy + 1 + k, mix(sh, C.white, 0.5)); }
    hline(hx - 5, hy - 1, 10, C.lampBody); hline(hx - 13, hy + 8, 27, C.lampBody);
    if (lamp.on) { hline(hx - 10, hy + 9, 21, C.bulb); }
  }

  /* ---------- props ---------- */
  function propVase(x, kind) {
    rect(x - 4, DESK_Y - 14, 9, 14, C.white); outline(x - 4, DESK_Y - 14, 9, 14, C.ink); hline(x - 5, DESK_Y - 15, 11, C.ink); hline(x - 2, DESK_Y - 9, 5, C.greyLight); vline(x + 2, DESK_Y - 12, 9, C.greyLight);
    vline(x, DESK_Y - 28, 13, C.stem); vline(x - 4, DESK_Y - 24, 9, C.stem); vline(x + 4, DESK_Y - 26, 11, C.stem);
    var p = kind === 0 ? C.petalR : kind === 1 ? C.petalW : C.petalY, ctr = kind === 1 ? C.petalY : C.ink;
    rect(x - 3, DESK_Y - 33, 7, 5, p); rect(x - 7, DESK_Y - 28, 5, 4, p); rect(x + 3, DESK_Y - 30, 5, 4, p); px(x, DESK_Y - 31, ctr); px(x - 5, DESK_Y - 26, ctr); px(x + 5, DESK_Y - 28, ctr);
    if (kind === 1) { outline(x - 3, DESK_Y - 33, 7, 5, C.greyLight); }
  }
  function propPlant(x) {
    rect(x - 7, DESK_Y - 10, 14, 10, C.pot); hline(x - 8, DESK_Y - 11, 16, C.potS); vline(x - 6, DESK_Y - 9, 8, C.potS); rect(x + 4, DESK_Y - 9, 2, 8, mix(C.pot, C.white, 0.3));
    rect(x - 8, DESK_Y - 20, 5, 8, C.leaf); rect(x + 4, DESK_Y - 23, 5, 11, C.greenL); rect(x - 3, DESK_Y - 29, 6, 17, C.green); rect(x - 2, DESK_Y - 32, 3, 3, C.greenL);
    px(x - 7, DESK_Y - 21, C.greenL); vline(x, DESK_Y - 27, 12, C.leaf); px(x + 6, DESK_Y - 24, C.leaf);
  }
  function propPapers(x) {
    rect(x - 14, DESK_Y - 5, 28, 5, C.paper); outline(x - 14, DESK_Y - 5, 28, 5, C.paperLine); rect(x - 13, DESK_Y - 9, 27, 4, C.paper); outline(x - 13, DESK_Y - 9, 27, 4, C.paperLine); hline(x - 9, DESK_Y - 7, 14, C.greyLight);
  }
  function propBottle(x, y) {   // the Nutrimatic shaker; bottom at y
    rect(x - 5, y - 26, 11, 26, C.white); outline(x - 5, y - 26, 11, 26, C.ink); rect(x - 4, y - 31, 9, 5, C.red); hline(x - 3, y - 32, 7, C.redDeep); hline(x - 4, y - 27, 9, C.redDeep);
    rect(x - 3, y - 18, 7, 10, C.greyLight); rect(x - 1, y - 15, 3, 2, C.red); px(x, y - 13, C.red); vline(x + 3, y - 24, 4, C.greyLight);
  }
  function propCartridge(x) {
    rect(x - 8, DESK_Y - 16, 17, 16, C.white); outline(x - 8, DESK_Y - 16, 17, 16, C.ink); rect(x - 7, DESK_Y - 20, 15, 4, C.greyLight); outline(x - 7, DESK_Y - 20, 15, 4, C.ink);
    rect(x - 3, DESK_Y - 11, 7, 6, "#c9a36a"); outline(x - 3, DESK_Y - 11, 7, 6, C.ink3); px(x - 1, DESK_Y - 9, C.ink); px(x + 1, DESK_Y - 9, C.ink);
  }
  function propMug(x, y, steam, f) {   // bottom at y
    rect(x - 5, y - 11, 10, 11, C.mug); hline(x - 5, y - 11, 10, C.mugS); vline(x - 5, y - 10, 10, C.mugS); vline(x + 3, y - 10, 9, C.mugL);
    rect(x + 5, y - 9, 2, 6, C.mug); px(x + 7, y - 8, C.mug); px(x + 7, y - 5, C.mug); vline(x + 7, y - 8, 4, C.mugS);
    if (steam) { var k = (f >> 2) % 3; px(x - 2 + k, y - 14, C.smoke2); px(x + 1 - k, y - 17, C.smoke2); px(x - 1 + k, y - 20, C.smoke2); }
  }
  function steam(x, y, f) { var k = (f >> 2) % 3; px(x - 1 + k, y, C.smoke2); px(x + 2 - k, y - 3, C.smoke2); px(x + k, y - 6, C.smoke2); }
  // T128 (Cole, 2026-10-27: "For the moment, we can give them everlasting cups of coffee. They can sit on the table, steaming
  // gently"): each of them has a red mug standing on the desk all the time. It is the mug in his hand (T94: one mug size, the
  // bigger one): 15 x 22 like the mug his coffee pose holds on the desk (outline, dark left side, red, a highlight as in his
  // sip), full of coffee under its rim, its handle 5 px. Where the coffee poses hold it, in front of each of them, the laptop,
  // the paper, the board, the DS and the hands lie in every other activity (T48: his mug had lain where the board goes), so it
  // stands on each one's outer side, by their lamp, on the desk's back row: Cole's left of his elbows, Ilinca's right of hers,
  // 2 clear pixels from every pose either of them takes there (his throw the nearest), from the lamps (moved a little out for
  // it, LAYOUTS), the desk props, her phone and his station and tools. Maker is never further back on the desk than row 137,
  // so she always passes in front of it. Handles outward: his on the left, as in his hand; hers on the right (on her left
  // her elbow leaves no room for it). Hand-drawn maps: k line, f dark red, g red, h highlight, c coffee.
  var MUG_BODY = ['..kkkkkkkkkkk..',
                  '.kgcccccccccgk.',
                  'kgcccccccccccgk',
                  'kgggggggggggggk'];
  while (MUG_BODY.length < 20) { MUG_BODY.push('kfggghggggggggk'); }     // (sixteen rows of its side)
  MUG_BODY.push('.kkgggggggggkk.', '...kkkkkkkkk...');
  var MUG_HANDLE = ['.kkkk', 'kgggg', 'kgkkk', 'kgk..', 'kgkkk', 'kgggg', '.kkkk'];   // its rows 3-9, drawn on his left (mirrored on her right; T128 follow-up: rows 3-9, so 4 rows into the desk it keeps 2 px from the lamps' feet)
  var MUG_COL = { k: C.line, f: C.mugS, g: C.mug, h: "#ff5a72", c: "#3b2012" };   // (the held mug's own colours; her outline her own near-black)
  // (T128 follow-up, Cole: "nudged slightly down (forward) on the desk": its bottom row 138, 4 rows into the desk top)
  var MUG_DX = { cole: -73, ilinca: 45 }, MUG_Y = DESK_Y + 4;          // its body's left column from their middle, its bottom row
  var MUG_HELD = { sip: 1, mug: 1, mugWave: 1, carry: 1, coffeeSip: 1 };   // poses with the mug in the hand: then none stands on the desk
  // (the coffee frames: lifted, the mug is in the hand; held on the desk, the pose draws it where it stands and the scene only
  // its steam; reaching, the scene draws it)
  function mugHeld(n) { return !!MUG_HELD[n] || /^coffeeLift/.test(n || ""); }
  // The steam: a dash of three pixels rising a row a frame over the mug's outer side and fading (a, b, c: three strengths),
  // six frames of a quarter second, the two mugs half a loop apart; never while it is held. Clear of the lamps' shades above
  // (rows 7 to 1 over the rim, the outer three columns inside it). Rows top to bottom, columns from the outside in. It is laid
  // on last, after the night's dimming and the lamps' light, where nothing has been drawn over it since the mugs (Maker
  // passing in front), as the bulbs are (steamShown), each pixel STEAM_D levels from the lit wall pixel behind it: darker
  // and a little cooler (blue taken down less) where the wall behind the wisp is pale (its middle brightness: the brick by
  // day and at dawn and dusk), lighter where it is darker (night), one way for the whole wisp so it never mixes light and
  // dark pixels (audit of 6e92bba: a day colour dimmed and a night white on top had cancelled out at dawn and dusk).
  var STEAM = [['c..', 'c..', '.b.', '...', '...', '...', '..a'],     // (drifting outward as it rises, 2 px clear of the shades)
               ['c..', 'c..', '...', '...', '...', '..a', '..a'],
               ['c..', '...', '...', '...', '.a.', '..a', '..a'],
               ['...', '...', '...', '.b.', '.a.', '..a', '...'],
               ['...', '...', '.b.', '.b.', '.a.', '...', '...'],
               ['...', 'c..', '.b.', '.b.', '...', '...', '...']];
  var STEAM_D = { a: 30, b: 20, c: 12 }, STEAM_COOL = [1, 0.95, 0.7], steamShown = [], steamBox = {};
  function mugStands(p) { return !mugHeld(p.drawn && p.drawn.name); }
  function drawStandingMug(p, f) {
    if (!mugStands(p)) { return; }                                     // at the lips: the one mug is in the hand, and no steam
    var x0 = p.x + MUG_DX[p.name], top = MUG_Y - MUG_BODY.length + 1, out = p === cole ? -1 : 1, i, j, col = function (k) { return k === "k" && p === ilinca ? "#0b0503" : MUG_COL[k]; };   // out: the side its handle and steam are on
    if (!(p.drawn && p.drawn.name === "coffeeHold")) {                // (held on the desk the pose draws it)
      for (j = 0; j < MUG_BODY.length; j++) { for (i = 0; i < MUG_BODY[j].length; i++) { var c = col(MUG_BODY[j][i]); if (c) { px(x0 + i, top + j, c); } } }
      for (j = 0; j < MUG_HANDLE.length; j++) { for (i = 0; i < 5; i++) { var ch = col(MUG_HANDLE[j][out < 0 ? i : 4 - i]); if (ch) { px(out < 0 ? x0 - 5 + i : x0 + 15 + i, top + 3 + j, ch); } } }
    }
    var fr = STEAM[(Math.floor(f / 3) + (p === cole ? 0 : 3)) % STEAM.length], sx = out < 0 ? x0 + 1 : x0 + 12;   // (r33-live: his a pixel further out: 2 clear px from his lamp's shade at 35)
    for (j = 0; j < fr.length; j++) { for (i = 0; i < 3; i++) { if (fr[j][i] !== ".") { steamShown.push([sx - out * i, top - fr.length + j, fr[j][i], null, p.name]); } } }   // (drawn last: steamDraw)
    steamBox[p.name] = [out < 0 ? sx : sx - 2, top - fr.length];       // (the wisp's 3 x 7 box)
  }
  // (T128 follow-up: the mug 4 rows into the desk top; Maker comes no further back than row 137, at a laptop: there, near the
  // mug, she is behind it, and it is drawn after her)
  function catBehindMug(p) { var c = actors.cat; return !!c && c.y < MUG_Y && Math.abs(c.x - (p.x + MUG_DX[p.name] + 7)) < 50; }
  function rgbAt(x, y) { var d = g.getImageData(x, y, 1, 1).data; return d[0] + "," + d[1] + "," + d[2]; }
  // (which steam pixels nothing has been drawn over since the mugs, and each one's colour from the finished pixel behind it)
  function steamMark() { steamShown.forEach(function (s) { if (s[3] === null) { s[3] = rgbAt(s[0], s[1]); } }); }
  function steamKept() { steamShown = steamShown.filter(function (s) { return rgbAt(s[0], s[1]) === s[3]; }); }
  function steamDraw() {
    var pale = {};
    Object.keys(steamBox).forEach(function (n) {                       // the wall behind each wisp: its middle brightness (the mortar lines are few)
      var b = steamBox[n], d = g.getImageData(b[0], b[1], 3, 7).data, ls = [];
      for (var k = 0; k < d.length; k += 4) { ls.push(luma([d[k], d[k + 1], d[k + 2]])); }
      ls.sort(function (u, v) { return u - v; }); pale[n] = ls[ls.length >> 1] > 170;
    });
    steamShown.forEach(function (s) {
      var d = g.getImageData(s[0], s[1], 1, 1).data, k = STEAM_D[s[2]], dn = pale[s[4]];
      px(s[0], s[1], "rgb(" + [0, 1, 2].map(function (i) { return clamp(Math.round(d[i] + (dn ? -k * STEAM_COOL[i] : k)), 0, 255); }).join(",") + ")");
    });
  }
  // Fourth spark rework (T67/T84, audit of 99c05d7; "Eliminating object clipping is essential"): the station's T holder is gone.
  // The iron no longer goes in it (held while soldering, laid on the desk in the spark and the wave), and it stood exactly
  // where his arms go: in facepalm its crossbar lay on his lap hand's outline and its stem ran down the hand's side leaving
  // a pixel of skin; in the start the same sliver; in a wave its crossbar covered his raised elbow's outline. No other spot
  // on or beside the station is clear of him (while soldering his forearm lies over the whole box top and his elbow just
  // left of it). The box now says what it is by its face: a round temperature knob, the heater's red light and a dark
  // readout lit in the iron tip's orange; drawn inside the box, so it never meets him. k ink, r red light, o readout.
  // Fifth rework (audit of 658787a, "an odd white spot"): the knob was silver with a white highlight, the brightest pixel on
  // the box, a light dot at display size. It is a mid grey (b), a faint lighter top edge (a) and a darker lower rim (c): a
  // round knob lit from above, no brighter than the readout.
  var STATION_FACE = ['..................',
                      '..aaa......kkkkkk.',
                      '.abbbc..r..kookok.',
                      '.bbbbc.....kookok.',
                      '..ccc......kkkkkk.',
                      '..................'];
  // Fifth rework (audit of 658787a, "no skin slivers"): the box stands in front of him, and where one of his lines runs
  // diagonally into its edge the skin beside it narrows to a 1 px wedge: in facepalm above the box (his lap hand's crease
  // at row 128, the box at row 130, a row of skin 2 px long between), while soldering at its left edge (his forearm's lower
  // outline, 1 px of skin, the box). Those pixels close the wedge; his hands are not redrawn. Pose pixels (figure
  // coordinates) and the colour each takes: k his line, b his crease brown (both his own palette's).
  // Sixth rework (audit of 3176b99): in facepalm both pixels in line colour made a 2x2 black foot where his crease steps
  // diagonally (rows 127-129: 93-94, 94-95, 96); now its last step is (95, 129) in line colour, so it keeps stepping
  // (95-96 on row 129), and (94, 129) beside it takes his crease's brown, as the crease starts in brown on row 127. The seal
  // is drawn with his figure (drawSeal, from drawCharacter), not with the station: at night under the lamp it then keeps
  // his lighting (figureMask) instead of the station's (a lit bump on the box's top). And each pixel is drawn only where
  // it is needed: right against the box's top or left edge, where his pose shows skin with one of his lines just beyond
  // it, so a later redraw of the hands that moves the line leaves no stray line pixel (the checker then shows the sliver).
  // T48 (round-31 integration): the DS scene keeps the bench (scenario.bench), so its poses meet the box too: 'hide' (his
  // hands in his lap when she catches him) is the arm facepalm took its lap arm from, the same two pixels; in the DS poses his
  // left forearm's outline comes down past the box's top right corner with one pixel of skin shade left in the corner
  // (15, 83), which takes his line colour, so his skin ends at the box's corner (the corner case in drawSeal).
  // (Round-31 integration audit: in the DS poses his left forearm's outline also comes down to the box's top two pixels short
  // of its corner, leaving a wedge of skin two pixels deep, (-2, 82-83): the crease brown and his line close it, both or
  // neither, by the guard's two-deep case.)
  var SEAL_SOLDER = [[-6, 85, "k"]], SEAL_LAP = [[7, 83, "b"], [8, 83, "k"]], SEAL_DS = [[15, 83, "k"], [-2, 82, "b"], [-2, 83, "k"]];
  // (r33-live: the handheld D1 has its forearm's skin run across the box's top with its own outline; the box's outline is the
  // line there, and SEAL_DS would paint a line and a crease onto that skin: not used, kept for the old DS poses)
  var STATION_SEAL = { facepalm: SEAL_LAP, solder: SEAL_SOLDER, solder1: SEAL_SOLDER, solderR: SEAL_SOLDER, solderR1: SEAL_SOLDER, solderL: SEAL_SOLDER, solderL1: SEAL_SOLDER,
                       hide: SEAL_LAP };
  // (round-31 integration audit: greeting from soldering his activity reads "wave"; the scenes that must not start while he
  // solders ask this instead)
  function soldering() { return cole.activity === "solder" || !!cole.benchFrom || (!!cole.react && cole.greetAct === "solder"); }
  function stationShows() { return (cole.activity === "solder" || cole.benchFrom || (cole.react && cole.greetAct === "solder")) && !cole.hidden; }
  function stationX() { return ENV.ready ? cole.x - 32 : cole.x - 50; }
  function stationBox() { var x = stationX(), b = deskAt(0.35) + 1; return { x0: x - 10, y0: b - 8, x1: x + 9, y1: b - 1 }; }   // as propSolderStation draws it
  function poseRGB(p, pose, sx, sy) {                                   // the colour his pose shows at a figure pixel (topmost layer), null where clear
    var layers = pose.ownHead ? [[bodyOf(pose), 0]] : [[pose.front, p.headDy || 0], [pose.frontBody, 0], [bodyOf(pose), 0]];
    for (var i = 0; i < layers.length; i++) {
      var s = layers[i][0]; if (!s) { continue; }
      var lx = sx - s.x, ly = sy - layers[i][1] - s.y; if (lx < 0 || ly < 0 || lx >= s.w || ly >= s.h) { continue; }
      if (!s.rgba) { s.rgba = s.c.getContext("2d").getImageData(0, 0, s.w, s.h).data; }
      var j = (ly * s.w + lx) * 4; if (s.rgba[j + 3]) { return [s.rgba[j], s.rgba[j + 1], s.rgba[j + 2]]; }
    }
    return null;
  }
  function luma(c) { return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; }
  function drawSeal(p) {
    var d = p.drawn, seal = p === cole && d && stationShows() && STATION_SEAL[d.name]; if (!seal) { return; }
    var bx = stationBox(), col = { k: C.line, b: C.crease };
    var has = function (ax, ay) { for (var j = 0; j < seal.length; j++) { if (seal[j][0] === ax && seal[j][1] === ay) { return true; } } return false; };
    var skin = function (c) { return !!c && luma(c) >= 120; };
    for (var k = 0; k < seal.length; k++) {
      var sx = seal[k][0], sy = seal[k][1], x = d.o.x + sx, y = d.o.y + d.jig + sy;
      var top = y === bx.y0 - 1 && x >= bx.x0 && x <= bx.x1, left = x === bx.x0 - 1 && y >= bx.y0 && y <= bx.y1, corner = y === bx.y0 - 1 && x === bx.x1 + 1;
      var top2 = y === bx.y0 - 2 && x >= bx.x0 && x <= bx.x1 && has(sx, sy + 1);   // the upper of two skin pixels between his line and the box's top
      if (!top && !left && !corner && !top2) { continue; }               // only right against the box's top or left edge (or diagonally at its top right corner)
      if (UNDER_DESK[d.name] && y >= deskEdge()) { continue; }           // (a pose clipped at the desk's edge: nothing of it below that row)
      var here = poseRGB(p, d.pose, sx, sy), beyond = top ? poseRGB(p, d.pose, sx, sy - 1) : left ? poseRGB(p, d.pose, sx - 1, sy) : poseRGB(p, d.pose, sx + 1, sy);   // (at the corner: his line beside it)
      if (top && skin(beyond) && has(sx, sy - 1)) { beyond = poseRGB(p, d.pose, sx, sy - 2); }   // two deep: his line above the pair, both sealed
      if (top2) { if (!skin(poseRGB(p, d.pose, sx, sy + 1))) { continue; } beyond = poseRGB(p, d.pose, sx, sy - 1); }
      if (!here || !beyond || luma(here) < 120 || luma(beyond) > 80) { continue; }   // skin here, one of his lines beyond it
      px(x, y, seal[k][2] === "k" ? "rgb(" + beyond.join(",") + ")" : col[seal[k][2]]);   // (his line in the colour of that line itself)
    }
  }
  function propSolderStation(x) {
    var b = deskAt(0.35) + 1, col = { a: C.knobL, b: C.knob, c: C.knobD, k: C.ink, o: C.ironHot, r: C.red };   // standing on the desk's top, beside the board
    rect(x - 10, b - 8, 20, 8, C.ink3); outline(x - 10, b - 8, 20, 8, C.ink);
    for (var j = 0; j < STATION_FACE.length; j++) { for (var i = 0; i < STATION_FACE[j].length; i++) { var ch = STATION_FACE[j][i]; if (col[ch]) { px(x - 9 + i, b - 7 + j, col[ch]); } } }
  }
  // T67 (round-31 audit, "the tools never disappear"): what his hands are not holding rests on the bench, at the size it
  // has in his hand (the same blue, silver and yellow). Both while the spark has his hands up, the iron alone while he
  // waves hello from soldering (his other hand keeps the pick): exactly the frames whose pose holds neither or one of them.
  function toolsResting() { var n = cole.drawn && cole.drawn.name; return { iron: !!cole.benchFrom || n === "solderWave", pick: !!cole.benchFrom }; }
  // Third spark rework (T67/T84): anywhere in or on the station a 35 px iron crossed his body (the station stands in front
  // of him, where his arms go when he jumps back: in its holder it lay along the forearm he throws up and through his arm
  // in his lap; in a corner socket its outline met his lap hand's and at night it blended with them), and in a wave hello
  // the holder's crossbar lies on his raised elbow's outline and the whole T is within 3 px of him, so it cannot take the
  // iron there either. When the puff startles him he drops both tools on the desk, and in a wave he lays the iron down at
  // the same place: flat, right of the board, at its size in his hand (35 px: 29 of blue, the grey collar, 5 of silver
  // tip, as in SOLDER_IRON), its tip towards the board and the station. Hand-drawn maps (k ink, e blue, G collar, g silver,
  // c yellow), never rotated art.
  // The desk top is rows 134-142; the iron keeps 2 px of desk from everything in every frame and both layouts: rows 137-140
  // (the board's lower edge is row 135, the front edge row 143, his elbow on the desk in facepalm row 134), its thin tip
  // (rows 138-140) in front of the board's right end, its blue body right of the board, its end 2 px short of the nearest
  // pixel Ilinca puts on the desk on phones (her paper and hands at x 124, rows 134-136). Its tip pulses as in his hand.
  var IRON_FLAT = ['......kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.',
                   '.kkkkkGeeeeeeeeeeeeeeeeeeeeeeeeeeeeek',
                   'kgggggGeeeeeeeeeeeeeeeeeeeeeeeeeeeeek',
                   '.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.'];
  function restingIron(f) {
    if (!toolsResting().iron) { return; }
    var o = origin(cole), x0 = o.x + 48, y0 = DESK_Y + 3, col = { k: C.ink, e: C.ironBlue, G: C.steelS, g: C.steel };
    for (var j = 0; j < IRON_FLAT.length; j++) { for (var i = 0; i < IRON_FLAT[j].length; i++) { var ch = IRON_FLAT[j][i]; if (col[ch]) { px(x0 + i, y0 + j, col[ch]); } } }
    px(x0 + 1, y0 + 2, (f % 6 < 3) ? C.ironHot : C.steel);              // still hot: its tip pulses as it did in his hand
  }
  // Second audit rework (T67, "Object scale must be consistent"): the pick lay on the board at 17 px, 60% of the pick in
  // his hand. In his hand it runs 28 px from the end of its handle to its point, through his fist (sprite (60, 62) to
  // (46, 86)): it lies on the desk in front of the board at that length, yellow handle and steel point (the point towards
  // the station), outlined so it reads against the wood. Third rework: its ends taper like the pick in his hand.
  // Fourth rework (audit of 99c05d7): it had 1 px of desk to the station's corner and one row to the desk's front edge,
  // and at display size its point met the station; it was cut to three rows. Fifth rework (audit of 658787a, "Object scale
  // must be consistent"): three rows made it half as thick as in his hand and a wire beside the iron. It is as thick as in
  // his hand again: a yellow handle 2 rows high (2 px on the slant in his fist) and the 1 px steel point, inside its
  // outline, rows 138-141, 28 px of colour (8 steel, 20 yellow), its handle end slanted. Its point tapers to one pixel
  // (row 140, two columns right of the station's lower right corner, three rows below it), so it keeps 2 px of desk from
  // the station, the board (row 135) and the iron, and one row (142) to the desk's front edge (row 143), the one margin
  // allowed at 1 px.
  var PICK_FLAT = ['.........kkkkkkkkkkkkkkkkkkkk.',
                   '.kkkkkkkkccccccccccccccccccck.',
                   'kggggggggcccccccccccccccccccck',
                   '.kkkkkkkkkkkkkkkkkkkkkkkkkkkk.'];
  function restingPick() {
    if (!toolsResting().pick) { return; }
    var o = origin(cole), x0 = o.x + 16, y0 = DESK_Y + 4, col = { k: C.ink, g: C.steel, c: C.pick };
    for (var j = 0; j < PICK_FLAT.length; j++) { for (var i = 0; i < PICK_FLAT[j].length; i++) { var ch = PICK_FLAT[j][i]; if (col[ch]) { px(x0 + i, y0 + j, col[ch]); } } }
  }

  // Where Ilinca's phone lies when she isn't holding it: on her right, clear of her laptop and her arm, 2 px from her mug's foot
  // (T128; the mug 4 rows into the desk now: the phone 2 px further in) and from her in every pose she takes while it lies there.
  function phoneSpot() { return ilinca.x + 38; }
  function propPhoneOnDesk(x) { var y = deskAt(0.5); rect(x - 5, y - 2, 10, 2, C.phone); hline(x - 4, y - 2, 8, C.phoneTop); }   // face down, its blue back up: the phone in her hand
  // A paper airplane seen from above at a slant, nose in dir (1 = right), its middle at x, y: the near wing white, the
  // far wing in shade, the crease between (T42: the old one read as a paper football; T57: as long as the folded one). The
  // same map as tools/desk/poses.py PLANE.
  var PLANE = ["k.....................", "kkkk..................", "kwwwkkk...............", "kwwwwwwkkk............", "kwwwwwwwwwkkk.........", "kwwwwwwwwwwwwkkk......", "kwwwwwwwwwwwwwwwkkk...", "kkkkkkkkkkkkkkkkkkkkkk", "kgggggggggggggkkkk....", "kgggggggggkkkk........", "kgggggkkkk............", "kgkkkk................", "kk...................."];
  function puff(cx, cy, r, col) {                                       // a round puff of smoke, r pixels across the middle
    for (var dy = -r; dy <= r; dy++) { var half = Math.round(Math.sqrt(r * r - dy * dy + 0.5)); rect(cx - half, cy + dy, half * 2 + 1, 1, col); }
  }
  function propPlane(x, y, dir) {
    var d = dir || 1, cols = { k: "#010101", w: "#fbfaf5", g: "#cfd2d4" };   // the same colours as the plane in his hand
    for (var r = 0; r < PLANE.length; r++) {
      for (var i = 0; i < PLANE[r].length; i++) { var ch = PLANE[r].charAt(i); if (ch !== ".") { px(x + (i - (PLANE[r].length >> 1)) * d, y + r - (PLANE.length >> 1), cols[ch]); } }
    }
  }

  /* ---------- the characters ---------- */
  // A figure is a body in one of its poses (the whole torso with arms, hands and whatever they hold, generated as
  // one picture per pose), the head on top of it, the face frames, and for a few poses a front part that covers the
  // face (a mug at the mouth). Nothing about the arms is drawn in code.
  function makeCharacter(name, o) {
    var a = ART[name], poses = {};
    Object.keys(a.poses || {}).forEach(function (k) {
      var q = a.poses[k], props = {};
      Object.keys(q.p || {}).forEach(function (n) { props[n] = bake(q.p[n], a.pal); });
      poses[k] = { body: bake(q.b, a.pal), bodyN: q.bn ? bake(q.bn, a.pal) : null, front: q.f ? bake(q.f, a.pal) : null, frontBody: q.fb ? bake(q.fb, a.pal) : null, over: q.o ? bake(q.o, a.pal) : null, pts: q.pts || {}, props: props, ownHead: !!q.oh, under: q.u || null };
    });
    if (!poses.rest) { poses.rest = { body: bake(a.torso, a.pal), front: null, pts: {} }; }
    return {
      name: name, art: a, poses: poses, head: bake(a.head, a.pal), headDown: a.down ? bake(a.down.head, a.pal) : null, x: 0, activities: o.activities, restMouth: o.restMouth, headDy: o.headDy, workLook: o.workLook,
      tilt: 0, lookDown: false, exprUntil: 0, nextExprAt: 60 + Math.random() * 120,
      activity: "rest", actUntil: 0, actFrame: 0, look: { x: 0, y: 0 }, lookTarget: { x: 0, y: 0 }, turn: 0, nod: 0, bob: 0, slide: 0, hidden: false,
      mouth: "neutral", brows: null, blink: 0, nextBlink: 20 + Math.random() * 40, talking: false, gesture: false, react: null, reactUntil: 0,
      phoneOnDesk: false, hold: null, drawn: null, laptopOut: false, catLift: null
    };
  }
  // headDy lowers the head on the body (Ilinca's neck read too long).
  var cole = makeCharacter("cole", { restMouth: "neutral", headDy: 0, workLook: { type: [0, 1], write: [0, 1], solder: [0, 1], ds: [0, 1] }, activities: ["type", "solder", "solder", "think", "coffee", "stretch", "rest", "type", "write"].filter(function (a) { return (a !== "write" || SCENE_ON.coleWrite) && (a !== "coffee" || SCENE_ON.coffee); }) });
  var ilinca = makeCharacter("ilinca", { restMouth: "soft", headDy: 3, workLook: { type: [0, 1], write: [-1, 1], phone: [0, 1] }, activities: ["type", "type", "phone", "coffee", "think", "write", "write", "rest"].filter(function (a) { return (a !== "write" || SCENE_ON.ilincaWrite) && (a !== "coffee" || SCENE_ON.coffee); }) });   // no stretch for her (Cole)
  var people = [cole, ilinca];
  function other(p) { return p === cole ? ilinca : cole; }
  function who(n) { return n === "cole" ? cole : ilinca; }
  function midX() { return (cole.x + ilinca.x) / 2 | 0; }

  // Where the figure's sprite sits: its centre column on the character's x, its desk row on the desk top.
  function origin(p) { var a = p.art; return { x: p.x - a.centre + Math.round(p.slide), y: DESK_Y - a.desk + p.bob }; }
  function point(p, name, o) { o = o || origin(p); var q = p.art.points[name]; return { x: o.x + q[0], y: o.y + q[1] + p.headDy }; }
  function eyeY(p) { return point(p, "eye").y; }
  // Round-31 audit of T88 ("arms supposed to be hidden by table ... Line on arms must coincide with edge of desk"): the desk's
  // back edge as the room shows it. The wide room picture draws it as a black line at row 132 with a row of its wood under
  // it (the desk picture starts at row 134); the phone's room has wall down to row 133 and the desk from 134. Hands under
  // the desk (these poses) end exactly there: the pose is clipped at that row, and nothing of it goes on the desk.
  var UNDER_DESK = { hide: 1, petlap: 1, petlap2: 1 };
  // (r33-live: a pose may have its own body for the phone layout, where the desk's back edge is two rows lower: R2's hidden
  // arm runs on to it there and ends at row 85 in the wide room, as the hand round drew it, 'bn')
  function bodyOf(pose) { return L === LAYOUTS.narrow && pose.bodyN ? pose.bodyN : pose.body; }
  // (one desk-edge setting per layout, art.deskEdge, also for his kept sheet's top edge: drawSheetBehind)
  function deskEdge() { return ENV.ready && L.art.deskEdge ? L.art.deskEdge : DESK_Y; }

  // Which pose an activity is drawn with. A pose the art does not have falls back to resting.
  var POSE_OF = {
    rest: "rest", type: "type", write: "write", solder: "solder", think: "think", phone: "phone", call: "call", ds: "ds", dsAway: "hide",
    stretch: "stretch", wave: "wave", highfive: "highfive", fold: "fold", "throw": "throw", shake: "shake", drink: "drink", offer: "offer",
    take: "take", rubEye: "yawn", yawn: "yawn", holdcup: "sip", pet: "pet", fan: "wave", fistpump: "fist", carry: "carry", release: "highfive",
    underdesk: "hide",                                                   // hands down in the lap, out of Maker's way
    setdown: "shake2",                                                   // the shaker held on the desk top, before he lets it go
    startle: "surprise", facepalm: "facepalm"                            // the spark: a start, then a hand to his head (T38)
  };
  // Something always moves (Cole's note 9): each activity has frames of small motion the pose steps through, as
  // [pose, ticks]: forearms typing behind the laptop screen, thumbs on the console, a hand fidgeting, a phone scrolled.
  // A pose a figure doesn't have is skipped. Now and then a hand goes to the trackpad; soldering changes position.
  var MOTION = {
    type: [["type", 4], ["type1", 2], ["type", 3], ["type2", 2], ["type", 2], ["type1", 1], ["type", 2], ["type2", 1], ["type", 1], ["type1", 2]],
    ds: [["ds", 2], ["ds1", 2], ["ds", 1], ["ds2", 2], ["ds", 2], ["ds2", 1], ["ds1", 1], ["ds", 3], ["ds1", 1]],
    rest: [["rest", 40], ["rest1", 12], ["rest", 26], ["rest1", 6]],
    phone: [["phone", 9], ["phone1", 3], ["phone", 5], ["phone1", 2]],
    // T67: every two or three seconds both hands and their tools move a pixel along the board and back, a pixel at a time
    // (solderR right, solderL left; ...1 with his left hand lifted)
    solder: [["solder", 16], ["solder1", 3], ["solder", 11], ["solderR", 14], ["solderR1", 3], ["solderR", 13], ["solder", 12], ["solder1", 2],
             ["solder", 14], ["solderL", 15], ["solderL1", 3], ["solderL", 12]],
    think: [["think", 22], ["think1", 3], ["think", 2], ["think1", 3], ["think", 30], ["think1", 4]],    // T7: fingers drumming on the desk
    call: [["call", 14], ["call1", 6], ["call", 9], ["call1", 4]]
  };
  // T73 ("doesn't appear to move"): her black sleeves read as moving only when a forearm eases in a pixel, then two, and back
  // (type1, type3 the left; type2, typetrack the right), then a smaller twitch of each; 23 ticks against his 20, never in step
  var MOTION_HER = { type: [["type", 4], ["type1", 1], ["type3", 2], ["type1", 1], ["type", 3], ["type2", 1], ["typetrack", 2], ["type2", 1], ["type", 3], ["type1", 1], ["type", 2], ["type2", 2]] };
  function motion(p, name) {
    // (solder2, another way of holding the iron, went: its shoulders and arms were far wider than every other pose, T30)
    var seq = MOTION[name]; if (!seq) { return name; }
    if (name === "type" && p.poses.typetrack && ((p.actFrame + (p.name === "ilinca" ? 31 : 0)) % (p.name === "ilinca" ? 83 : 70)) >= (p.name === "ilinca" ? 71 : 60)) { return "typetrack"; }   // a hand on the trackpad, at their own times (hers held 1 s, not 2: T73)
    if (p.name === "ilinca" && MOTION_HER[name]) { seq = MOTION_HER[name]; }
    var total = 0, i; for (i = 0; i < seq.length; i++) { total += seq[i][1]; }
    var k = (p.actFrame + (p.name === "ilinca" ? 13 : 0)) % total;      // T50: never in step with him (another rhythm, another start)
    for (i = 0; i < seq.length; i++) { if (k < seq[i][1]) { return p.poses[seq[i][0]] ? seq[i][0] : name; } k -= seq[i][1]; }
    return name;
  }
  // Writing: the hand moves along the line in small steps and comes back (write1 and write2 are the write pose with
  // the hand moved one and two pixels on).
  var WRITING = ["write", "write", "write1", "write1", "write2", "write2", "write2", "write1", "write", "write", "write", "write1", "write2", "write", "write", "write"];
  // T128 follow-up (Cole, 2026-10-28: "On coffee drinking, what's missing is the mug in hand on table stage before the drink"):
  // a coffee is one sip, 10 s: the hands at rest, the reach (2 frames each of two), the hand round the mug where it stands
  // (a beat, 1 s), the lift in COFFEE_LIFT steps of at most 4 px for the mug, the sip (14 frames), the same steps down, the
  // mug held on the desk a moment, the hand back, at rest again; a longer coffee repeats it. "SIP" is his 'sip' (M0-R) or
  // her 'coffeeSip'.
  var COFFEE_LIFT = 22, COFFEE_SEQ = (function () {
    var q = [], i, add = function (n, k) { for (var j = 0; j < k; j++) { q.push(n); } };
    add(null, 24); add("coffeeReach1", 2); add("coffeeReach2", 2); add("coffeeHold", 12);
    for (i = 1; i <= COFFEE_LIFT; i++) { add("coffeeLift" + i, 1); }
    add("SIP", 14);
    for (i = COFFEE_LIFT; i >= 1; i--) { add("coffeeLift" + i, 1); }
    add("coffeeHold", 8); add("coffeeReach2", 2); add("coffeeReach1", 2);
    while (q.length < 120) { q.push(null); }
    return q;
  })();
  var SIP_AT = COFFEE_SEQ.indexOf("SIP"), DOWN_AT = SIP_AT + 14, LIFT_AT = COFFEE_SEQ.indexOf("coffeeLift1");
  // Maker passing (holdcup): the mug lifted the same way, from wherever the coffee had got to, and held at the lips
  var HOLDCUP = [24, 24, 26, 26, 28, 28, 28, 28].concat((function () { var q = []; for (var i = LIFT_AT; i <= SIP_AT; i++) { q.push(i); } return q; })());
  function coffeePose(p, k) {
    var n = COFFEE_SEQ[k % COFFEE_SEQ.length]; if (n === "SIP") { n = p.poses.coffeeSip ? "coffeeSip" : "sip"; }
    return n && p.poses[n] ? n : null;
  }
  function holdcupFrom(p) {                                            // where in HOLDCUP to start: the frame the coffee was showing
    var k = p.activity === "coffee" ? p.actFrame % COFFEE_SEQ.length : 0;
    if (k >= LIFT_AT && k <= SIP_AT) { return HOLDCUP.indexOf(k); }
    if (k > SIP_AT && k < DOWN_AT + COFFEE_LIFT) { return k < DOWN_AT ? HOLDCUP.length - 1 : HOLDCUP.indexOf(LIFT_AT + (DOWN_AT + COFFEE_LIFT - 1 - k)); }
    return (k >= 28 && k < LIFT_AT) || (k >= DOWN_AT + COFFEE_LIFT && k < DOWN_AT + COFFEE_LIFT + 8) ? 4 : 0;
  }
  function coffeeFromHoldcup(p) {                                      // back from it: the coffee goes on from the same frame, on the way down
    var j = HOLDCUP[Math.min(HOLDCUP.length - 1, (p.cupAt || 0) + p.actFrame)];
    return j >= SIP_AT ? DOWN_AT : j >= LIFT_AT ? DOWN_AT + COFFEE_LIFT - 1 - (j - LIFT_AT) : j >= 28 ? DOWN_AT + COFFEE_LIFT : DOWN_AT + COFFEE_LIFT + 8;
  }
  function poseOf(p, f) {
    var a = p.activity, name = POSE_OF[a] || (p.poses[a] ? a : "rest");
    // (T128: the mug stands at their side; the coffee is the reach, the hold, the lift in steps, the sip and back: COFFEE_SEQ)
    if (a === "coffee") { name = coffeePose(p, p.actFrame) || "rest"; }
    if (a === "holdcup") { name = coffeePose(p, HOLDCUP[Math.min(HOLDCUP.length - 1, (p.cupAt || 0) + p.actFrame)]) || name; }
    if (p.react === "surprise") { name = "surprise"; }
    else if (p.gesture && a === "rest" && (p !== cole || SCENE_ON.coleTalkHands)) { name = "talk"; }      // a hand joins in only when it is free (not from thinking: chin on hand to talking arms read as a shoulder jump, T58/j); his stays at rest (SCENE_ON)
    if (a === "wave" && p.react === "greet") {                           // T33: the hand comes up and stays; the other arm stays as it was
      var from = p.greetAct === "coffee" ? "rest" : (POSE_OF[p.greetAct] || p.greetAct);   // (from a coffee the mug stands on the desk: T128)
      name = p.poses[from + "Wave"] ? from + "Wave" : p.poses.restWave ? "restWave" : "wave";
    }
    if ((name === "talk" && p === cole && !SCENE_ON.coleTalkHands) || (/^highfive/.test(name) && !SCENE_ON.highFive)) { name = "rest"; }   // (go-live: off, SCENE_ON)
    if (name === "wave" && p.poses.wave2 && (a === "fan" || p.name === "ilinca") && ((p.actFrame >> 2) % 2)) { name = "wave2"; }   // her wave rocks a pixel; his only fans smoke
    if (name === "write" && p.poses.write1) { name = WRITING[(p.actFrame >> 1) % WRITING.length]; }
    if (name === "fold" && p.poses.fold3) { name = p.actFrame < 14 ? "fold" : "fold3"; }   // T42: the sheet folded, then the plane
    if (!p.react && !p.gesture) { name = motion(p, name); }
    if (name === "shake" && p.poses.shake2 && (p.actFrame % 2)) { name = "shake2"; }
    if (name === "petcat" && p.poses.petcat2 && ((p.actFrame / 6 | 0) % 2)) { name = "petcat2"; }   // a slow stroke along her back
    if (name === "petedge" && p.poses.petedge2 && ((p.actFrame / 6 | 0) % 2)) { name = "petedge2"; }
    if (name === "petlap" && p.poses.petlap2 && ((p.actFrame / 6 | 0) % 2)) { name = "petlap2"; }   // T88: the stroke behind the screen, in and out along the arm
    if (name === "petedgeLap" && p.poses.petedgeLap2 && ((p.actFrame / 6 | 0) % 2)) { name = "petedgeLap2"; }   // (the visit, the laptop on the desk)
    return p.poses[name] ? name : "rest";
  }
  function posePoint(p, name) { var d = p.drawn; if (!d || !d.pose.pts[name]) { return null; } var q = d.pose.pts[name]; return { x: d.o.x + q[0], y: d.o.y + q[1] + d.jig }; }

  // A nod, or looking down at the work, moves the face (eyes, brows, mouth) a pixel down inside the head, the lids
  // lowered; the head itself stays whole (folding it a pixel looked like it shrank).
  // Looking down at something (the work, the cat, a nod) the head itself tips toward the desk: a second head drawn from
  // a generated picture of each of them looking down (Cole's note 10); its eyes are open on the work and shut in a nod
  // (note 11: "the current look down is perfect for a nod").
  function drawHead(p, o) { blit(p.lookDown ? p.headDown : p.head, o.x, o.y + p.headDy); }
  // His yawn (Y1; Cole, 2026-10-28: "face needs to move with yawn"): in his yawn video the head tips back as the yawn opens and
  // comes forward again as it ends. As a nod moves the face a pixel down inside the head, the yawn moves it a pixel up (tilt
  // -1: his shut eyes and raised brows; the mouth is under his hand) from YAWN_TIP[0] to YAWN_TIP[1] frames into it. (The whole
  // head lifted a pixel instead doubled his jaw line against the neck below it: work/r33/live.)
  var YAWN_TIP = [3, 17];
  function yawnTip(p) {
    if (p !== cole || p.react) { return false; }
    var k = p.activity === "yawn" ? p.actFrame : p.yawnAt ? frame - p.yawnAt : -1;   // (or yawning at his laptop: yawnAt)
    return k >= YAWN_TIP[0] && k < YAWN_TIP[1];
  }
  // A stretch: eyes shut, mouth open (the face keeps its own proportions: moving the features read as a different face).
  function stretching(p) { return p.activity === "stretch" && !p.react && !p.talking; }
  function drawFace(p, o, f) {
    var a = p.art, hy = o.y + p.headDy, t = p.tilt, st = stretching(p), dn = p.drawn && p.drawn.name, atLips = dn === "sip" || dn === "drink", handAtMouth = dn === "yawn";
    var closed = st || p.blink > 0 || p.mouth === "laugh" || p.mouth === "yawn" || atLips;   // a sip with the eyes shut (T44)
    if (p.lookDown) {                                                  // the head tipped down: eyes open on the work, shut in a nod or a blink
      pixels(a.down.eyes[(p.nod > 0 || closed) ? "closed" : "open"], o.x, hy, a.pal);
      var md = p.mouth; if (md === "talk") { md = (f % 4 < 2) ? "open" : "neutral"; } if (md === "neutral") { md = p.restMouth; }
      pixels(a.down.mouth[md] || a.down.mouth.neutral, o.x, hy, a.pal); return;
    }
    var lx = Math.round(p.look.x), ly = Math.round(p.look.y);
    var key = closed ? "closed" : ((ly > 0 || t > 0 ? "down" : "open") + (lx < 0 ? -1 : lx > 0 ? 1 : 0));
    pixels(a.eyes[key] || a.eyes.open0, o.x, hy + t, a.pal);
    pixels(a.brows[p.brows || (st ? "up" : ly < 0 ? "up" : "neutral")] || a.brows.neutral, o.x, hy + t, a.pal);
    var m = p.mouth; if (m === "talk") { m = (f % 4 < 2) ? "open" : "neutral"; } if (m === "neutral") { m = st ? "o" : p.restMouth; }
    if (!atLips && !handAtMouth) { pixels(a.mouth[m] || a.mouth.neutral, o.x, hy + t, a.pal); }   // the mug or the bottle is at the mouth: no lips drawn beside it (T44)
  }

  function drawCharacter(p, f) {
    if (p.hidden) { p.drawn = null; return; }
    var o = origin(p), name = poseOf(p, f), pose = p.poses[name];
    var jig = 0;                                                         // the body never jumps under the head (shaking moves only the arms: shake2)
    p.drawn = { o: o, pose: pose, name: name, jig: jig };
    var under = UNDER_DESK[name] || pose.under;                          // hands under the desk: nothing below its back edge (round-31 audit)
    if (under) { g.save(); g.beginPath(); underClip(pose, o); g.clip(); }
    blit(bodyOf(pose), o.x, o.y + jig);
    if (!pose.ownHead) {                                                 // (a picture that brings its own head: leaning back)
      drawHead(p, o);
      drawFace(p, o, f);
      if (pose.frontBody) { blit(pose.frontBody, o.x, o.y + jig); }      // hands and things in front of her hair, where her body has them
      if (pose.front) { blit(pose.front, o.x, o.y + jig + p.headDy); }    // what is at the face moves with the head
    }
    if (under) { g.restore(); }
    if (pose.ownHead) { return; }
    if (/^type/.test(name) && pose.props.laptop) { blit(pose.props.laptop, o.x, o.y + jig); }   // the laptop stands in front of the neck and the hair (T29, T45)
    drawSeal(p);                                                         // where his line meets the station's box (STATION_SEAL)
    if (p.activity === "solder") {                                       // the iron's tip: a glow, a wisp of smoke, now and then a spark
      var tip = posePoint(p, "tip");
      if (tip) { px(tip.x, tip.y, (f % 6 < 3) ? C.ironHot : C.iron); var sm = (f >> 1) % 10; px(tip.x + (sm % 2), tip.y - 2 - sm, sm < 5 ? C.smoke : C.smoke2); if (f % 23 === 0) { px(tip.x - 1, tip.y - 1, C.sun); px(tip.x + 1, tip.y - 2, C.sun); } }
    }
  }
  // Hands, forearms and what they hold lie on the desk: that part of the pose is drawn again once the desk is there.
  // While her laptop is left on the desk (the shake break), the hands at its keyboard stay behind it as when typing: below
  // the desk line nothing of them is drawn where the laptop stands (their tips had stuck out under its front edge).
  // (a pose under the desk ends at its edge; a pose's 'under' columns only: her coffee frames' arm in her lap, T128)
  function underClip(pose, o) {
    var e = deskEdge(), u = pose.under; g.rect(0, 0, W, e);
    if (u) { g.rect(0, e, o.x + u[0], H - e); g.rect(o.x + u[1] + 1, e, W, H - e); }
  }
  function drawOnDesk(p) {
    var d = p.drawn; if (p.hidden || !d || UNDER_DESK[d.name]) { return; }   // (hands under the desk: none of it is on the desk)
    var lap = p.deskProp === "type" && p.poses.type && p.poses.type.props.laptop, u = d.pose.under;
    g.save(); g.beginPath();
    if (lap) { var lx0 = d.o.x - Math.round(p.slide) + lap.x, lx1 = lx0 + lap.w; g.rect(0, DESK_Y, lx0, H - DESK_Y); g.rect(lx1, DESK_Y, W - lx1, H - DESK_Y); }
    else if (u) { g.rect(0, DESK_Y, d.o.x + u[0], H - DESK_Y); g.rect(d.o.x + u[1] + 1, DESK_Y, W, H - DESK_Y); }   // (her arm in her lap stays under it)
    else { g.rect(0, DESK_Y, W, H - DESK_Y); }
    g.clip();
    blit(bodyOf(d.pose), d.o.x, d.o.y + d.jig); if (d.pose.frontBody) { blit(d.pose.frontBody, d.o.x, d.o.y + d.jig); } if (d.pose.front) { blit(d.pose.front, d.o.x, d.o.y + d.jig + p.headDy); }
    g.restore();
  }
  // The laptop (or the paper) stays on the desk while the hands are off it: lifted for the cat, or petting her.
  // T91 ("cole's paper disappears when maker shows up"): the paper stays too, whole, under the hands (drawSheetBehind,
  // drawDeskPropUnder: the 'paper' prop closed by its top edge, tools/desk/poses.py prop_fix); one sheet, never a second.
  // Round-31 audit (T91 in the visit, r31-maker): a petting arm that reaches past the laptop's screen or lies on the paper is
  // drawn again over it (the pose's 'over' layer: the arm's skin and its outline).
  function leftOnDesk(p) {                                             // the pose whose things lie on the desk while the hands are elsewhere
    if (p.hidden) { return null; }
    var greetFrom = p.react === "greet" && (p.greetAct === "type" || p.greetAct === "write") ? p.greetAct : null;   // waving hello from the keyboard
    var keep = p.keepProps === "type" || p.keepProps === "write" ? p.keepProps : null;
    var from = p.laptopOut ? "type" : keep || p.benchFrom || ((p.catLift === "type" || p.catLift === "write") ? p.catLift : greetFrom), q = from && p.poses[from];
    return !q || (p.activity === from && !p.laptopOut) ? null : q;
  }
  function drawLaptopOut(p) {                                           // (a paper lies under the hands: drawDeskPropUnder)
    var q = leftOnDesk(p); if (!q) { return; }
    var o = origin(p), d = p.drawn; Object.keys(q.props).forEach(function (n) { if (n !== "paper") { blit(q.props[n], o.x, o.y); } });
    // (the petting arm in front of the laptop's screen, or on the paper. Round-31 integration: his petting pose has his shirt
    // down onto the desk's first row, where the paper lies, so under the hands the sheet had lost its white to the shirt's
    // hem in the visit, a thin grey line left; with an arm drawn 'over', the paper's sheet goes over the pose once more and
    // the arm over it, as r31-maker's audited visit drew it: the paper in front of his shirt, his arm and hand on it)
    if (d && d.pose.over) { drawDeskPropUnder(p); blit(d.pose.over, d.o.x, d.o.y + d.jig); }
  }
  // The work left on the desk while the hands do something else (the shake break, T48; a greeting, Maker on the desk): a
  // paper lies under the hands (only the sheet: its picture carries a scrap of her blouse above it), a laptop stands in
  // front of them as it does while typing. p.deskProp is the activity whose things stay ("type", "write"); they stay where they
  // were put however the figure moves (p.slide).
  // The sheet's top row in the paper picture (tools/desk/poses.py prop_fix; above it the picture carries scraps of the pose).
  // His top edge lies on the row above the desk line: that row is drawn before the figures, so wherever he is he stays in
  // front of it (it had drawn a line through his fingers); the rest, on the desk, before his hands and forearms on it.
  var SHEET_TOP = { cole: 87, ilinca: 84 };
  function sheetLeft(p) { var q = p.deskProp === "write" && !p.hidden ? p.poses.write : leftOnDesk(p); return q && q.props.paper ? q : null; }
  function drawSheetPart(p, y0, y1, up) {
    var q = sheetLeft(p), o = origin(p), top = Math.max(y0, o.y + SHEET_TOP[p.name]); if (!q || top >= y1) { return; }
    g.save(); g.beginPath(); g.rect(0, top, W, y1 - top); g.clip(); blit(q.props.paper, o.x - Math.round(p.slide), o.y - (up || 0)); g.restore();
  }
  // (in the wide room picture the desk's back edge is a dark line on row 132 with a row of desk top under it: there the
  // sheet's white runs up to that line, which closes it, instead of a second dark row under it; art.deskEdge)
  function drawSheetBehind(p) { drawSheetPart(p, 0, DESK_Y, Math.max(0, DESK_Y - 1 - deskEdge())); }
  function drawDeskPropUnder(p) { drawSheetPart(p, DESK_Y, H); }
  function drawDeskPropOver(p) {
    var q = p.deskProp === "type" && !p.hidden && p.poses.type; if (!q || !q.props.laptop) { return; }
    var o = origin(p); blit(q.props.laptop, o.x - Math.round(p.slide), o.y);
  }
  // A hand petting the cat lies on her: that part of the pose (a box in the figure's coordinates) goes on again after her.
  // (r33-live: his E2 and E3 each have their own box, the stroking hand's, from the hand round's boxes.json; inside it, where
  // she lies, those pictures leave their layer clear)
  var PET_HAND = { cole: { pet: [60, 72, 86, 100], pethead: [28, 60, 52, 82], petcat: [52, 57, 69, 68], petcat2: [50, 58, 67, 67], petedge: [53, 67, 70, 78], petedge2: [51, 68, 68, 77] },   // T62: the hand on her head; the other forearm rests behind her
                   ilinca: { pet: [-20, 66, 2, 88], pethead: [12, 54, 40, 70], petcat: [-20, 52, 16, 78], petcat2: [-20, 52, 16, 78], petedge: [-29, 62, 24, 100], petedge2: [-29, 62, 24, 100] } };   // (petedge2's started at row 52 and redrew her body over her hair: re-audit)
  ["cole", "ilinca"].forEach(function (n) { var b = PET_HAND[n]; b.petedgeLap = b.petedge; b.petedgeLap2 = b.petedge2; });   // (the visit with the laptop on the desk)
  // Where Maker lies to be petted: the petting pictures were made with a cat under the hand (since erased); she lies
  // where that cat was, facing the same way, so the hand rests exactly on her back. Figure coordinates of her middle.
  var PET_RIG = { cole: { x: 57, dir: -1 }, ilinca: { x: -3, dir: -1 } };
  var PAPER_Y = DESK_Y + 4;                                              // curled up on the writing paper, at the back of the desk
  function petSpot(p) { return p.x - p.art.centre + PET_RIG[p.name].x; }
  function drawPetHand(p) {
    var d = p.drawn, box = d && PET_HAND[p.name][d.name]; if (!box || p.hidden || !actors.cat) { return; }
    g.save(); g.beginPath(); g.rect(d.o.x + box[0], d.o.y + box[1], box[2] - box[0], box[3] - box[1]); g.clip();
    blit(d.pose.over && leftOnDesk(p) ? d.pose.over : bodyOf(d.pose), d.o.x, d.o.y + d.jig); g.restore();   // (only the arm, over the laptop: its shirt stays behind it)
  }

  /* ---------- desk set per visit ---------- */
  var SETS = [
    ["vase0", "plant", "papers", "mug"], ["plant", "bottle", "vase1", "cartridge"], ["bottle", "vase2", "plant", "mug"],
    ["vase1", "papers", "bottle", "cartridge"], ["papers", "plant", "vase0", "bottle"], ["plant", "cartridge", "papers", "mug"], ["vase2", "papers", "plant", "bottle"]
  ];
  var setIndex = (function () {
    try { var n = parseInt(localStorage.getItem("nutrimatic-desk-visit") || "-1", 10); n = isNaN(n) ? Math.floor(Math.random() * SETS.length) : n + 1; localStorage.setItem("nutrimatic-desk-visit", String(n)); return n % SETS.length; }
    catch (e) { return Math.floor(Math.random() * SETS.length); }
  })();
  var extras = [];   // things left on the desk by scenarios: {kind, x}
  function propArt(name, x, y) { var im = ENV.img["prop-" + name]; g.drawImage(im, Math.round(x - im.width / 2), y - im.height); }
  function drawProps(f) {
    var set = SETS[setIndex];
    if (ENV.ready) {
      for (var j = 0; j < L.art.slots.length && j < set.length; j++) {
        var kind = set[j].indexOf("vase") === 0 ? "vase" : set[j] === "cartridge" ? "papers" : set[j];
        var sy = deskAt(kind === "mug" ? 0.45 : 0.35) + 1; propArt(kind, L.art.slots[j], sy); if (kind === "mug") { steam(L.art.slots[j] - 1, sy - 12, f); }
      }
      if (stationShows()) { propSolderStation(stationX()); restingPick(); restingIron(f); }
      if (ilinca.phoneOnDesk && !ilinca.hidden && !actors.buzz) { propPhoneOnDesk(phoneSpot()); }   // (buzzing, the call draws it)
      for (var m = 0; m < extras.length; m++) {
        var e2 = extras[m];
        if (e2.kind === "plane") { propPlane(e2.x, deskAt(0.7), e2.dir); } else if (e2.kind === "bottle") { propArt("bottle", e2.x, deskAt(0.5) + 1); }
        else if (e2.kind === "mug") { propArt("mug", e2.x, deskAt(0.55) + 1); if (e2.steam) { steam(e2.x - 1, deskAt(0.55) - 11, f); } }
      }
      people.forEach(function (p) { if (!catBehindMug(p)) { drawStandingMug(p, f); } });   // T128: their everlasting mugs (the room drawn in code, while the pictures load, keeps its own desk set)
      return;
    }
    for (var i = 0; i < L.slots.length && i < set.length; i++) {
      var k = set[i], x = L.slots[i];
      if (k === "plant") { propPlant(x); } else if (k === "papers") { propPapers(x); } else if (k === "bottle") { propBottle(x, DESK_Y); }
      else if (k === "cartridge") { propCartridge(x); } else if (k === "mug") { propMug(x, DESK_Y, false, f); } else if (k.indexOf("vase") === 0) { propVase(x, +k[4]); }
    }
    if (stationShows()) { propSolderStation(stationX()); restingPick(); restingIron(f); }
    if (ilinca.phoneOnDesk && !ilinca.hidden && !actors.buzz) { propPhoneOnDesk(phoneSpot()); }   // (buzzing, the call draws it)
    for (var e = 0; e < extras.length; e++) { var ex = extras[e]; if (ex.kind === "plane") { propPlane(ex.x, deskAt(0.7), ex.dir); } else if (ex.kind === "bottle") { propBottle(ex.x, DESK_Y); } else if (ex.kind === "mug") { propMug(ex.x, DESK_Y, ex.steam, f); } }
  }

  /* ---------- conversation without bubbles: look at each other, talk, gesture, nod ---------- */
  var EXCHANGES = [
    [["cole", 2.2], ["ilinca", 1.6], ["cole", 1.2]], [["ilinca", 1.8], ["cole", 0.9], ["ilinca", 1.6]], [["cole", 1.9], ["ilinca", 2.0]],
    [["ilinca", 1.0], ["cole", 0.9]], [["ilinca", 2.0], ["cole", 1.7], ["ilinca", 1.3]], [["cole", 2.3], ["ilinca", 1.5]]
  ];
  var convo = null, nextConvoAt = 9 * FPS, saidHello = false;
  function startConvo(lines) { convo = { lines: lines, i: 0, until: 0 }; }
  function stepConvo(f) {
    if (!convo) {
      if (f >= nextConvoAt && !scenario && !review && !cole.react && !ilinca.react) { startConvo(EXCHANGES[(Math.random() * EXCHANGES.length) | 0]); nextConvoAt = f + (26 + Math.random() * 30) * FPS; }   // (never into a greeting: a listener's nod on a wave, f)
      return;
    }
    if (f >= convo.until) {
      people.forEach(function (p) { p.talking = false; p.gesture = false; if (p.mouth === "talk") { p.mouth = "neutral"; } });
      if (convo.i >= convo.lines.length) { convo = null; people.forEach(function (p) { p.turn = 0; p.mouth = Math.random() < 0.6 ? "smile" : "neutral"; p.smileUntil = f + 3 * FPS; }); return; }
      var line = convo.lines[convo.i], sp = who(line[0]), ls = other(sp);
      sp.talking = true; sp.mouth = "talk"; sp.gesture = Math.random() < 0.7;
      sp.turn = ls.x < sp.x ? -1 : 1; ls.turn = sp.x < ls.x ? -1 : 1;
      sp.lookTarget = { x: sp.turn, y: 0 }; ls.lookTarget = { x: ls.turn, y: 0 };
      ls.nodAt = f + Math.round(line[1] * FPS * 0.6);
      convo.until = f + Math.round(line[1] * FPS); convo.i++;
    }
  }

  /* ---------- activities ---------- */
  var frame = 0;
  // r33-live (audit of the go-live; Cole's standing rule: props never vanish): a short break from the laptop or the paper (a
  // stretch, the late-night yawn, the fist pump, her phone ringing) leaves it on the desk where it stands while typing or
  // writing, in front of them as it is then, the hands that stay on the desk behind it, none below its front edge (p.deskProp,
  // as the shake break keeps her work: drawDeskPropOver, drawOnDesk, sheetLeft); the work goes on after the break (p.resume).
  // A change of task (thinking, soldering, the phone, resting) puts it away as before: its hands and things need that place.
  // (the test state: "laptop" or "paper" while one of theirs is on the desk, in the pose or kept there; null when not)
  function workOnDesk(p) {
    var n = (!p.hidden && p.drawn && p.drawn.name) || "", q;
    if (/^type/.test(n) || p.deskProp === "type") { return "laptop"; } if (/^write/.test(n) || p.deskProp === "write") { return "paper"; }
    q = leftOnDesk(p); return q && q.props.laptop ? "laptop" : q && q.props.paper ? "paper" : null;
  }
  function leaveWork(p) { if (!p.deskProp && (p.activity === "type" || p.activity === "write")) { p.deskProp = p.resume = p.activity; } }
  function resumeWork(p, secs) { var a = p.resume; p.deskProp = null; p.resume = null; setActivity(p, a, secs); }
  function setActivity(p, a, seconds) {
    // (T141, Cole on the go-live page: "paper moves under ilinca's hand": writing is off, but a hold of the test hooks (the
    // approval page's cards) still sat her at her paper, whose writing frames move the sheet with the hand. Off is off: asked
    // to write while writing is off, they type; no paper is ever on the desk)
    if (a === "write" && !SCENE_ON[p === cole ? "coleWrite" : "ilincaWrite"]) { a = "type"; }
    // T48 (round-31 integration): a scene that takes his hands off the board while he solders (scenario.bench) leaves the
    // bench as the spark does: the station and the board stay on the desk and his tools lie on it (p.benchFrom: stationShows,
    // leftOnDesk, restingIron, restingPick); he picks them up again when he goes back to soldering
    if (p === cole && scenario && scenario.bench && p.activity === "solder" && a !== "solder" && !p.benchFrom) { var d = p.drawn; p.benchFrom = d && /^solder/.test(d.name) ? d.name : "solder"; }
    if (p === cole && a === "solder") { p.benchFrom = null; }
    p.activity = a; p.actFrame = 0; p.actUntil = frame + Math.round(seconds * FPS);
    p.brows = a === "think" ? "down" : (p.brows === "down" ? null : p.brows);
    if (p === ilinca) { p.phoneOnDesk = a !== "phone" && a !== "call"; }
  }
  function nextActivity(p) {
    if (p.resume) { resumeWork(p, review ? 1e4 : 6 + Math.random() * 8); return; }   // (back to the laptop or the paper after a break)
    if (review && review[p.name]) { setActivity(p, review[p.name], 1e4); return; }
    var a = p.activities[(Math.random() * p.activities.length) | 0];
    if (a === p.activity) { a = p.activities[(Math.random() * p.activities.length) | 0]; }
    if (a === "stretch" && (other(p).activity === "stretch" || other(p).activity === "yawn")) { a = "rest"; }   // never both at once
    if (a === "stretch") { leaveWork(p); }                               // (a stretch from the keyboard: the laptop stays, and back to it)
    var secs = a === "stretch" ? 2.5 : a === "coffee" ? 10 : a === "rest" ? 4 : 12 + Math.random() * 14;
    setActivity(p, a, secs);
  }
  function faceOf(p, o) { if (o.mouth !== undefined) { p.mouth = o.mouth; } if (o.brows !== undefined) { p.brows = o.brows; } if (o.look) { p.lookTarget = o.look; } if (o.turn !== undefined) { p.turn = o.turn; } }
  function lookAtEachOther() { cole.turn = ilinca.x > cole.x ? 1 : -1; ilinca.turn = -cole.turn; cole.lookTarget = { x: cole.turn, y: 0 }; ilinca.lookTarget = { x: ilinca.turn, y: 0 }; }
  function lookAt(p, x, y) { p.lookTarget = aimAt(p, x, y); p.turn = p.lookTarget.x; }
  function faceLevel(p) { return eyeY(p); }

  /* ---------- Maker, the cat ---------- */
  // Drawn from sprites when the art has them (ART.maker: walk0/1, sit, sitside, yawn, loaf, curl, stand, knead0/1, most
  // with a ...Blink twin), otherwise as a simple grey cat. (x, y) = feet centre on the desk. She stands on the desk top,
  // in front of their arms (catY), and blinks every second or three.
  function bakeSheet(sheet) { if (!sheet) { return null; } var out = {}; Object.keys(sheet).forEach(function (k) { if (k !== "pal") { out[k] = bake(sheet[k], sheet.pal); } }); return out; }
  var MAKER = bakeSheet(ART.maker);
  // Where her feet go: the front of the desk top (it is drawn higher in the phone layout's room).
  function catY() { return ENV.ready ? L.art.catY : DESK_Y + 7; }      // where her paws are as she walks: the desk's front half
  // at the desk's front edge: lying there her front paws and tail hang over it; kneading or sitting up she is just behind it
  function catEdgeY(state) { return state === "loaf" ? DESK_FRONT + 1 : DESK_FRONT; }
  function towards(c, ty) { c.y += Math.max(-1, Math.min(1, ty - c.y)); }   // a pixel a frame: she walks forward or back on the desk
  var WALK_N = 10;                                                       // Maker's walk: frames a cycle (tools/desk/walk_rig.py)
  function drawMaker(x, y, pose, dir, f, blink) {
    var d = dir || 1;
    // the walk: ten frames, one per three pixels she moves (a 30 px stride), so the paws on the desk stay where they are
    var step = Math.floor(x * d / 3), key = pose === "walk" ? "walk" + (((step % WALK_N) + WALK_N) % WALK_N) : pose === "knead" ? "knead" + ((f >> 2) % 2) : pose;
    var set = MAKER, data = ART.maker;
    if (blink && set && set[key + "Blink"]) { key += "Blink"; }
    if (set && set[key]) {
      var s = set[key], ox = x - (s.w / 2 | 0), oy = y - s.h + (data[key].g || 0);
      if (pose === "loaf") { drawHangingTail(d > 0 ? ox + 5 : ox + s.w - 6, oy + s.h - (data[key].g || 0) - 2, f, d); }   // under her rear
      if (d > 0) { blit(s, ox - s.x, oy - s.y); } else { blitFlip(s, ox - s.x, oy - s.y); }
      return;
    }
    var body = C.cat, dk = C.catD, lt = C.catL, blinkNow = (f % 46) >= 42;
    if (pose === "sit" || pose === "yawn") {
      rect(x - 7, y - 17, 14, 17, body); rect(x - 8, y - 12, 16, 12, body); rect(x - 5, y - 16, 10, 3, lt); vline(x - 8, y - 11, 10, dk); hline(x - 7, y - 1, 14, dk);
      rect(x - 6, y - 27, 13, 11, body); px(x - 6, y - 29, body); px(x - 5, y - 28, body); px(x - 6, y - 28, body); px(x + 6, y - 29, body); px(x + 5, y - 28, body); px(x + 6, y - 28, body); px(x - 5, y - 27, dk); px(x + 5, y - 27, dk);
      if (pose === "yawn") { rect(x - 2, y - 22, 5, 5, C.catMouth); outline(x - 3, y - 23, 7, 7, dk); hline(x - 4, y - 24, 3, dk); hline(x + 2, y - 24, 3, dk); px(x - 1, y - 21, C.white); px(x + 1, y - 21, C.white); }
      else { rect(x - 4, y - 23, 3, 2, blinkNow ? dk : C.catEye); rect(x + 2, y - 23, 3, 2, blinkNow ? dk : C.catEye); if (!blinkNow) { px(x - 3, y - 23, C.ink); px(x + 3, y - 23, C.ink); } px(x, y - 20, C.catNose); px(x - 1, y - 19, dk); px(x + 1, y - 19, dk); }
      limb(x + 7 * d, y - 3, x + 13 * d, y - 9 + ((f >> 3) % 2), 2, dk);
    } else if (pose === "loaf") {
      rect(x - 14, y - 12, 28, 12, body); rect(x - 12, y - 14, 24, 2, body); hline(x - 10, y - 14, 18, lt); hline(x - 14, y - 1, 28, dk); vline(x - 14 * d - (d > 0 ? 0 : 1), y - 10, 9, dk);
      var hx = x + 10 * d; rect(hx - 6, y - 21, 12, 11, body); px(hx - 6, y - 23, body); px(hx - 5, y - 22, body); px(hx - 6, y - 22, body); px(hx + 5, y - 23, body); px(hx + 4, y - 22, body); px(hx + 5, y - 22, body);
      rect(hx - 4, y - 17, 3, 2, blinkNow ? dk : C.catEye); rect(hx + 1, y - 17, 3, 2, blinkNow ? dk : C.catEye); if (!blinkNow) { px(hx - 3, y - 17, C.ink); px(hx + 2, y - 17, C.ink); } px(hx - 1, y - 14, C.catNose);
      rect(x + 4 * d, y - 2, 5, 6, body); hline(x + 4 * d, y + 3, 5, dk);                              // the paw over the edge
    } else {                           // walk
      var s2 = (f >> 1) % 4;
      rect(x - 13, y - 15, 26, 9, body); hline(x - 11, y - 15, 20, lt); hline(x - 13, y - 7, 26, dk);
      var fx = x + 13 * d; rect(fx - (d > 0 ? 2 : 9), y - 20, 11, 10, body); px(fx + (d > 0 ? -1 : -8), y - 22, body); px(fx + (d > 0 ? 7 : 0), y - 22, body); px(fx + (d > 0 ? 0 : -7), y - 21, body); px(fx + (d > 0 ? 6 : -1), y - 21, body);
      rect(fx + (d > 0 ? 4 : -6), y - 17, 3, 2, C.catEye); px(fx + (d > 0 ? 5 : -5), y - 17, C.ink); px(fx + (d > 0 ? 8 : -9), y - 14, C.catNose);
      var legs = [[-10, s2 === 0 ? -1 : 0], [-6, s2 === 2 ? -1 : 0], [6, s2 === 1 ? -1 : 0], [10, s2 === 3 ? -1 : 0]];
      for (var i = 0; i < 4; i++) { rect(x + legs[i][0] * d - 1, y - 6, 3, 6 + legs[i][1], i % 2 ? dk : body); }
      limb(x - 13 * d, y - 13, x - 19 * d, y - 22 + (s2 % 2), 2, dk);
    }
  }

  /* ---------- scenarios: little scripted scenes ---------- */
  var scenario = null, nextScenarioAt = 22 * FPS, actors = {};
  // T128 (Cole, 2026-10-27: "The coffee run is sort of a non-starter because a lot will be needed that just isn't there. She'll
  // have to be standing, walk across the frame behind the desk. ... Eventually we can get the walking around thing working"):
  // the coffee run (SCENARIOS.coffee: she rolls off and back with two mugs, `carry`) is kept but never plays while this is off.
  var COFFEE_RUN = false;
  var review = null;   // the approval page's hold (test hooks): {cole, ilinca, greet, relay, petter, pointer}
  var still = false;   // test hook: no blinks, no passing expressions, no glancing about, clouds at rest (exact captures)
  function startScenario(name) {
    var sc = SCENARIOS[name]; if (!sc || (sc.when && !sc.when())) { return false; }
    if (scenario && scenario.end) { scenario.end(); }                    // (only the test hooks start one over another)
    scenario = { name: name, t0: frame, steps: sc.steps.map(function (s) { return { at: s[0], fn: s[1], done: false }; }), dur: sc.dur, bench: !!sc.bench, update: sc.update, drawOutside: sc.drawOutside, drawBack: sc.drawBack, drawMid: sc.drawMid, drawFront: sc.drawFront, end: sc.end };
    actors = {}; if (sc.setup) { sc.setup(); }
    people.forEach(function (p) { p.actUntil = frame + 1e6; p.gesture = false; }); convo = null;
    return true;
  }
  function stepScenario(f) {
    if (!scenario) { return; }
    var t = (f - scenario.t0) / FPS;
    scenario.steps.forEach(function (s) { if (!s.done && t >= s.at) { s.done = true; s.fn(t); } });
    if (scenario.update) { scenario.update(t, f); }
    if (t >= scenario.dur) { if (scenario.end) { scenario.end(); } scenario = null; actors = {}; people.forEach(function (p) { p.turn = 0; p.brows = p.activity === "think" ? "down" : null; p.mouth = "neutral"; p.hold = null; if (p === cole && p.benchFrom) { backToBench(); } else if (!p.resume && !review && (p.activity === "type" || p.activity === "write")) { setActivity(p, p.activity, 6 + Math.random() * 8); } else { nextActivity(p); } }); nextScenarioAt = f + (45 + Math.random() * 35) * FPS; }
  }
  function backToBench() {                                              // (T48) the scene is over: he takes up his tools again
    if (review && review.cole && review.cole !== "solder") { cole.benchFrom = null; nextActivity(cole); return; }
    setActivity(cole, "solder", review ? 1e4 : 12 + Math.random() * 14);
  }
  function neutral(p) { p.mouth = "neutral"; p.brows = null; p.turn = 0; p.lookTarget = { x: 0, y: 1 }; }
  // Maker in a scenario: her blinks, and hands that come up off the desk while she walks past them.
  // Hands go under the desk while she walks past them (note 9: lifting them into the air looked silly), as soon as her
  // body would reach them: the hands come out to about 44 pixels either side of a figure's middle, and half her
  // length goes the other way. A mug is lifted to drink instead, so it doesn't vanish.
  var HANDS_DOWN = { rest: 1, type: 1, write: 1, think: 1, coffee: 1 }, HAND_REACH = 44;
  function catHalf() { var w = MAKER && MAKER.walk0 ? MAKER.walk0.w : 64; return Math.round(w * 0.45); }   // half her length on the desk, nose to rump
  function catReach() { return HAND_REACH + catHalf() - 4; }
  function handsAway(p) { var from = holdcupFrom(p); setActivity(p, p.activity === "coffee" && p.poses.sip ? "holdcup" : "underdesk", 99); p.cupAt = from; }
  function handsBack(p) {                                              // (T128 follow-up: a coffee goes on where the lifted mug is)
    var k = p.activity === "holdcup" && p.catLift === "coffee" ? coffeeFromHoldcup(p) : 0;
    setActivity(p, p.catLift, 99); p.actFrame = k;
  }
  function catTick(c, f) {
    if (!c.nextBlink) { c.nextBlink = f + 12 + Math.random() * 24; }
    if (f >= c.nextBlink) { c.blinkUntil = f + 2; c.nextBlink = f + 14 + Math.random() * 26; }
    c.blink = c.shut || f < (c.blinkUntil || 0);
    people.forEach(function (p) {
      if (p.hidden || p.held) { return; }
      var reach = catReach(), near = c.state === "walk" && Math.abs(c.x - p.x) < reach;
      if (near && !p.catLift && HANDS_DOWN[p.activity]) { p.catLift = p.activity; handsAway(p); }                     // hands go under the desk as she passes
      else if (!near && p.catLift && (Math.abs(c.x - p.x) > reach + 6 || (c.state !== "walk" && p !== actors.petter))) { handsBack(p); p.catLift = null; }   // she has passed, or settled further along
    });
  }
  // Lying at the desk's front edge her tail hangs over it: a chain of short segments from the root, swinging like a
  // pendulum, each segment a little behind the one above it, so the tip trails; the end is round. Drawn in her own
  // greys: outline, coat, and a sheen on the side toward the window.
  var TAIL_LEN = 26, CAT_LINE = "#1f2129", CAT_COAT = "#696e79", CAT_SHEEN = "#7d828d";
  // full most of the way, narrowing a little toward the end, which is round (a pointed tip read worse)
  function tailWidth(t) { return t < 0.7 ? 1 : 1 - 0.22 * (t - 0.7) / 0.3; }
  function disc(cx, cy, r, col) {
    for (var y = Math.floor(cy - r); y <= Math.ceil(cy + r); y++) { for (var x = Math.floor(cx - r); x <= Math.ceil(cx + r); x++) { var dx = x + 0.5 - cx, dy = y + 0.5 - cy; if (dx * dx + dy * dy <= r * r) { px(x, y, col); } } }
  }
  function drawHangingTail(rx, ry, f, side) {
    var n = 12, step = TAIL_LEN / n, pts = [[rx, ry]], ff = reduceMotion ? 0 : f, t = Math.floor(ff / 3) * 3 / FPS;   // it moves in small steps, not a smooth sway
    var fk = ff % 53, flick = fk < 6 ? Math.sin(fk / 6 * Math.PI) * 0.55 : 0;                                          // now and then the tip flicks
    for (var i = 1; i <= n; i++) {
      var k = i / n, ang = Math.PI / 2 - side * 0.12 + Math.sin(t * 1.3 - k * 1.6) * (0.05 + 0.24 * k) + flick * k * k * side, q = pts[i - 1];
      pts.push([q[0] + Math.cos(ang) * step, q[1] + Math.sin(ang) * step]);
    }
    var passes = [[0.85, CAT_LINE, 0], [0, CAT_COAT, 0], [-0.75, CAT_SHEEN, 0.7]];
    for (var p2 = 0; p2 < passes.length; p2++) {
      for (var j = 0; j < n; j++) {
        for (var s2 = 0; s2 < 4; s2++) {
          var tt = (j + s2 / 4) / n, r = 2.0 * tailWidth(tt) + 0.2 + passes[p2][0];
          if (r > 0.05) { disc(lerp(pts[j][0], pts[j + 1][0], s2 / 4) + passes[p2][2], lerp(pts[j][1], pts[j + 1][1], s2 / 4), r, passes[p2][1]); }
        }
      }
    }
  }
  function catEnd() {
    people.forEach(function (p) {
      if (p.catLift) { handsBack(p); }
      if (/^pet/.test(p.activity) || p.activity === "underdesk") { setActivity(p, p.keepProps || "rest", 99); }   // no hand left stroking a cat that has gone, none left under the desk
      p.catLift = null; p.petFrom = null; p.held = false; p.laptopOut = false; p.keepProps = null;
    });
  }

  // The shaker sliding across the desk in the shake break, in its own desk-prop picture (propArt: x its middle, y one below
  // its bottom row). It starts where his hands held it (shake2's shaker, set 3 px lower onto the desk top) and eases to a
  // stop at her left (L.shake.stop px from her middle), moving toward the desk's front edge as it goes, clear of her mug,
  // laptop and paper; n frames, the first step 4 px. Round-31 integration audit: it had stopped 43 px from her middle in both
  // layouts, over her resting and typing elbow's tip. In the wide room it stops 49 px from her, 2 clear px from every pose
  // of hers (writing, the closest) and of his at rest. On a phone their elbows are 7 px apart, too close for the 14 px
  // shaker with 2 px on each side, so there it stops as before but she reaches for it 6 px before its stop, before it comes
  // within 2 px of her (L.shake.reach: it slides into her hand, which lies over it), and after drinking she keeps it
  // (L.shake.keep) instead of setting it down between her resting elbow and his.
  function shakerSlide() { var x0 = cole.x + 3, x1 = ilinca.x - L.shake.stop; return { x0: x0, x1: x1, y0: DESK_Y + 2, y1: DESK_Y + 8, n: Math.ceil((x1 - x0) / 2) }; }
  function shakerAt(k) { var s = shakerSlide(), p = clamp(k / s.n, 0, 1), e = 1 - (1 - p) * (1 - p); return { x: Math.round(s.x0 + (s.x1 - s.x0) * e), y: Math.round(s.y0 + (s.y1 - s.y0) * e) }; }

  // (go-live: which laptop or paper scene may play, SCENE_ON)
  function laptopScene(p) {
    return p.activity === "type" ? SCENE_ON[p === cole ? "laptopCole" : "laptopIlinca"] : p.activity === "write" ? SCENE_ON[p === cole ? "paperCole" : "paperIlinca"] : false;
  }
  var SCENARIOS = {
    // Cole sneaks a game on a red DS; Ilinca notices; he puts it away.
    ds: {
      dur: 13, bench: true,                                              // (from soldering: the station, board and tools stay on the desk)
      when: function () { return cole.activity !== "type"; },            // (r33-live: the console is held where his laptop's screen stands: not while he types)
      steps: [
        [0, function () { setActivity(cole, "ds", 99); faceOf(cole, { mouth: "smile", look: { x: 0, y: 1 }, turn: 0 }); }],
        [6.5, function () { faceOf(ilinca, { brows: "down", mouth: "flat" }); lookAt(ilinca, cole.x, faceLevel(cole)); }],
        [8.0, function () { faceOf(cole, { brows: "up", mouth: "o" }); lookAt(cole, ilinca.x, faceLevel(ilinca)); }],
        [9.0, function () { faceOf(cole, { brows: "sad", mouth: "frown", look: { x: 0, y: 1 }, turn: 0 }); setActivity(cole, "dsAway", 99); }],
        [10.6, function () { setActivity(cole, cole.benchFrom ? "solder" : "type", 99); faceOf(cole, { brows: null, mouth: "neutral" }); faceOf(ilinca, { brows: null, mouth: "smile" }); ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: 1 }; }]
      ]
    },
    // Cole folds a paper airplane in three steps and throws it; it glides past Ilinca and out of the room, both watch it
    // go (T42: "should glide to the side and out of frame when thrown").
    airplane: {
      dur: 7.5,
      when: function () { return SCENE_ON.airplane && !soldering(); },        // (T48: his throwing arm and his hands at rest lie where the board and the tools would)
      steps: [
        [0, function () { setActivity(cole, "fold", 99); faceOf(cole, { look: { x: 0, y: 1 }, turn: 0, mouth: "smile" }); }],
        [2.4, function () { setActivity(cole, "throw", 99); lookAt(cole, ilinca.x, faceLevel(ilinca)); }],
        [3.0, function () { var hand = posePoint(cole, "hand") || { x: cole.x + 40, y: DESK_Y - 100 }; setActivity(cole, "release", 99); actors.plane = { t0: frame, x0: hand.x, y0: hand.y, x: hand.x, y: hand.y }; }],
        [3.3, function () { faceOf(ilinca, { brows: "up", mouth: "o" }); }],   // she looks up from her laptop; it stays where it is
        [4.2, function () { faceOf(cole, { brows: "up", mouth: "smile" }); setActivity(cole, "rest", 99); }],
        [5.2, function () { faceOf(ilinca, { brows: null, mouth: "smile" }); }],
        [6.6, function () { neutral(cole); neutral(ilinca); }]
      ],
      update: function (t, f) {
        var pl = actors.plane; if (!pl || pl.gone) { return; }
        var k = f - pl.t0, dir = ilinca.x > cole.x ? 1 : -1;
        // it climbs to its height in six frames (four on a phone, where she sits closer), clear of her hair and soon level
        var cruise = DESK_Y - 95, past = dir > 0 ? pl.x > L.art.win.x - 6 : pl.x < 40;   // level between the two shelves (clear of the books above and the photo below), then a slow sink past the window
        pl.x = pl.x0 + dir * (k < 4 ? 7 * k : 28 + 5 * (k - 4)); pl.y = Math.round(pl.y0 + (cruise - pl.y0) * Math.sin(Math.min(1, k / (L === LAYOUTS.narrow ? 4 : 6)) * Math.PI / 2)) + (past ? Math.round((k - 18) * 0.4) : 0);   // 7 px a frame off the hand, then 5 (the old formula stepped back a pixel at the change)
        if (pl.x < -20 || pl.x > W + 20) { pl.gone = true; return; }
        [cole, ilinca].forEach(function (p) { if (k > 1) { lookAt(p, pl.x, pl.y); } });
      },
      // leaving his hand it is out of sight for two frames (only slivers showed round and between his fingers), behind
      // his fingers for one, then in front of everyone
      drawBack: function (t, f) { var pl = actors.plane; if (pl && !pl.gone && f - pl.t0 >= 2 && f - pl.t0 < 3) { propPlane(Math.round(pl.x), Math.round(pl.y), ilinca.x > cole.x ? 1 : -1); } },
      drawFront: function (t, f) { var pl = actors.plane; if (pl && !pl.gone && f - pl.t0 >= 3) { propPlane(Math.round(pl.x), Math.round(pl.y), ilinca.x > cole.x ? 1 : -1); } }
    },
    // A pigeon lands on the sill, pecks about, and leaves. Both watch it.
    pigeon: {
      dur: 11,
      setup: function () { actors.bird = { x: WIN.x + WIN.w - 8, y: WIN.y + 16, state: "land" }; },
      steps: [
        [1.2, function () { people.forEach(function (p) { lookAt(p, WIN.x + WIN.w / 2, sillY()); }); }],
        [8.4, function () { actors.bird.state = "fly"; }],
        [9.6, function () { people.forEach(function (p) { neutral(p); }); }]
      ],
      update: function (t, f) {
        var b = actors.bird, target = sillY() - 7;
        if (b.state === "land") { b.dir = -1; if (b.y < target) { b.y += 2; b.x -= L === LAYOUTS.narrow ? 0 : 1; } else { b.y = target; b.state = "walk"; b.t0 = f; } }
        else if (b.state === "walk") { var k = f - b.t0; b.dir = (k % 120) < 72 ? -1 : 1; if (k % 24 < 12 && !b.peck) { b.x += (k % (L === LAYOUTS.narrow ? 4 : 2)) === 1 ? b.dir : 0; } b.peck = (k % 30) >= 22; }   // it walks the way it faces (T39), turns once, pecks standing still; on a phone at half the pace, so it stays in the right-hand pane (the middle bar hid its head)
        else if (b.state === "fly") { b.dir = 1; b.y -= 3; b.x += 2; }
      },
      drawOutside: function (t, f) {                                     // on the ledge outside: behind the glass and the window's bars (T27)
        var b = actors.bird, x = Math.round(b.x), y = Math.round(b.y), flap = b.state !== "walk" && (f % 4 < 2), pk = b.peck ? 2 : 0, s = b.dir || -1;
        function R(dx, dy, w, h, col) { rect(s > 0 ? x + dx : x - dx - w + 1, y + dy, w, h, col); }   // drawn facing right, mirrored when it faces left
        R(-4, 0, 9, 5, C.pigeon); R(-6, 1, 3, 3, C.pigeonD); R(-3, 4, 7, 1, C.pigeonD);
        R(3, -3 + pk, 4, 4, C.pigeonL); R(7, -2 + pk, 1, 1, C.sun); R(5, -2 + pk, 1, 1, C.ink); R(3, pk, 3, 1, "#5d8f7a");
        if (flap) { R(-3, -2, 6, 1, C.pigeonL); R(-2, -3, 4, 1, C.pigeonL); } else { R(-3, 1, 5, 1, C.pigeonL); }
        if (b.state === "walk") { R(-1, 5, 1, 1, C.sun); R(2, 5, 1, 1, C.sun); }
      }
    },
    // Maker comes along the desk (hands go under it as she passes), kneads a spot between them, lies down for a good
    // while and blinks at them; one of them pets her (eyes shut, content; the laptop or the paper stays on the desk); she
    // sits up, looks at each in turn (they look back), and goes. Never while Cole is soldering.
    visit: {
      dur: 34, when: function () { return !soldering() && (SCENE_ON.visitIlinca || (SCENE_ON.visitCole && (SCENE_ON.visitColeTyping || cole.activity !== "type"))); },   // (go-live: SCENE_ON)
      setup: function () {
        var mayCole = SCENE_ON.visitCole && (SCENE_ON.visitColeTyping || cole.activity !== "type");   // (go-live: SCENE_ON)
        var petter = review && review.petter ? who(review.petter) : !SCENE_ON.visitIlinca ? cole : !mayCole ? ilinca : Math.random() < 0.5 ? cole : ilinca, spot = petSpot(petter), fromLeft = Math.random() < 0.5;
        actors.cat = { x: fromLeft ? -36 : W + 36, y: catY(), state: "walk", dir: fromLeft ? 1 : -1, spot: spot, phase: "in", lieDir: PET_RIG[petter.name].dir };
        actors.petter = petter;
      },
      steps: [
        [1.5, function () { people.forEach(function (p) { p.mouth = "smile"; }); }],
        // (round-31 audit, T91: the hands that came off the laptop or the paper go back under the desk, the laptop or the paper
        // staying there, and back to work once she has gone)
        // (r33-live: his hands stay under the desk until she has gone, whatever he was doing: back at rest his elbow, R2's, lay
        // behind her rump, a sliver of it showing along her back; hands-back is catTick's, as when she passes)
        [19.0, function () { var p = actors.petter; p.catLift = p.keepProps || p.petFrom || "rest"; p.keepProps = null; setActivity(p, "underdesk", 99); p.held = false; actors.cat.shut = false; }],
        [20.5, function () { var c = actors.cat; c.state = "sitside"; c.dir = cole.x < c.x ? -1 : 1; lookAt(cole, c.x, catY() - 30); cole.mouth = "smile"; }],
        [23.0, function () { var c = actors.cat; c.dir = -c.dir; lookAt(ilinca, c.x, catY() - 30); ilinca.mouth = "smile"; }],
        [25.5, function () { var c = actors.cat; c.state = "walk"; c.phase = "out"; c.dir = c.x < W / 2 ? -1 : 1; }],
        [31.0, function () { people.forEach(function (p) { neutral(p); }); }]
      ],
      update: function (t, f) {
        var c = actors.cat; catTick(c, f);
        towards(c, c.state === "walk" ? (c.phase === "in" && Math.abs(c.x - c.spot) < 24 ? catEdgeY("knead") : catY()) : catEdgeY(c.state));
        if (c.phase === "in" && c.state === "walk") { c.x += 3 * c.dir; if ((c.dir > 0 && c.x >= c.spot) || (c.dir < 0 && c.x <= c.spot)) { c.x = c.spot; c.state = "knead"; c.kneadUntil = f + 3 * FPS; } }
        else if (c.state === "knead" && f >= c.kneadUntil) { c.state = "loaf"; c.dir = c.lieDir; c.lyingSince = f; }
        if (c.state === "loaf" && c.lyingSince && f - c.lyingSince === 6 && t < 18) {   // she has settled: the one beside her strokes her
          // round-31 audit (Cole's T91, "cole's paper disappears when maker shows up", here too): the laptop or the paper
          // stays on the desk while they stroke her; typing, one hand stays at the keyboard behind the screen (petedgeLap)
          var pp = actors.petter, keep = pp.catLift === "type" || pp.catLift === "write" ? pp.catLift : null;
          pp.keepProps = keep; pp.petFrom = pp.catLift; pp.catLift = null; pp.held = true;
          setActivity(pp, keep === "type" && pp.poses.petedgeLap ? "petedgeLap" : pp.poses.petedge ? "petedge" : "pet", 99); pp.mouth = "smile"; c.shut = true; pp.lookTarget = aimAt(pp, c.x, c.y - 6);
        }
        else if (c.phase === "out") { c.x += 3 * c.dir; }
        if (t >= 1.5 && t < 30 && c.state !== "sitside") { people.forEach(function (p) { if (!p.held) { p.lookTarget = aimAt(p, c.x, catY() - 14); } }); }
      },
      drawFront: function (t, f) { var c = actors.cat; drawMaker(Math.round(c.x), Math.round(c.y), c.state, c.dir, f, c.blink); },
      end: catEnd
    },
    // Maker picks whoever is typing or writing and sits on the laptop (on the keyboard, peeking over the screen) or on
    // the paper. Hands under the desk, a look; the other one laughs; then a stroke anyway (on the paper; on Cole's laptop
    // behind the screen, T88). She leaves,
    // thinks better of it, and comes back once more; the hands go back to work once she has gone.
    laptop: {
      dur: 30, when: function () { return !soldering() && people.some(laptopScene); },
      setup: function () {
        var cands = people.filter(laptopScene), v = cands[(Math.random() * cands.length) | 0];
        var onLaptop = v.activity === "type", o = origin(v), box = onLaptop ? v.poses.type.props.laptop : v.poses.write && v.poses.write.props.paper;
        var sx = box ? o.x + box.x + (box.w / 2 | 0) : v.x, fromLeft = v === cole;
        if (!onLaptop) { sx = petSpot(v); }                              // on the paper she lies where the petting hand lands
        actors.cat = { x: fromLeft ? -36 : W + 36, y: catY(), state: "walk", dir: fromLeft ? 1 : -1, spot: sx, phase: "in", onLaptop: onLaptop && !!box, home: fromLeft ? -40 : W + 40, half: box ? (box.w / 2 | 0) : 0, lieDir: PET_RIG[v.name].dir };
        if (onLaptop && box) {                                           // T89: her paws behind the screen's bottom edge (on the desk top's back row);
          var sitH = MAKER && MAKER.sit ? MAKER.sit.h : 50, bottom = o.y + box.y + box.h;   // sitting, her eyes just over its top edge
          actors.cat.backY = clamp(bottom, DESK_Y + 1, catY()); actors.cat.sitY = Math.min(actors.cat.backY, o.y + box.y - 15 + sitH);
        }
        actors.victim = v; actors.act = v.activity; v.held = true;
        v.keepProps = actors.act;                                        // the laptop or the paper stays on the desk whatever the hands do
      },
      steps: [],
      update: function (t, f) {
        var c = actors.cat, v = actors.victim, o = other(v), dv = Math.abs(c.x - v.x); catTick(c, f);
        if (c.state === "walk" && c.phase === "in" && dv < catReach() && v.activity === actors.act) { setActivity(v, "underdesk", 99); }   // her way in crosses the hands
        if (c.phase === "leave" && dv > catReach() + 6 && v.activity === "underdesk") { setActivity(v, actors.act, 99); }                 // she has gone: back to work
        if (c.onLaptop) {
          // T89 ("just make the laptop screen the frontmost object in the scene instead of moving maker around"): she no
          // longer steps up onto the keyboard or goes behind the desk; she stays on the desk top, in front of the desk, and
          // the laptop is drawn over her (drawFront). Near it she walks to the back of the desk top, where it stands, so her
          // paws go out of sight behind the screen (at the front they showed under it); on the keyboard she peeks over it.
          var dl = Math.abs(c.x - c.spot);
          c.behind = dl <= c.half + catHalf() - 2;                       // over the keyboard, behind the screen (the test state reports it)
          if (c.state === "sit") { c.y = c.sitY; } else { towards(c, dl <= c.half + catHalf() + 8 ? c.backY : catY()); }   // (back before her legs reach it)
        } else {                                                          // the paper lies at the back of the desk: she steps back onto it
          towards(c, Math.abs(c.x - c.spot) < 24 && c.phase === "in" ? PAPER_Y : catY());
        }
        if (c.phase === "in" && c.state === "walk") {
          c.x += 3 * c.dir; lookAt(v, c.x, catY() - 14);
          if ((c.dir > 0 && c.x >= c.spot) || (c.dir < 0 && c.x <= c.spot)) {
            c.x = c.spot; c.since = f;
            if (c.onLaptop) { c.state = "sit"; c.dir = v.x < c.x ? -1 : 1; c.y = c.sitY; } else { c.state = "curl"; c.dir = c.lieDir; c.y = PAPER_Y; }   // sitting on the keyboard (peeking over the screen from the first frame), or curled up on the paper
            setActivity(v, "underdesk", 99);                                 // on the keyboard or the paper: the hands stay under the desk
            faceOf(v, { brows: "down", mouth: "flat" }); lookAt(v, c.x, DESK_Y - 34);
            lookAt(o, c.x, DESK_Y - 34); o.mouth = "laugh";
          }
        } else if (c.state === "sit" || ((c.state === "loaf" || c.state === "curl") && c.phase === "in")) {
          var k = f - c.since;
          if (k === 18) { o.mouth = "smile"; }
          if (k === 36) {
            if (!c.onLaptop) { setActivity(v, v.poses.petcat ? "petcat" : "pet", 99); v.lookTarget = aimAt(v, c.x, catY() - 6); }
            else if (v.poses.petlap) { setActivity(v, "petlap", 99); }      // T88: an arm goes in behind the screen to stroke her back, the hand out of sight
            faceOf(v, { brows: null, mouth: "smile" }); c.shut = true;
          }
          if (k === 84) { c.shut = false; c.state = "walk"; c.phase = "leave"; c.dir = c.home < c.x ? -1 : 1; c.left = f; setActivity(v, "underdesk", 99); faceOf(v, { mouth: "neutral" }); v.lookTarget = { x: 0, y: 1 }; }
        } else if (c.phase === "leave") {
          c.x += 3 * c.dir;
          if (!c.again && f - c.left === 9) { c.again = true; c.dir = -c.dir; c.phase = "in"; faceOf(v, { brows: "up" }); }
        }
      },
      drawFront: function (t, f) {
        var c = actors.cat, v = actors.victim, lap = c.onLaptop && v.poses.type && v.poses.type.props.laptop;
        drawMaker(Math.round(c.x), Math.round(c.y), c.state, c.state === "sit" && c.onLaptop ? 1 : c.dir, f, c.blink);
        if (lap && !v.hidden && v.drawn && !/^type/.test(v.drawn.name)) { var o = origin(v); blit(lap, o.x, o.y); }   // T89: the laptop in front of her, frontmost (typing, his pose draws it and she is not near)
      },
      end: catEnd
    },
    // Ilinca rolls off for coffee and comes back with two mugs. Shelved (T128, COFFEE_RUN): it never starts. If it comes
    // back, the mugs she brings are the two standing on the desk (drawStandingMug), not two more.
    coffee: {
      dur: 15,
      when: function () { return COFFEE_RUN && ilinca.activity !== "coffee" && cole.activity !== "coffee" && !soldering(); },   // (T48: his mug and hands lie where the board and the tools would)
      steps: [
        [0, function () { setActivity(ilinca, "rest", 99); lookAt(ilinca, cole.x, faceLevel(cole)); ilinca.mouth = "smile"; }],
        [0.8, function () { lookAt(cole, ilinca.x, faceLevel(ilinca)); cole.nodAt = frame + 2; cole.mouth = "smile"; }],
        [1.6, function () { actors.away = { dir: ilinca.x > cole.x ? 1 : -1, phase: "out" }; }],
        [8.5, function () { actors.away.phase = "in"; setActivity(ilinca, "carry", 99); }],
        [11.5, function () { setActivity(cole, "coffee", 99); setActivity(ilinca, "coffee", 99); neutral(cole); cole.mouth = "smile"; }]
      ],
      update: function (t, f) {
        var a = actors.away; if (!a) { return; }
        var gone = (a.dir > 0 ? W - ilinca.x : ilinca.x) + 40;
        if (a.phase === "out") { if (Math.abs(ilinca.slide) < gone) { ilinca.slide += 9 * a.dir; } else { ilinca.hidden = true; } }
        else if (a.phase === "in") { ilinca.hidden = false; ilinca.slide -= 9 * a.dir; if (a.dir * ilinca.slide <= 0) { ilinca.slide = 0; a.phase = "home"; } }
      },
      end: function () { ilinca.slide = 0; ilinca.hidden = false; ilinca.hold = null; extras = extras.filter(function (e) { return e.kind !== "mug"; }); }
    },
    // Shake break: Cole mixes the shaker, sets it down on the desk in front of him and slides it across to Ilinca (Cole's
    // pick, round 31: "Slide it"; nobody moves in their seat). It slides along the desk top toward the front edge, slowing
    // (4 px a frame at first, never more), and stops at her left, clear of her laptop, paper and mug and of his hands; she
    // keeps working until it is almost there, reaches for it, lifts it and drinks, and sets it down where she took it.
    // Her laptop or paper stays on the desk meanwhile (T48); a mug she was drinking from stands at her side again as her
    // hand leaves it for the shaker (T128). Frame numbers below are counted from the push.
    shake: {
      dur: 11.5,
      when: function () { return SCENE_ON.shake && !soldering(); },        // (never while he solders: the shaker would slide through his tools on the desk)
      steps: [
        [0, function () { setActivity(cole, "shake", 99); faceOf(cole, { mouth: "smile", look: { x: 0, y: 0 }, turn: 0 }); }],
        // he stops shaking and holds it on the desk top for a moment (shake2: the shaker 3 px above where it will stand)
        [2.6, function () { setActivity(cole, "setdown", 99); lookAt(cole, ilinca.x, faceLevel(ilinca)); cole.mouth = "smile"; lookAt(ilinca, cole.x, faceLevel(cole)); faceOf(ilinca, { brows: "up", mouth: "smile" }); }],
        // he lets go and it slides (the hands pushing it are still to be drawn: until then the hands come up, open)
        [2.9, function () { setActivity(cole, "talk", 99); actors.shaker = { state: "slide", t0: frame }; }]
      ],
      update: function (t, f) {
        var s = actors.shaker; if (!s) { return; }
        var k = f - s.t0, n = shakerSlide().n;
        if (s.state === "slide" && (k >= n - 3 || (L.shake.reach && shakerAt(k).x >= shakerSlide().x1 - L.shake.reach)) && !s.reached) {   // nearly there (on a phone, 6 px from its stop): she leaves her work and reaches for it
          s.reached = true;
          if (ilinca.activity === "type" || ilinca.activity === "write") { ilinca.deskProp = ilinca.activity; }
          setActivity(ilinca, "pet", 99); ilinca.brows = null; var q = shakerAt(n); lookAt(ilinca, q.x, q.y - 20);
        }
        if (s.state === "slide" && k >= n + 4) {                           // she lifts it (in between frames still to be drawn)
          s.state = "held"; s.at = f; setActivity(ilinca, "take", 99); lookAt(ilinca, cole.x, faceLevel(cole)); ilinca.mouth = "smile";
          setActivity(cole, "rest", 99); cole.mouth = "smile";
        }
        if (s.state === "held" && f - s.at === 17) { setActivity(ilinca, "drink", 99); ilinca.mouth = "o"; ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: -1 }; }
        if (s.state === "held" && f - s.at === 49 && L.shake.keep) { setActivity(ilinca, "take", 99); ilinca.mouth = "smile"; ilinca.turn = 0; ilinca.nodAt = frame + 1; lookAt(ilinca, cole.x, faceLevel(cole)); }   // (a phone: she keeps it)
        if (s.state === "held" && f - s.at === 49 && !L.shake.keep) { s.state = "down"; s.at = f; setActivity(ilinca, "pet", 99); ilinca.mouth = "smile"; ilinca.turn = 0; ilinca.hold = null; var r = shakerAt(1e6); lookAt(ilinca, r.x, r.y - 20); }   // she sets it down where she took it, her hand on it
        if (s.state === "down" && f - s.at === 6) { setActivity(ilinca, "rest", 99); ilinca.nodAt = frame + 1; lookAt(ilinca, cole.x, faceLevel(cole)); }
      },
      drawFront: function (t, f) {
        var s = actors.shaker; if (!s || s.state === "held") { return; }
        var q = shakerAt(s.state === "down" ? 1e6 : f - s.t0); if (ENV.ready) { propArt("bottle", q.x, q.y); } else { propBottle(q.x, q.y - 1); }
        var d = ilinca.drawn, box = d && PET_HAND.ilinca[d.name];            // her hand on it lies over it
        if (box && !ilinca.hidden) { g.save(); g.beginPath(); g.rect(d.o.x + box[0], d.o.y + box[1], box[2] - box[0], box[3] - box[1]); g.clip(); blit(bodyOf(d.pose), d.o.x, d.o.y); g.restore(); }
      },
      end: function () { ilinca.deskProp = null; }
    },
    // Late: a yawn passes between them.
    latenight: {
      dur: 7, when: function () { return SCENE_ON.lateNight && isDark(hourNow()) && !soldering(); },   // (T48: his yawning arm and his hands at rest lie where the board and the tools would)
      steps: [
        // (re-audit: at his laptop he yawns where he sits, his hands at the keyboard behind the screen, eyes shut, his face
        // tipping back: Y1's hand to his mouth would rise from behind the screen with his wrist exactly on its top edge, as if
        // resting on it; the screen cannot move. Not typing, Y1 as picked)
        // (at 5.0, yawning at his laptop he types on)
        [0, function () { if (cole.activity === "type") { cole.yawnAt = frame; } else { leaveWork(cole); setActivity(cole, "yawn", 99); } cole.mouth = "yawn"; cole.lookTarget = { x: 0, y: -1 }; }],
        [1.8, function () { if (cole.yawnAt) { cole.yawnAt = 0; } else { setActivity(cole, "rubEye", 99); } cole.mouth = "neutral"; }],
        [2.4, function () { lookAt(ilinca, cole.x, faceLevel(cole)); }],
        [3.2, function () { leaveWork(ilinca); setActivity(ilinca, "yawn", 99); ilinca.mouth = "yawn"; ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: -1 }; }],
        [5.0, function () { [ilinca, cole].forEach(function (p) { if (p.resume) { resumeWork(p, 99); } else if (p.activity !== "type") { setActivity(p, "rest", 99); } }); ilinca.mouth = "smile"; lookAt(cole, ilinca.x, faceLevel(ilinca)); cole.mouth = "smile"; }]
      ]
    },
    // A bigger spark while soldering: a puff of smoke from the board, he starts back, then puts a hand to his head,
    // frustrated (T38: "instead of looking frustrated or surprised I do a little dance"); she looks over, sympathetic.
    spark: {
      dur: 6.5, when: function () { return SCENE_ON.spark && cole.activity === "solder"; },
      steps: [
        [0, function () { var tip = posePoint(cole, "tip"); actors.puff = { t0: frame, x: tip ? tip.x : cole.x + 11, y: tip ? tip.y - 1 : DESK_Y - 12 }; }],   // at the iron's tip, whichever way he holds it
        [0.25, function () { var d = cole.drawn; cole.benchFrom = d && /^solder/.test(d.name) ? d.name : "solder"; faceOf(cole, { brows: "up", mouth: "o" }); setActivity(cole, "startle", 99); cole.lookTarget = { x: 0, y: 0 }; }],   // the station and the board stay where they are
        [0.8, function () { lookAt(ilinca, cole.x, faceLevel(cole)); faceOf(ilinca, { brows: "up", mouth: "o" }); }],
        [1.4, function () { setActivity(cole, "facepalm", 99); faceOf(cole, { brows: "down", mouth: "flat" }); cole.blink = 6; }],
        [3.0, function () { faceOf(ilinca, { brows: "sad", mouth: "smile" }); }],
        [4.4, function () { setActivity(cole, "solder", 99); cole.benchFrom = null; faceOf(cole, { brows: "down", mouth: "flat" }); }],
        [5.6, function () { faceOf(cole, { brows: null, mouth: "neutral" }); ilinca.mouth = "smile"; ilinca.brows = null; ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: 1 }; }]
      ],
      end: function () { cole.benchFrom = null; },
      drawFront: function (t, f) {
        var pf = actors.puff; if (!pf) { return; }
        var k = f - pf.t0, cx = pf.x, cy = pf.y;
        if (k < 3) { px(cx, cy - 3, C.sun); px(cx - 3, cy, C.sun); px(cx + 3, cy - 1, C.sun); px(cx + 1, cy - 5, C.white); px(cx - 2, cy - 4, C.white); }
        if (k < 18) { for (var i = 0; i < 3; i++) { var wy = cy - 2 - Math.round(k * 1.4) - i * 2; px(cx + ((k + i) % 2) * (cx < cole.x ? -1 : 1) - i, wy, k < 9 ? C.smoke : C.smoke2); } }   // a thin wisp off the board, no cloud over him
      }
    },
    // The phone buzzes; good news; a fist pump.
    call: {
      dur: 11,
      when: function () { return ilinca.activity !== "phone" && ilinca.activity !== "call" && !soldering(); },   // (T48: his fist pump and his hands at rest lie where the board and the tools would)
      steps: [
        [0, function () { actors.buzz = { t0: frame }; }],
        [1.4, function () { leaveWork(ilinca); setActivity(ilinca, "call", 99); actors.buzz = null; ilinca.phoneOnDesk = false; faceOf(ilinca, { mouth: "talk", look: { x: 0, y: 0 }, turn: 0 }); }],
        [5.6, function () { ilinca.mouth = "smile"; ilinca.nodAt = frame + 1; }],
        // (re-audit: with her laptop on the desk she tells him with her hands back at it; her talking forearm ran down the
        // screen's edge, touching it. Not from typing: her talking hand, as before)
        [7.0, function () { if (ilinca.resume) { resumeWork(ilinca, 99); } else { setActivity(ilinca, "rest", 99); ilinca.gesture = true; } lookAt(ilinca, cole.x, faceLevel(cole)); ilinca.mouth = "talk"; lookAt(cole, ilinca.x, faceLevel(ilinca)); }],
        [8.6, function () { ilinca.gesture = false; ilinca.mouth = "laugh"; leaveWork(cole); setActivity(cole, "fistpump", 99); cole.mouth = "laugh"; }],
        [10.2, function () { if (cole.resume) { resumeWork(cole, 99); } else { setActivity(cole, "rest", 99); } if (ilinca.resume) { resumeWork(ilinca, 99); } cole.mouth = "smile"; ilinca.mouth = "smile"; }]
      ],
      // (T128: her mug stands above and right of the phone, where the buzz's two marks went up; they go down to its left now, on
      // the desk top in front of her, below her sleeves in every pose she can take while it buzzes)
      drawFront: function (t, f) { var b = actors.buzz; if (b && ilinca.phoneOnDesk) { var x = phoneSpot() - ((f % 2) ? 1 : 0), py = deskAt(0.5); var side = x > ilinca.x ? 1 : -1; rect(x - 5, py - 2, 10, 2, C.phone); hline(x - 4, py - 2, 8, C.phoneTop); px(x - 7 * side, deskAt(0.5) + 1, C.greyLight); px(x - 9 * side, deskAt(0.5) + 3, C.greyLight); } }   // the one phone, hopping a pixel to the left and back (T128 follow-up: between her sleeves and her mug there is room for nothing more)
    }
  };
  var SCENARIO_NAMES = Object.keys(SCENARIOS);
  // Back to a clean start (the approval page, between one scenario and the next): no scenario, no conversation, nothing
  // left on the desk, nobody hidden, holding anything, or mid-greeting.
  function resetAll() {
    if (scenario && scenario.end) { scenario.end(); }
    scenario = null; actors = {}; convo = null; extras = [];
    people.forEach(function (p) {
      p.react = null; p.talking = false; p.gesture = false; p.turn = 0; p.turnUntil = 0; p.brows = null; p.mouth = "neutral"; p.hold = null; p.hidden = false; p.slide = 0;
      p.held = false; p.laptopOut = false; p.keepProps = null; p.deskProp = null; p.resume = null; p.yawnAt = 0; p.benchFrom = null; p.catLift = null; p.petFrom = null; p.nodAt = 0; p.nod = 0; p.bob = 0; p.smileUntil = 0; p.lookTarget = { x: 0, y: 1 };
    });
  }
  function pickScenario() {
    var order = SCENARIO_NAMES.slice().sort(function () { return Math.random() - 0.5; });
    for (var i = 0; i < order.length; i++) { if (startScenario(order[i])) { return order[i]; } }
    return null;
  }

  /* ---------- pointer ---------- */
  var pointer = { x: 0, y: 0, at: -1e9, inside: false };
  function toScene(cx, cy) {
    var r = canvas.getBoundingClientRect();
    return { x: (cx - r.left) / r.width * W, y: (cy - r.top) / r.height * H, near: cx > r.left - r.width * 0.5 && cx < r.right + r.width * 0.5 && cy > r.top - r.height && cy < r.bottom + r.height };
  }
  window.addEventListener("pointermove", function (e) {
    var s = toScene(e.clientX, e.clientY); if (!s.near) { return; }
    pointer.x = s.x; pointer.y = s.y; pointer.at = Date.now(); pointer.inside = s.x >= 0 && s.x <= W && s.y >= 0 && s.y <= H;
  }, { passive: true });
  canvas.addEventListener("pointerdown", function (e) {
    var s = toScene(e.clientX, e.clientY);
    pointer.x = s.x; pointer.y = s.y; pointer.at = Date.now() + 1500; pointer.inside = true;
    var target = null;
    for (var i = 0; i < people.length; i++) { if (!people[i].hidden && Math.abs(s.x - people[i].x) < 32 && s.y > DESK_Y - people[i].art.desk - 4 && s.y < DESK_FRONT + 4) { target = people[i]; } }
    if (target) { react(target); } else { people.forEach(function (p) { p.lookTarget = aimAt(p, s.x, s.y); }); }
  });
  function aimAt(p, x, y) { var dx = x - p.x, dy = y - eyeY(p); return { x: Math.abs(dx) < 14 ? 0 : (dx < 0 ? -1 : 1), y: dy < -22 ? -1 : (dy > 30 ? 1 : 0) }; }

  // A click on one of them: a brief look at you, a nod, a smile and a casual wave, from that one only, then back to
  // what they were doing. Now and then the one you clicked turns and tells the other, who then says hello the same way.
  function react(p) {
    if (scenario || p.react) { return; }
    var o = other(p); greet(p, (review && review.relay !== undefined ? review.relay : Math.random() < 0.25) && !o.hidden && !o.react);
  }
  function greet(p, relay) {
    p.react = relay ? "relay" : "greet"; p.greetAt = frame; p.greetStep = 0; p.greetAct = p.activity;
    p.greetKind = p === cole && !SCENE_ON.coleWave ? "nod" : (review && review.greet) || (Math.random() < 0.5 ? "nod" : "wave");   // T54: a nod or a wave, not both (go-live: he nods, SCENE_ON.coleWave)
    p.reactUntil = frame + Math.round((relay ? 1.7 : p.greetKind === "nod" ? 1.5 : 2.2) * FPS);
  }
  function stepGreet(p, f) {
    if (p.react !== "greet" && p.react !== "relay") { return; }
    var k = (f - p.greetAt) / FPS, o = other(p);
    if (p.react === "relay") {
      if (p.greetStep === 0) { p.greetStep = 1; lookAt(p, o.x, faceLevel(o)); p.mouth = "talk"; p.talking = true; p.gesture = p.greetAct === "rest"; }
      if (k >= 1.2 && p.greetStep === 1) { p.greetStep = 2; p.talking = false; p.gesture = false; p.mouth = "smile"; p.smileUntil = f + 2 * FPS; if (!o.react) { greet(o, false); } }
      return;
    }
    if (p.greetStep === 0) { p.greetStep = 1; p.turn = 0; p.lookTarget = { x: 0, y: 0 }; p.mouth = "smile"; p.brows = null; }
    if (p.greetKind === "nod") {                                         // a look, a smile and a nod
      if (k >= 0.35 && p.greetStep === 1) { p.greetStep = 2; p.nodAt = f; }
      if (k >= 1.3 && p.greetStep === 2) { p.greetStep = 4; p.smileUntil = f + 2 * FPS; }
      return;
    }
    if (k >= 0.3 && p.greetStep === 1) { p.greetStep = 3; setActivity(p, "wave", 99); }   // a look, a smile and a casual wave
    if (k >= 1.9 && p.greetStep === 3) { p.greetStep = 4; setActivity(p, p.greetAct, 6 + Math.random() * 6); p.smileUntil = f + 2 * FPS; }
  }

  /* ---------- light: a sun patch by day, a warm low sun at dusk, blue dark with warm pools at night ---------- */
  function drawSunPatch(h) {
    var day = (1 - nightAmount(h)) * (h > 6 && h < 19.5 ? 1 : 0); if (day <= 0.05) { return; }
    var dusk = duskAmount(h), col = dusk > 0.3 ? "rgba(255,170,90," + (0.16 * day).toFixed(3) + ")" : "rgba(255,240,200," + (0.20 * day).toFixed(3) + ")", reach = 40 + dusk * 30;
    for (var y = WIN.y + 6; y < DESK_Y; y++) { var t = (y - WIN.y) / (DESK_Y - WIN.y); rect(WIN.x - 10 - Math.round(t * reach), y, WIN.w + 6 - Math.round(t * 8), 1, col); }
  }
  function pool(cx, top, bottom, w0, w1, strength) {
    // light falling in a cone: 'overlay' warms and lifts what is lit and leaves black black; a faint haze on top
    g.save(); g.globalCompositeOperation = "overlay";
    for (var y = top; y < bottom; y++) { var t = (y - top) / (bottom - top), half = Math.round(lerp(w0, w1, t)); rect(cx - half, y, half * 2, 1, "rgba(255,214,150," + ((0.9 - t * 0.25) * strength).toFixed(3) + ")"); }
    g.restore();
    for (var y2 = top; y2 < bottom; y2++) { var t2 = (y2 - top) / (bottom - top), h2 = Math.round(lerp(w0, w1, t2)); rect(cx - h2, y2, h2 * 2, 1, "rgba(255,220,150," + (0.05 * strength).toFixed(3) + ")"); }
  }
  function drawNight(h, f) {
    var n = nightAmount(h), d = duskAmount(h) * (1 - n);
    if (ENV.ready) { drawNightArt(h, f, n, d); return; }
    if (d > 0.02) { rect(0, CEIL, W, H - CEIL, "rgba(255,150,80," + (0.10 * d).toFixed(3) + ")"); }
    if (n <= 0.02) { return; }
    rect(0, CEIL, W, DESK_Y - CEIL, "rgba(14,18,46," + (0.40 * n).toFixed(3) + ")"); rect(0, DESK_Y, W, H - DESK_Y, "rgba(14,18,46," + (0.38 * n).toFixed(3) + ")");
    drawWindow(h, f);                                                    // the city stays bright
    pool(L.pendant, 30, DESK_FRONT + 4, 44, 160, n * 0.32);              // the pendant: three nested cones, so its edge is soft
    pool(L.pendant, 30, DESK_FRONT + 4, 26, 104, n * 0.3);
    pool(L.pendant, 30, DESK_FRONT + 4, 10, 52, n * 0.26);
    if (lamp.on) { pool(Math.round(lamp.hx), Math.round(lamp.hy) + 9, DESK_FRONT, 10, 28, n * 0.4); }
    rect(0, DESK_Y, W, DESK_DEEP, "rgba(255,224,160," + (0.07 * n).toFixed(3) + ")");
  }

  // The generated room at night: everything but the window dims to blue (the city stays bright behind the glass);
  // each lamp that is on throws a warm slanting pool on the desk and whoever sits under it.
  function drawNightArt(h, f, n, d) {                                    // on the front layer: only what is drawn there darkens
    g.save(); g.globalCompositeOperation = "source-atop";
    if (d > 0.02) { rect(0, 0, W, H, "rgba(255,150,80," + (0.10 * d).toFixed(3) + ")"); }
    if (n > 0.02) { rect(0, 0, W, H, "rgba(14,18,46," + (0.46 * n).toFixed(3) + ")"); }
    g.restore();
    if (n <= 0.02) { return; }
    fgCopyX.clearRect(0, 0, W, H); fgCopyX.drawImage(fg, 0, 0);          // what the layer covers, before the light
    var pim = ENV.img["pendant-on"];
    if (pim) {                                                           // the ceiling lights are on: their shades glow, their light falls on the desk
      L.art.pendants.forEach(function (x) {
        g.drawImage(pim, Math.round(x - pim.width / 2), PENDANT_RIM - pim.height);
        pool(x, PENDANT_RIM, DESK_FRONT + 3, 9, 50, n * 0.12); pool(x, PENDANT_RIM, DESK_FRONT + 3, 7, 36, n * 0.12); pool(x, PENDANT_RIM, DESK_FRONT + 3, 5, 22, n * 0.14);   // nested, so the edges stay soft
      });
    }
    if (shadeFig) { beamTmp.width = W; beamTmp.height = H; beamTmpX.drawImage(fg, 0, 0); }   // T84: the layer before the lamps' light
    for (var i = 0; i < 2; i++) {
      if (!lampIsOn(i, h)) { continue; }
      var q = lampGeom(i);
      slantCone(q, n * 0.34, true, 34); slantCone(q, n * 0.30, true, 22); slantCone(q, n * 0.26, true, 12);
      slantCone(q, n * 0.05, false, 30);
    }
    if (shadeFig) {                                                      // his own pixels as they were before it (figureMask)
      beamTmpX.globalCompositeOperation = "destination-in"; beamTmpX.drawImage(figMask, 0, 0); beamTmpX.globalCompositeOperation = "source-over";
      g.drawImage(beamTmp, 0, 0);
    }
    g.save(); g.globalCompositeOperation = "destination-in"; g.drawImage(fgCopy, 0, 0); g.restore();   // light falls on things, not into the window
  }

  /* ---------- the frame loop ---------- */
  var running = false, visible = true, lastTick = 0;
  function tick(now) {
    if (!running) { return; }
    requestAnimationFrame(tick);
    if (now - lastTick < 1000 / FPS) { return; }
    lastTick = now; frame++; update(frame); render(frame);
  }
  function update(f) {
    var h = hourNow(), pointerActive = (!review || review.pointer) && (Date.now() - pointer.at) < 2500;
    for (var i = 0; i < people.length; i++) {
      var p = people[i];
      stepGreet(p, f);
      if (p.react && f >= p.reactUntil) { p.react = null; p.mouth = p.smileUntil > f ? "smile" : "neutral"; p.brows = p.activity === "think" ? "down" : null; p.bob = 0; }
      if (p.turnUntil && f >= p.turnUntil && !convo && !scenario) { p.turn = 0; p.turnUntil = 0; }
      if (p.smileUntil && f >= p.smileUntil) { if (p.mouth === "smile") { p.mouth = "neutral"; } p.smileUntil = 0; }
      p.actFrame++;
      if (f >= p.actUntil && !p.react && !scenario) { nextActivity(p); }
      if (p.nodAt && f >= p.nodAt) { var k = f - p.nodAt; p.nod = (k < 10) ? [0, 1, 1, 1, 0, 0, 1, 1, 1, 0][k] : 0; if (k >= 10) { p.nodAt = 0; p.nod = 0; } }
      if (p.react) { /* greeting: it sets where they look */ }
      else if (pointerActive && !scenario) { p.lookTarget = aimAt(p, pointer.x, pointer.y); if (!convo) { p.turn = p.lookTarget.x; } }
      else if (!convo && !p.react && !scenario) {
        var a = p.activity; p.turn = 0;
        if (p.workLook[a]) { p.lookTarget = { x: p.workLook[a][0], y: p.workLook[a][1] }; }
        else if (a === "think") { p.lookTarget = { x: (f >> 5) % 2 ? -1 : 1, y: -1 }; }
        else if (a === "coffee") { p.lookTarget = { x: 0, y: 0 }; }
        else { p.lookTarget = still ? { x: 0, y: 0 } : { x: ((f >> 4) + i) % 3 - 1, y: 0 }; }
      }
      p.look.x += (p.lookTarget.x - p.look.x) * 0.6; p.look.y += (p.lookTarget.y - p.look.y) * 0.6;
      if (still) { p.blink = 0; } else if (p.blink > 0) { p.blink--; } else if (--p.nextBlink <= 0) { p.blink = 2; p.nextBlink = 24 + Math.random() * 48; }
      if (!p.react && !(scenario && scenario.name === "spark")) { p.bob = 0; }
      p.tilt = stretching(p) ? 0 : yawnTip(p) ? -1 : p.yawnAt ? 0 : (p.nod > 0 || (p.workLook[p.activity] && !convo && !p.react && !(pointerActive && !scenario))) ? 1 : 0;
      p.lookDown = !!p.headDown && !stretching(p) && p.activity !== "stretch" && p.activity !== "coffee" && p.activity !== "holdcup" && p.activity !== "yawn" && p.activity !== "rubEye" && (p.nod > 0 || (!p.react && p.look.y > 0.5));     // at the work, the cat, a pointer on the desk; never over a coffee (T43)
      if (!still) { stepExpression(p, f); }
    }
    if (pointer.inside && pointerActive && !saidHello && !convo && !scenario && f > 4 * FPS) {          // the nearer one glances over and smiles
      saidHello = true; var near = Math.abs(pointer.x - cole.x) < Math.abs(pointer.x - ilinca.x) ? cole : ilinca;
      if (!near.react) { near.mouth = "smile"; near.smileUntil = f + 2 * FPS; }
    }
    if (!scenario && !convo && !review && f >= nextScenarioAt && !pointerActive && !cole.react && !ilinca.react && cole.activity !== "stretch") { if (!pickScenario()) { nextScenarioAt = f + 15 * FPS; } }   // (go-live: not mid-stretch, which a scene would hold for its whole length)
    stepScenario(f);
    stepConvo(f);
    updateLamp(h);
  }

  // Small changes of expression between everything else, so neither of them wears one face all the time.
  var EXPRESSIONS = {
    cole: [["smile", null, 2.5, 3], ["smirk", null, 2, 2], [null, "up", 1.2, 1], ["grin", null, 1.6, 1], ["flat", "down", 1.8, 1]],
    ilinca: [["smile", null, 2.5, 3], ["smirk", null, 2, 2], ["purse", "down", 1.8, 2], [null, "up", 1.2, 1], ["grin", null, 1.6, 1], ["neutral", "sad", 1.4, 1]]
  };
  function stepExpression(p, f) {
    if (scenario || convo || p.react || p.talking) { return; }
    if (p.exprUntil && f >= p.exprUntil) { p.exprUntil = 0; p.mouth = "neutral"; p.brows = p.activity === "think" ? "down" : null; p.nextExprAt = f + (5 + Math.random() * 9) * FPS; return; }
    if (!p.exprUntil && f >= p.nextExprAt) {
      var list = EXPRESSIONS[p.name], total = 0, r, e = list[0];
      list.forEach(function (x) { total += x[3]; }); r = Math.random() * total;
      for (var i = 0; i < list.length; i++) { r -= list[i][3]; if (r <= 0) { e = list[i]; break; } }
      if (e[0]) { p.mouth = e[0]; } if (e[1]) { p.brows = e[1]; }
      p.exprUntil = f + Math.round(e[2] * FPS);
    }
  }

  function render(f) {
    var h = hourNow(), t = scenario ? (f - scenario.t0) / FPS : 0, dark = isDark(h), art = ENV.ready, back = g;
    if (art) {
      drawWindowView(h, f);                                              // behind the glass, on the back layer
      if (scenario && scenario.drawOutside) { scenario.drawOutside(t, f); }   // outside the window (the pigeon on the ledge)
      g = fgx; g.clearRect(0, 0, W, H);                                  // the room and everyone in it, on the front layer
      g.drawImage(ENV.img["room-" + layoutName], 0, 0); g.drawImage(ENV.img["painting-" + layoutName], L.art.painting.x, L.art.painting.y); drawClockArt(h); drawSunPatch(h);
      drawPendantArt(dark);
    }
    else { drawRoom(h); drawWindowView(h, f); if (scenario && scenario.drawOutside) { scenario.drawOutside(t, f); } drawWindowFrame(); drawSunPatch(h); drawPendant(dark); drawLampArm(); }
    if (art) { drawLampsArt(h, "back"); }
    if (scenario && scenario.drawBack) { scenario.drawBack(t, f); }
    people.forEach(drawSheetBehind);                                    // a paper's top edge above the desk line, behind them
    for (var i = 0; i < people.length; i++) { drawCharacter(people[i], f); }
    if (scenario && scenario.drawMid) { scenario.drawMid(t, f); }        // between them and the desk (a cat on a keyboard is drawn in front now, the laptop over her: T89)
    if (art) { g.drawImage(ENV.img["desk-" + layoutName], 0, 0); } else { drawDesk(); }
    people.forEach(drawDeskPropUnder); people.forEach(drawOnDesk); people.forEach(drawLaptopOut); people.forEach(drawDeskPropOver);
    if (art) { drawLampsArt(h, "front"); } else { drawLampBase(); }
    steamShown = []; steamBox = {}; drawProps(f);
    if (art) { steamMark(); }                                            // (T128: the steam goes on last, where nothing covers it)
    if (!art) { drawLampCone(); drawLamp(); }
    people.forEach(drawNamePlate);
    if (scenario && scenario.drawFront) { scenario.drawFront(t, f); }
    if (art) { people.forEach(function (p) { if (catBehindMug(p)) { drawStandingMug(p, f); } }); steamMark(); }   // (a mug Maker walks behind)
    people.forEach(drawPetHand);
    shadeFig = art && dark && lampIsOn(0, h) && handsOffWork(cole) && !cole.hidden;   // T84: his figure keeps out of his lamp's beam
    if (shadeFig) { figureMask(cole, f); }
    var glow = dark && art ? bulbsShowing(h) : [];                       // (the lamps stand behind them now: only what still shows)
    if (art) { steamKept(); }
    drawNight(h, f);
    if (art) { g = back; g.drawImage(fg, 0, 0); }
    if (dark) { if (art) { glow.forEach(function (q) { px(q[0], q[1], C.bulb); }); } else { drawPendant(true); drawLamp(); } }   // the bulbs glow through the dark
    if (art) { steamDraw(); }
    blit2();
  }
  function blit2() { ctx.imageSmoothingEnabled = false; ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.drawImage(off, 0, 0, canvas.width, canvas.height); }

  /* ---------- layout + sizing ---------- */
  function applyLayout(name) {
    if (name === layoutName) { return; }
    var prev = layoutName ? { cole: cole.x, ilinca: ilinca.x, W: W, winX: WIN.x } : null;
    layoutName = name; L = LAYOUTS[name]; W = L.W; H = L.H; WIN = ENV.ready ? L.art.win : L.win; off.width = W; off.height = H;
    fg.width = fgCopy.width = W; fg.height = fgCopy.height = H;
    cole.x = L.cole; ilinca.x = L.ilinca; lamp.base = L.lamp; var idle = lampIdle(); lamp.hx = lamp.tx = idle.x; lamp.hy = lamp.ty = idle.y;
    makeStars();
    if (prev) { remapAcross(prev); } else { extras = []; }
    canvas.setAttribute("width", W); canvas.setAttribute("height", H);
  }
  // T63 ("When switched between narrow and wide, some objects that should stay connected become disconnected, eg maker
  // sitting in front of cole is moved far to the side"): on a layout switch whatever was placed by someone keeps its place
  // beside them (Maker lying in front of Cole, a plane or a bottle on the desk), the pigeon keeps its place on the sill,
  // anything else scales with the room.
  function remapAcross(prev) {
    function mapX(x) {
      var dc = Math.abs(x - prev.cole), di = Math.abs(x - prev.ilinca);
      if (Math.min(dc, di) < 90) { return dc <= di ? cole.x + (x - prev.cole) : ilinca.x + (x - prev.ilinca); }
      if (x < 0) { return x; } if (x > prev.W) { return W + (x - prev.W); }
      return Math.round(x * W / prev.W);
    }
    var c = actors.cat;
    if (c) { c.x = mapX(c.x); if (c.spot !== undefined) { c.spot = mapX(c.spot); } if (c.home !== undefined) { c.home = c.home < 0 ? c.home : W + 40; } }
    if (actors.bird) { actors.bird.x = WIN.x + (actors.bird.x - prev.winX); }
    if (actors.plane) { actors.plane.x = mapX(actors.plane.x); actors.plane.x0 = mapX(actors.plane.x0); }
    if (actors.puff) { actors.puff.x = mapX(actors.puff.x); }
    extras.forEach(function (e) { e.x = mapX(e.x); });
  }
  function resize() {
    var cw = host.clientWidth || 360;
    applyLayout(cw < 480 ? "narrow" : "wide");
    var scale = cw >= 2 * W ? Math.floor(cw / W) : cw / W;
    var cssW = Math.round(W * scale), cssH = Math.round(H * scale), dpr = Math.min(window.devicePixelRatio || 1, 3);
    canvas.style.width = cssW + "px"; canvas.style.height = cssH + "px";
    canvas.width = Math.round(cssW * dpr); canvas.height = Math.round(cssH * dpr);
    render(frame);
  }
  if (window.ResizeObserver) { new ResizeObserver(resize).observe(host); } else { window.addEventListener("resize", resize); }

  function start() { if (running || reduceMotion) { return; } running = true; lastTick = 0; requestAnimationFrame(tick); }
  function stop() { running = false; }
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; if (visible && !document.hidden) { start(); } else { stop(); } }, { threshold: 0.05 }).observe(host);
  } else { start(); }
  document.addEventListener("visibilitychange", function () { if (document.hidden) { stop(); } else if (visible) { start(); } });

  setActivity(cole, Math.random() < 0.6 ? "solder" : "type", 14); setActivity(ilinca, Math.random() < 0.5 || !SCENE_ON.ilincaWrite ? "type" : "write", 16);
  host.setAttribute("data-live", reduceMotion ? "still" : "on");
  resize();
  if (reduceMotion) { update(0); render(0); }

  window.NutrimaticDesk = {
    setHour: function (h) { hourOverride = (h === null || h === undefined) ? null : +h; updateLamp(hourNow()); render(frame); },
    activity: function (n, a, secs) { setActivity(who(n), a, secs || 10); updateLamp(hourNow()); render(frame); },
    react: function (n) { react(who(n)); render(frame); },
    scenario: function (name) { var ok = startScenario(name); render(frame); return ok; },
    converse: function (i) { startConvo(EXCHANGES[i | 0] || EXCHANGES[0]); stepConvo(frame); render(frame); },
    // candidate hands: pose layers in the figure's exported palette ({b, f, fb, p, pts, oh}, as js/desk-sprites.js has them)
    patchPoses: function (n, list) {
      var p = who(n), a = p.art; if (!p.poses0) { p.poses0 = {}; Object.keys(p.poses).forEach(function (k) { p.poses0[k] = p.poses[k]; }); }
      Object.keys(list || {}).forEach(function (k) {
        var q = list[k], props = {};
        Object.keys(q.p || {}).forEach(function (m) { props[m] = bake(q.p[m], a.pal); });
        p.poses[k] = { body: bake(q.b, a.pal), bodyN: q.bn ? bake(q.bn, a.pal) : null, front: q.f ? bake(q.f, a.pal) : null, frontBody: q.fb ? bake(q.fb, a.pal) : null, over: q.o ? bake(q.o, a.pal) : null, pts: q.pts || {}, props: props, ownHead: !!q.oh, under: q.u || null };
      });
      render(frame); return Object.keys(list || {}).length;
    },
    still: function (on) { still = !!on; people.forEach(function (p) { p.blink = 0; p.mouth = p.restMouth || "neutral"; p.brows = p.activity === "think" ? "down" : null; }); render(frame); },
    unpatchPoses: function (n) { var p = who(n); if (p.poses0) { p.poses = p.poses0; p.poses0 = null; } render(frame); },
    review: function (o) {
      review = o || null; resetAll();
      if (review) { people.forEach(function (p) { if (review[p.name]) { setActivity(p, review[p.name], 1e4); } }); }
      else { people.forEach(nextActivity); nextScenarioAt = frame + 20 * FPS; nextConvoAt = frame + 9 * FPS; }
      updateLamp(hourNow()); render(frame);
    },
    face: function (n, o) { var p = who(n); faceOf(p, o || {}); if (o && o.look) { p.look = { x: o.look.x, y: o.look.y }; } if (o && o.blink) { p.blink = 2; } p.actUntil = frame + 1e6; render(frame); },
    step: function (n) { for (var i = 0; i < (n || 1); i++) { frame++; update(frame); } render(frame); },
    poses: function (n) { return Object.keys(who(n).poses); },
    scenesOn: function () { return JSON.parse(JSON.stringify(SCENE_ON)); },   // (go-live: which scenes are switched on)
    state: function () { return { layout: layoutName, size: [W, H], cole: cole.activity, ilinca: ilinca.activity, poses: [cole.drawn ? cole.drawn.name : null, ilinca.drawn ? ilinca.drawn.name : null], set: setIndex, hour: hourNow(), running: running, convo: !!convo, scenario: scenario ? scenario.name : null, lamp: { on: lamp.on, x: Math.round(lamp.hx) }, art: ENV.ready, lamps: [lampIsOn(0, hourNow()), lampIsOn(1, hourNow())], cat: actors.cat ? { x: Math.round(actors.cat.x), y: Math.round(actors.cat.y || 0), state: actors.cat.state, behind: !!actors.cat.behind } : null, laptopOut: [cole.laptopOut, ilinca.laptopOut], mugs: [mugStands(cole), mugStands(ilinca)], down: [cole.lookDown, ilinca.lookDown], react: [cole.react, ilinca.react], review: !!review, work: [workOnDesk(cole), workOnDesk(ilinca)] }; }
  };
})();
