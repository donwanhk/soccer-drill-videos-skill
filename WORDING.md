# 用詞 — the house vocabulary

Decided by the person, not inferred. When a word here conflicts with what reads naturally,
**this file wins** — consistency across videos matters more than any single sentence, and a
coach watching three of these should not meet three words for the same thing.

## 字幕 vs 旁白

The split is deliberate and stays:

- **字幕（on-screen）is 書面語** — 傳球、移動、球員. A coach screenshots the setup screen and
  sends it to someone; it should read as a written diagram.
- **旁白（narration）is 口語廣東話** — 傳波、郁、企. It should sound like someone standing on
  the grass, not reading a manual.

So the same action is 傳球 on screen and 傳波 spoken. That is not an inconsistency; writing
傳波 on screen, or saying 傳球 aloud, is.

## 龍門類 — two words, not four

| Thing | 字幕 | 旁白 |
|---|---|---|
| Two cones, about 2 m apart | 閘 | 閘 |
| A mini goal | 細龍門 | 細龍門 |
| A full-size goal | 龍門 | 龍門 |

**「大門」is retired.** A real goal is 龍門 whatever its size; a gap between cones is 閘.

## 二過一

- The return pass is **撞牆** — 撞牆波, 做一次撞牆. Not 傳牆.
- The player who plays it back is **隊友**. Not 支援, not 牆.
- The run past the defender afterwards stays **疊瓦跑** / 疊上.

## 逼搶

**逼搶** is the standard noun across 字幕 and 旁白. The verb is **逼** — 逼佢向邊線, 兩個一齊逼.
**「壓迫」is retired**, including inside theme names.

## 搶波時機

The moment the ball gets away from an opponent's foot is **控甩腳**: 等佢控甩腳先搶.
Not 甩腳 on its own.

## 細路仔點稱呼

**「細朋友」唔係一個詞，唔好用。** 廣東話講細路係 **小朋友**。

| 講緊乜 | 用邊個詞 |
|---|---|
| 練習入面嘅人，唔理年齡 | 球員 |
| 特登指細路仔（例如解釋點解 U8 要調淺啲） | 小朋友 |

預設係 **球員** —— 睇片嗰個係教練，佢講緊自己隊波嘅人。寫 小朋友 淨係喺真係講緊
年齡嗰陣先啱。同 [波仔 → 球員](#其他已定嘅詞) 係同一個道理。

## 器材

| Thing | Word |
|---|---|
| A training cone | 雪糕筒 |
| The cone marking a start spot | 起點筒 |
| A bib | 分隊衫 |

**「角錐」is retired.**

## 其他已定嘅詞

These were reviewed and kept as they are:

| Word | Means |
|---|---|
| 球員 | a player — never 波仔 |
| 攻方 / 防守 | the attacking side / the defending side or defender |
| 邊路 | the wide player |
| 傳波、收波、帶波、出球、回傳 | pass, receive, dribble, release, return pass |
| 斷波、搶到波、失波 | intercept, win it, lose it |
| 埋位、輪轉、隊尾、等緊 | take positions, rotation, back of the queue, waiting |
| 底線、邊線、通道、空位、中間 | end line, touchline, channel, space, central area |
| 一打一、二打一、四打二 | 1v1, 2v1, 4v2 |
| 抬頭、側住身、企開角度、企闊啲 | head up, side on, take an angle, stay wide |

## Changing a word later

A word changed here is not just a text edit. Anything in the **narration** has to be
re-synthesised and the video re-rendered; anything on screen needs a re-render. Before
changing one, grep `src/drills/*.json` to see which drills it touches, and say what the
re-render will cost.
