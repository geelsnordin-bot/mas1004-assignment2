# Log

One entry for each recipe, selection or Track B model you train, newest at
the bottom. The numbers come from `experiments.csv`. "Why" and "what it means"
are in your own words: your agent asks you for them and does not make them up.
End the log with your plan for what to try next.

<!-- The form of an entry:

## <date> <tag> (Track A or B)
- changed: what is different from the run before
- why: your reason
- validation: 0.000 (before: 0.000)
- what it means: what you think the result says
-->

## 2026-11-03 baseline (Track A)
- changed: nothing, the starter recipe, trained with seed 0 and seed 1
- why: a starting point, and to see how much the score moves by chance
- validation: seed 0 0.496 (seoul 0.568, busan 0.383, tokyo 0.637, osaka 0.343, taipei 0.547); seed 1 0.495 (seoul 0.580, busan 0.399, tokyo 0.608, osaka 0.371, taipei 0.517)
- what it means: "The difference of only 0.001 shows that the results barely change between the two random seeds. So the baseline seems stable."

## 2026-11-06 manual_drop (Track A)
- changed: left out 3019 training photos from my own control list (track_a/manual_list.csv, reasons in track_a/dropped.csv): food, animals, museum pieces, press events and uniforms, aeroplanes, a car show, black-and-white, 360-degree photos, long series by one photographer, and three Busan videos with overlays
- why: "get the junk out that had nothing characteristic of the city"
- validation: 0.492 (seoul 0.585, busan 0.376, tokyo 0.639, osaka 0.367, taipei 0.495) (before: 0.496 / 0.495)
- what it means: "I expected a better score since junk goes out that had nothing characteristic of the city and the model otherwise stays the same, so the score would go up in percentage terms; so this is a bit of a shock"

## 2026-11-07 no_flip (Track A)
- changed: removed `T.RandomHorizontalFlip()` from train_transform; same selection as manual_drop
- why: "The recipe randomly mirrors every photo horizontally. Because of that, text ends up in mirror image and cars seem to drive on the wrong side of the road. Precisely that driving direction can help to tell cities apart: in Japan people drive on the left, in Korea and Taiwan on the right. So my expectation was that the model would pick up this clue better if I turned the mirroring off."
- validation: 0.491 (seoul 0.597, busan 0.360, tokyo 0.627, osaka 0.344, taipei 0.528) (before: 0.492, manual_drop)
- what it means: "That turned out not to be the case: the score stayed the same. The model apparently relies little on such small details and recognises a city mainly by the overall picture, such as buildings, colours and streetscape."

## 2026-11-07 b_starter (Track B)
- changed: nothing, src/train_b.py with its default settings (ResNet18, 224 px, 4 epochs, all training photos)
- why: (to be filled in by Nordin)
- validation: 0.489 (seoul 0.580, busan 0.360, tokyo 0.591, osaka 0.358, taipei 0.557)
- what it means: (to be filled in by Nordin)

## 2026-11-09 less_zoom (Track A)
- changed: `T.RandomResizedCrop(224, scale=(0.7, 1.0))` instead of `scale=(0.35, 1.0)`; otherwise the same as no_flip
- why: "by seeing more of a photo the model can get a hint which city fits it; say it zooms in and so does not catch the text of a billboard, then choosing becomes a lot harder"
- validation: 0.478 (seoul 0.579, busan 0.344, tokyo 0.611, osaka 0.352, taipei 0.505) (before: 0.491, no_flip)
- what it means: "I think the validation score came out lower because with less random zooming the model kept seeing roughly the same images. Because of this the model may have learned too much from the training photos themselves, instead of recognising the general features of a city. So the model worked well on the training data, but less well on new images during validation."

## 2026-11-09 b_mnv3_448 (Track B)
- changed: MobileNetV3-Large instead of ResNet18, photos of 448 px instead of 224; otherwise 4 epochs like b_starter
- why: "bigger photos with better quality are best, I think, because then it can read text"
- validation: 0.562 (seoul 0.621, busan 0.462, tokyo 0.683, osaka 0.436, taipei 0.608) (before: 0.489, b_starter)
- what it means: (to be filled in by Nordin)

## 2026-11-09 balanced (Track A)
- changed: every city drawn equally often (`sample_weights` gives each photo 1 / the number of photos of its city); otherwise the same as no_flip
- why: (to be filled in by Nordin)
- validation: 0.498 (seoul 0.552, busan 0.415, tokyo 0.554, osaka 0.427, taipei 0.540) (before: 0.491, no_flip)
- what it means: (to be filled in by Nordin)

## 2026-11-09 ema (Track A)
- changed: keep a running average of the weights next to the model (EMA, decay 0.999, roughly the last 1000 steps) and hand in that average; otherwise the same as balanced
- why: (to be filled in by Nordin)
- validation: 0.500 (seoul 0.561, busan 0.429, tokyo 0.530, osaka 0.425, taipei 0.553) (before: 0.498, balanced)
- what it means: (to be filled in by Nordin)

## 2026-11-09 b_mnv3_448_e6_bal (Track B)
- changed: 6 epochs instead of 4, and every city drawn equally often (`--balance`); otherwise the same as b_mnv3_448. Two changes at once, so it cannot be said which of the two made the difference
- why: (to be filled in by Nordin)
- validation: 0.574 (seoul 0.576, busan 0.511, tokyo 0.620, osaka 0.519, taipei 0.645) (before: 0.562, b_mnv3_448)
- what it means: (to be filled in by Nordin)

## 2026-11-10 ema_no_smooth (Track A)
- changed: no more label smoothing in `loss_fn` (was 0.1); otherwise the same as ema
- why: (to be filled in by Nordin)
- validation: 0.507 (seoul 0.570, busan 0.429, tokyo 0.526, osaka 0.422, taipei 0.591) (before: 0.500, ema)
- what it means: (to be filled in by Nordin)

## 2026-11-10 b_mnv3_512_e8_bal (Track B)
- changed: photos of 512 px (the maximum) instead of 448, and 8 epochs instead of 6; otherwise the same as b_mnv3_448_e6_bal. Two changes at once
- why: (to be filled in by Nordin)
- validation: 0.586 (seoul 0.595, busan 0.494, tokyo 0.627, osaka 0.515, taipei 0.700) (before: 0.574, b_mnv3_448_e6_bal)
- what it means: (to be filled in by Nordin)
