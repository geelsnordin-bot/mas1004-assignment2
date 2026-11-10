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
- changed: niets, het startrecept, getraind met seed 0 en seed 1
- why: beginpunt, en zien hoeveel de score door toeval beweegt
- validation: seed 0 0.496 (seoul 0.568, busan 0.383, tokyo 0.637, osaka 0.343, taipei 0.547); seed 1 0.495 (seoul 0.580, busan 0.399, tokyo 0.608, osaka 0.371, taipei 0.517)
- what it means: (nog in te vullen door Nordin)

## 2026-11-06 manual_drop (Track A)
- changed: 3019 trainingsfoto's weggelaten uit mijn eigen controlelijst (track_a/manual_list.csv, redenen in track_a/dropped.csv): eten, dieren, museumstukken, persmomenten en uniformen, vliegtuigen, autoshow, zwart-wit, 360-graden, lange reeksen van een fotograaf, en drie Busan-video's met overlays
- why: troep eruit die niks kenmerkbaars had voor de stad
- validation: 0.492 (seoul 0.585, busan 0.376, tokyo 0.639, osaka 0.367, taipei 0.495) (before: 0.496 / 0.495)
- what it means: "ik had verwacht een betere score aangezien troep eruit gaat wat niks kenmerkbaars had voor de stad en het model verder zelfde blijft dus de score percentueel wel omhoog zou gaan dit is dus wel een kleine shock"

## 2026-11-07 no_flip (Track A)
- changed: `T.RandomHorizontalFlip()` weggehaald uit train_transform; selectie dezelfde als manual_drop
- why: "Het recept spiegelt elke foto willekeurig horizontaal. Daardoor komt tekst in spiegelbeeld te staan en lijken auto's aan de verkeerde kant van de weg te rijden. Juist die rijrichting kan helpen om steden te onderscheiden: in Japan rijdt men links, in Korea en Taiwan rechts. Mijn verwachting was daarom dat het model deze aanwijzing beter zou oppikken als ik het spiegelen uitzette."
- validation: 0.491 (seoul 0.597, busan 0.360, tokyo 0.627, osaka 0.344, taipei 0.528) (before: 0.492, manual_drop)
- what it means: "Dat bleek niet zo te zijn: de score bleef gelijk. Het model leunt blijkbaar weinig op zulke kleine details en herkent een stad vooral aan het algemene beeld, zoals gebouwen, kleuren en straatbeeld."

## 2026-11-07 b_starter (Track B)
- changed: niets, src/train_b.py met de standaardinstellingen (ResNet18, 224 px, 4 epochs, alle trainingsfoto's)
- why: (nog in te vullen door Nordin)
- validation: 0.489 (seoul 0.580, busan 0.360, tokyo 0.591, osaka 0.358, taipei 0.557)
- what it means: (nog in te vullen door Nordin)

## 2026-11-09 less_zoom (Track A)
- changed: `T.RandomResizedCrop(224, scale=(0.7, 1.0))` in plaats van `scale=(0.35, 1.0)`; verder gelijk aan no_flip
- why: "door meer te zien van een foto kan het model een hint krijgen welke stad er bij past stel hij zoomt in en pakt daardoor niet de tekst van een billboard dan wordt kiezen een stuk lastiger"
- validation: 0.478 (seoul 0.579, busan 0.344, tokyo 0.611, osaka 0.352, taipei 0.505) (before: 0.491, no_flip)
- what it means: "Ik denk dat de validatiescore lager is uitgevallen doordat het model bij minder willekeurig inzoomen steeds ongeveer dezelfde afbeeldingen te zien kreeg. Hierdoor heeft het model mogelijk te veel geleerd van de trainingsfoto's zelf, in plaats van de algemene kenmerken van een stad te herkennen. Daardoor werkte het model goed op de trainingsdata, maar minder goed op nieuwe afbeeldingen tijdens de validatie."

## 2026-11-09 b_mnv3_448 (Track B)
- changed: MobileNetV3-Large in plaats van ResNet18, foto's van 448 px in plaats van 224; verder 4 epochs zoals b_starter
- why: "grotere fotos met betere kwaliteit is denk ik het beste want dan kan het teksten lezen"
- validation: 0.562 (seoul 0.621, busan 0.462, tokyo 0.683, osaka 0.436, taipei 0.608) (before: 0.489, b_starter)
- what it means: (nog in te vullen door Nordin)

## 2026-11-09 balanced (Track A)
- changed: elke stad even vaak getrokken (`sample_weights` geeft elke foto 1 / aantal foto's van zijn stad); verder gelijk aan no_flip
- why: (nog in te vullen door Nordin)
- validation: 0.498 (seoul 0.552, busan 0.415, tokyo 0.554, osaka 0.427, taipei 0.540) (before: 0.491, no_flip)
- what it means: (nog in te vullen door Nordin)

## 2026-11-09 ema (Track A)
- changed: naast het model een lopend gemiddelde van de gewichten bijhouden (EMA, decay 0.999, ongeveer de laatste 1000 stappen) en dat gemiddelde inleveren; verder gelijk aan balanced
- why: (nog in te vullen door Nordin)
- validation: 0.500 (seoul 0.561, busan 0.429, tokyo 0.530, osaka 0.425, taipei 0.553) (before: 0.498, balanced)
- what it means: (nog in te vullen door Nordin)

## 2026-11-09 b_mnv3_448_e6_bal (Track B)
- changed: 6 epochs in plaats van 4, en elke stad even vaak getrokken (`--balance`); verder gelijk aan b_mnv3_448. Twee veranderingen tegelijk, dus niet te zeggen welke van de twee het verschil maakte
- why: (nog in te vullen door Nordin)
- validation: 0.574 (seoul 0.576, busan 0.511, tokyo 0.620, osaka 0.519, taipei 0.645) (before: 0.562, b_mnv3_448)
- what it means: (nog in te vullen door Nordin)

## 2026-11-10 ema_no_smooth (Track A)
- changed: geen label smoothing meer in `loss_fn` (was 0.1); verder gelijk aan ema
- why: (nog in te vullen door Nordin)
- validation: 0.507 (seoul 0.570, busan 0.429, tokyo 0.526, osaka 0.422, taipei 0.591) (before: 0.500, ema)
- what it means: (nog in te vullen door Nordin)

## 2026-11-10 b_mnv3_512_e8_bal (Track B)
- changed: foto's van 512 px (het maximum) in plaats van 448, en 8 epochs in plaats van 6; verder gelijk aan b_mnv3_448_e6_bal. Twee veranderingen tegelijk
- why: (nog in te vullen door Nordin)
- validation: 0.586 (seoul 0.595, busan 0.494, tokyo 0.627, osaka 0.515, taipei 0.700) (before: 0.574, b_mnv3_448_e6_bal)
- what it means: (nog in te vullen door Nordin)
