# The World in One Image — Wednesday 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Indodegen/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Indodegen/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A make.fun bounty entry for **news-image-20261118**: sum up 18 November's
world news in one image. Bounty page:
[Sum up 18 November's world news in one image](https://make.fun/bounty/news-image-20261118).

`main.py` is a Python standard-library-only program (no PIL, no network,
no API keys). It draws a 1024×1024 newspaper front-page infographic and
writes it as a PNG. Every glyph comes from a hand-written 5×7 bitmap font
(uppercase A–Z, digits 0–9 and punctuation), scaled by integer factors,
and every icon (plane, bridge, radar drone, sanction document, microchip,
cyclone) is drawn from geometric shapes in code. The PNG encoder is pure
stdlib too (`zlib` + `struct`, RGB, no interlace).

Running the program twice produces byte-identical PNG output: there is no
randomness and no timestamp anywhere in the image or the file.

## How to run

```sh
python3 main.py
```

The image is written to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output` when the variable is not set).

## The stories covered

1. **Trump lands in Manila** — US President Donald Trump arrives in the
   Philippines for Quad talks with India, Japan and Australia, ahead of a
   China visit and the APEC summit.
2. **Ukraine hits Crimean Bridge again** — Ukraine strikes the Crimean
   Bridge for a second straight day, damaging its road section, as Russian
   strikes hit bridges in Kyiv.
3. **Iran drones target US radar in Bahrain** — Iran fires drones at a US
   military radar site in Bahrain; Gulf states report interceptions and an
   all-clear.
4. **UK sanctions Israeli settlement firms** — Britain sanctions eight
   firms over illegal West Bank settlements and a group blocking aid to
   Gaza.
5. **Nvidia's record $115.8bn quarter** — Nvidia reports record quarterly
   revenue, up 103% on a year ago, as it probes its CEO's alleged link to
   a Chinese spy.
6. **Cyclone Akvan bears down on India** — Cyclone Akvan strengthens over
   the Bay of Bengal, putting Andhra Pradesh and Odisha on high alert.

Also: Canada and China extend trade deals as Xi meets Carney ahead of
APEC — MS Dhoni retires from the IPL.

## Layout

- Navy masthead with the date set large: **WEDNESDAY 18 NOVEMBER 2026**
- Lead story panel (Trump in Manila) with a drawn plane icon
- Five more numbered story rows, each with its own drawn icon
- Footer with an "ALSO:" line and a credit line

## License

MIT — see `LICENSE`.
