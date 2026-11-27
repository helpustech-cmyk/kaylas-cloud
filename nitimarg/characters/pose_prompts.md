# Niti Didi pose prompts

Make the poses once, outside the VPS, with any free image tool (Gemini, Ideogram, Leonardo,
Bing Image Creator). Generate `neutral` first, then attach it as the reference image for every
other pose so her face, glasses and kurta stay the same.

## Master style (paste before every pose)

> Flat 2D cartoon character, simple vector style, thick dark outline, flat colours, no
> gradients, no shadows, no text. Young Indian woman "Niti Didi": round face, big expressive
> dark eyes, small friendly smile, warm brown skin, black hair in a neat bun, round thin-rimmed
> glasses, small red bindi. Bold saffron (#FF9933) kurta with a deep green (#136238) dupatta
> over one shoulder. Upper body visible from the waist up, facing the viewer, centred, plain
> transparent background (or flat white if transparency isn't supported). Portrait 4:5,
> same proportions and line weight in every image.

## Poses (file names the pipeline expects)

| # | File prefix | Pose prompt (add after the master style) |
|---|---|---|
| 1 | `neutral` | Neutral talking, arms relaxed at her sides, calm warm expression. |
| 2 | `happy_pointing` | Happy, big smile, right arm raised pointing to the upper right (where a number appears). |
| 3 | `worried` | Worried, eyebrows raised and tilted, both hands clasped near her chest. |
| 4 | `explaining` | Explaining, both palms open and turned up at waist height, friendly face. |
| 5 | `warning` | Serious warning, right index finger raised next to her face, firm look. |
| 6 | `celebrating` | Celebrating, both arms raised up, big open smile. |
| 7 | `thinking` | Thinking, right hand on chin, eyes looking up and to the side. |
| 8 | `holding_phone` | Holding a smartphone in her right hand, screen turned towards the viewer, slight smile. |

## Two mouth states per pose

For each pose make two images that are identical except for the mouth:

- `<prefix>_closed.png`: mouth closed (small smile, or a flat line for `worried` and `warning`).
- `<prefix>_open.png`: mouth open in a relaxed speaking "aa" shape.

Easiest way: generate the closed version, then ask the tool to edit only the mouth to open
(or open the image in Canva or Photopea, draw the open mouth once, and reuse it on all 8).

## File checklist

- 16 PNG files, transparent background, about 800×1000 px (any 4:5 size works; they are scaled).
- Names exactly as above, for example `warning_open.png`, `warning_closed.png`.
- Copy them to `nitimarg/poses/` on Hermes. Real files are never overwritten by the placeholders.
- Banner and profile picture: reuse `neutral_closed.png` with the channel name (doc section 10).
