# Niti Didi pose prompts (style F: bold 3D mascot)

The approved set is in the Figma file **Niti Didi 3D Character Options** (frames 2:2 to 2:9).
To make more poses, paste the master prompt and change only the POSE line. Ask for a solid
pure white background so `prep-poses` can cut her out automatically.

## Master prompt

> Sleek modern stylised 3D character, crisp high-contrast look, sharp clean silhouette, smooth
> matte-satin materials, YouTube mascot quality. Character sheet consistency: "Niti Didi",
> stylish smart young Indian woman finance explainer, expressive heart-shaped face, large bright
> brown eyes, defined brows, warm brown skin, sleek black hair in a sharp top-knot bun with a
> single wavy strand on the right, bold round black-framed glasses, small red bindi, small gold
> hoop earrings, fitted saffron kurta (#FF9933) with subtle geometric gold print, emerald green
> dupatta (#136238) across her left shoulder, slim gold smartwatch on left wrist.
> POSE: `<pose line>`. Waist-up, centred, same framing as a character turnaround. Strong studio
> key light with a soft saffron rim light. Solid pure white background (#FFFFFF), no shadow on
> background, no text.

## Pose lines

| File | POSE line |
|---|---|
| `neutral` | neutral talking, standing straight facing viewer, arms relaxed at her sides, calm warm friendly smile, mouth closed |
| `happy_pointing` | happy, big bright smile, left hand on hip, right arm raised pointing up to the upper right with index finger as if revealing a big number |
| `worried` | worried and concerned, eyebrows raised and tilted up in the middle, lips pressed, both hands clasped together near her chest, slight head tilt |
| `explaining` | explaining, both palms open and turned up at waist height, friendly engaged smile, eyebrows slightly raised |
| `warning` | serious warning, firm look, brows lowered, right index finger raised next to her face in a "be careful" gesture, left hand on hip |
| `celebrating` | celebrating, both arms raised up in joy with fists, big open happy smile, eyes bright |
| `thinking` | thinking, right hand on chin, eyes looking up and to the side, slight thoughtful half smile, left arm folded across waist |
| `holding_phone` | holding a smartphone in her right hand with the blank bright screen turned towards the viewer, left index finger pointing at the phone screen, helpful confident smile |

## Getting them into the pipeline

1. In Figma, select each pose frame and export it as PNG (2x), named as in the table
   (`neutral.png`, `worried.png`, ...).
2. Copy the files to Hermes, then run
   `python -m nitimarg prep-poses /path/to/exports`.
   This cuts out the white background (keeping white details like the phone screen) and puts the
   files in `nitimarg/poses/`.
3. One image per pose is enough: while she speaks, the renderer adds a small head-bob.
   For true lip-sync, also add `<pose>_open.png` (the same image with the mouth open, e.g.
   edited in Figma or Canva) and rename the first one to `<pose>_closed.png`.

Banner and profile picture: use `neutral.png` with the channel name (doc section 10).
