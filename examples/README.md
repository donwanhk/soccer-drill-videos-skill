# Reference files

Working files lifted from the project these conventions came from. Copy and adapt;
they are not a library to import.

| file | what it shows |
|---|---|
| `nesTheme.ts` | the palette and framebuffer metrics, verbatim |
| `futsal-phase-tracks.ts` | phase keyframes -> interpolated tracks (`actorAt`, `ballAt`, `passInFlight`), and a court mapped at one scale on both axes |
| `soundtrack.tsx` | narration table, ducking, and SFX derived from the drill data |
| `lines.json` | input for `make_narration.py` — colloquial Cantonese with frame budgets |
| `futsal-corner-drill.json` | a full six-phase routine; passes `check_tactics.py` with `--marks 2:7,3:9,4:10 --expect-beaten 3:9@4,3:9@5` |
| `broken-positions.json` | a fixture that FAILS on purpose — defenders behind their man, markers stacked. Use it to confirm the checker still bites. |
