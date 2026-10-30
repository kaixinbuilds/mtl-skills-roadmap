# mtl-skills-roadmap

BVSS MTL Skills Roadmap: CPDD 2021-syllabus skills for CL, ML and TL, Sec 1 to 4, mapped to SEC 2027 and to the two BVSS school approaches from 2027 (inquiry-based learning and the E21CC priority areas), with the department's planning layer.

Live: https://kaixinbuilds.github.io/mtl-skills-roadmap/

## Pages

- `index.html`: the roadmap. Tabs: Overview, By language, Course map, Unit themes, Syllabus map, Pedagogical design, 21CC roadmap, Inquiry (IBL) roadmap, E21CC priorities, Redesigned SOW.
- `sow-stocktake.html`: stock-take of the department's scheme-of-work documents across the three languages (inventory, formats, completeness, findings).

## Source files and build

No build step for the pages themselves, but the embedded data is generated:

- `tools/enrich.py`: rebuilds the embedded `DATA` in `index.html` (domains, provenance-tagged 21CC / IBL / E21CC tags, design facts, SOW frame). Run `python3 tools/enrich.py` after editing any of the files below.
- `tools/design.json`: pedagogical design facts, hero text, inquiry sketches, theme-thread and course-comparison summaries.
- `tools/sow.json`: the redesigned SOW frame, 2027 calendar and assessment pattern, pacing rules, E21CC moves (with MOE definitions and milestones), HOD decisions, three exemplar units.
- `tools/stocktake.json` and `tools/stocktake_gen.py`: SOW inventory read from the department drive; `tools/build_stocktake.py` embeds it into `sow-stocktake.html`.

See `HANDOFF.md` for what changed on each date, how to change things, the data model and the open gaps.
