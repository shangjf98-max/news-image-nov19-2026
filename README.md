# news-image-nov19-2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/shangjf98-max/news-image-nov19-2026/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/shangjf98-max/news-image-nov19-2026/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Draws one newspaper-style image summing up the world news of Thursday 19 November 2026: the first-ever Trump–Xi–Putin trilateral in Shenzhen ending in a four-point Declaration toward Peace, Cyclone Akvan bearing down on India's east coast with 299,000 evacuated in Odisha, Anthropic's record $81.3 billion IPO debuting on Nasdaq and closing at $97.17, GTA 6 launching to a 99/100 first-review score and record livestream audiences, and NASA confirming Voyager 1 as the first human-made object one light-day from Earth.

Everything is drawn in code. `main.py` uses only the Python standard library: a built-in 5x7 bitmap font for all text, rectangles, lines, circles and polygons for every picture element, and a hand-written PNG encoder (zlib + CRC chunks). No fonts, no image files, no network, no generated imagery. Two runs produce byte-identical output (verified: 23,088 bytes, 1024x1024 PNG).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=3h1pepd7&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
