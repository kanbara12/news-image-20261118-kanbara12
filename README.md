# news-image-20261118-kanbara12

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/kanbara12/news-image-20261118-kanbara12/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/kanbara12/news-image-20261118-kanbara12/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One newspaper front page for Wednesday 18 November 2026: 26 stories from six continents. The three lead stories are the Xi–Putin meeting in Shenzhen ahead of the Trump trilateral, Iran firing on US bases in Kuwait and Bahrain, and the Kerch Bridge hit for a second day. Nine more stories carry small illustrations. A world map pins the twelve illustrated stories by number, and the other fourteen run as a numbered list. Every story happened or was first reported that day. Scheduled items are worded as due. Contested claims are marked as claims. The footer names the one big item still to come, the trilateral due on Thursday.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The output is `out/entry.png`, the same 1024 by 1024 front page.

## How it works

render.py draws entry.png at 1024 by 1024. It composites twelve illustrations made for this entry, one per illustrated story, crops each to its panel, and adds a caption bar naming the place. The map is drawn from a short list of continent outlines. main.py only copies that image to the output directory, so the entry runs on the standard library alone and writes the same bytes every time.

---

<sub>Entered on [make.fun](https://make.fun/?ref=wfzk99wk&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
