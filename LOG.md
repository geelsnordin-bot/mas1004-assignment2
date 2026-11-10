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
- why: "It was useful to run the original code first, because that way we had a clear starting point (baseline). This let us compare properly later whether our changes, such as a different model and bigger images, actually led to better results."
- validation: 0.489 (seoul 0.580, busan 0.360, tokyo 0.591, osaka 0.358, taipei 0.557)
- what it means: "That Track B with 0.489 scored almost the same as Track A with 0.496 I found logical and reassuring. We used the same model (ResNet18 at 224 px), although the training settings were not exactly the same. It showed that both baselines performed comparably and that we could start improving from a fair starting point."

## 2026-11-09 less_zoom (Track A)
- changed: `T.RandomResizedCrop(224, scale=(0.7, 1.0))` instead of `scale=(0.35, 1.0)`; otherwise the same as no_flip
- why: "by seeing more of a photo the model can get a hint which city fits it; say it zooms in and so does not catch the text of a billboard, then choosing becomes a lot harder"
- validation: 0.478 (seoul 0.579, busan 0.344, tokyo 0.611, osaka 0.352, taipei 0.505) (before: 0.491, no_flip)
- what it means: "I think the validation score came out lower because with less random zooming the model kept seeing roughly the same images. Because of this the model may have learned too much from the training photos themselves, instead of recognising the general features of a city. So the model worked well on the training data, but less well on new images during validation."

## 2026-11-09 b_mnv3_448 (Track B)
- changed: MobileNetV3-Large instead of ResNet18, photos of 448 px instead of 224; otherwise 4 epochs like b_starter
- why: "bigger photos with better quality are best, I think, because then it can read text"
- validation: 0.562 (seoul 0.621, busan 0.462, tokyo 0.683, osaka 0.436, taipei 0.608) (before: 0.489, b_starter)
- what it means: "The rise from 0.489 to 0.562 shows that our changes had a positive effect on the model's performance. By switching from ResNet18 to MobileNetV3 and enlarging the images from 224 to 448 pixels, the model could probably recognise important details better. I think this is a good improvement, because the score rose by 0.073 (7.3 percentage points). This shows that our changes together were effective. We just cannot say yet which of the two changes had the most influence."

## 2026-11-09 balanced (Track A)
- changed: every city drawn equally often (`sample_weights` gives each photo 1 / the number of photos of its city); otherwise the same as no_flip
- why: "We wanted to even out the cities because there was a big difference in the number of images. Seoul (10,834) and Tokyo (13,055), for example, had many more images than Busan (4,179) and Osaka (6,731). Because of this the model could learn more from the bigger cities and possibly become biased."
- validation: 0.498 (seoul 0.552, busan 0.415, tokyo 0.554, osaka 0.427, taipei 0.540) (before: 0.491, no_flip)
- what it means: "That Busan and Osaka scored better shows that balancing probably helped to recognise smaller cities better. That Seoul and Tokyo actually scored worse is possibly because the model got fewer training examples of these cities. I find this an interesting result, because it shows that a fairer distribution does not automatically mean that all cities are recognised better. We improved the performance for some cities, but gave up performance on other cities for it. But overall, on net, the model scored better because of it."

## 2026-11-09 ema (Track A)
- changed: keep a running average of the weights next to the model (EMA, decay 0.999, roughly the last 1000 steps) and hand in that average; otherwise the same as balanced
- why: "We chose EMA (Exponential Moving Average) because this technique gradually updates the model's weights as an average. Because of this we hoped the model would become more stable and perform better."
- validation: 0.500 (seoul 0.561, busan 0.429, tokyo 0.530, osaka 0.425, taipei 0.553) (before: 0.498, balanced)
- what it means: "That the score only rose from 0.498 to 0.500 shows that EMA had hardly any effect in our experiment. I found this interesting, because it shows that a technique that can help in theory does not always lead to better results. The improvement was so small that we do not know for sure whether it came from EMA or from normal fluctuations."

## 2026-11-09 b_mnv3_448_e6_bal (Track B)
- changed: 6 epochs instead of 4, and every city drawn equally often (`--balance`); otherwise the same as b_mnv3_448. Two changes at once, so it cannot be said which of the two made the difference
- why: "We chose to train the model for 6 rounds instead of 4 and to even out the cities, because we wanted to investigate whether this would improve performance."
- validation: 0.574 (seoul 0.576, busan 0.511, tokyo 0.620, osaka 0.519, taipei 0.645) (before: 0.562, b_mnv3_448)
- what it means: "The total score rose from 0.562 to 0.574. Busan (0.46 → 0.51) and Osaka (0.44 → 0.52) in particular improved clearly. In my view this shows that, thanks to the better distribution, the model gave more attention to cities with fewer images. I found this a positive result, because not only did the total score improve, but the differences between the cities also became smaller. However, we cannot say exactly whether this came from the longer training or from the balancing."

## 2026-11-10 ema_no_smooth (Track A)
- changed: no more label smoothing in `loss_fn` (was 0.1); otherwise the same as ema
- why: "We chose to turn label smoothing off, because we wanted to investigate whether the model would perform better when it learned more directly from the correct labels, without weakening them."
- validation: 0.507 (seoul 0.570, busan 0.429, tokyo 0.526, osaka 0.422, taipei 0.591) (before: 0.500, ema)
- what it means: "The score rose from 0.500 to 0.507, which is a small improvement. In my view this shows that label smoothing was not really necessary in our case and possibly even limited performance a little. Because the difference is small, though, we cannot say with certainty whether turning off label smoothing was actually the cause."

## 2026-11-10 b_mnv3_512_e8_bal (Track B)
- changed: photos of 512 px (the maximum) instead of 448, and 8 epochs instead of 6; otherwise the same as b_mnv3_448_e6_bal. Two changes at once
- why: "We chose to enlarge the images from 448 to 512 pixels and to train the model for 8 rounds instead of 6. With this we wanted to investigate whether the model could recognise the cities better thanks to more detail in the images and longer training."
- validation: 0.586 (seoul 0.595, busan 0.494, tokyo 0.627, osaka 0.515, taipei 0.700) (before: 0.574, b_mnv3_448_e6_bal)
- what it means: "The total score rose from 0.574 to 0.586, which was again an improvement. Taipei in particular stood out with a score of 0.70. In my view this shows that bigger images and longer training together can have a positive effect on performance. We just cannot say exactly which of the two changes helped the most."

## 2026-11-10 lr_1e4 (Track A)
- changed: learning rate 1e-4 instead of 3e-4 (in `make_optimizer` and as `max_lr` in `make_scheduler`); otherwise the same as ema_no_smooth
- why: "We chose to lower the learning rate, because the model then takes smaller steps during training. We hoped the model would learn more accurately this way and eventually reach a better score."
- validation: 0.501 (seoul 0.552, busan 0.427, tokyo 0.533, osaka 0.430, taipei 0.565) (before: 0.507, ema_no_smooth)
- what it means: "The score, however, dropped from 0.507 to 0.501. This shows that a lower learning rate did not lead to better results in our experiment. Possibly the steps were too small, so that the model could learn less well within the available training rounds. That is why we decided to keep the original learning rate."

## 2026-11-10 safe_all_photos (Track A)
- changed: all training photos again (no `selection.csv`), left-right flip back, no EMA; kept every city drawn equally often and no label smoothing. Several changes at once, compared with ema_no_smooth
- why: (to be filled in)
- validation: 0.505 (seoul 0.510, busan 0.442, tokyo 0.518, osaka 0.456, taipei 0.599) (before: 0.507, ema_no_smooth)
- what it means: (to be filled in)

## Plan for what to try next
"If we had more time, for Track A I would first try to distribute the 250,000 photos better over the cities via `selection.csv`. Seoul and Tokyo have more images than, for example, Busan and Osaka. By adjusting the distribution, the model might learn better to recognise all cities. In addition, in `recipe.py` I would test different learning rates, for example a lower learning rate, so that the model takes smaller steps during learning and possibly becomes more accurate. I would also try different photo edits, such as adjusting brightness and contrast, so that the model learns better to deal with different weather conditions and lighting.

For Track B I would train the model longer, for example 10 or 12 rounds instead of 8. We saw that the scores often improved when we trained longer. In addition, I would test the image size, the number of training rounds and the balancing of the cities separately. That way we can find out which change contributed most to the improvements and how we can raise the score further."
