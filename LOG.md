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
