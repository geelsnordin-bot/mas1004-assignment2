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
