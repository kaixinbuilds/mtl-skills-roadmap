# mtl-skills-roadmap

BVSS MTL Skills Roadmap: CPDD 2021-syllabus skills for CL, ML and TL, Sec 1 to 4, mapped to SEC 2027 and to the two BVSS school approaches from 2027 (inquiry-based learning and the E21CC priority areas), with the department's planning layer.

Live: https://kaixinbuilds.github.io/mtl-skills-roadmap/

## Pages

- `index.html`: the roadmap. Tabs: Overview, By language, Course map, Unit themes, Syllabus map, Pedagogical design, 21CC roadmap, Inquiry (IBL) roadmap, E21CC priorities, Scheme of work 2027, Writing task bank (every CPDD writing task by type and year, with when each type first appears). Scheme of work 2027 is one term-by-term grid per language, course and year, with the school's VMV and E21CC focus mapped to the MTL curriculum).

## Source files and build

No build step for the pages themselves, but the embedded data is generated:

- `tools/enrich.py`: rebuilds the embedded `DATA` in `index.html` (domains, provenance-tagged 21CC / IBL / E21CC tags, design facts, SOW frame). Run `python3 tools/enrich.py` after editing any of the files below.
- `tools/design.json`: pedagogical design facts, hero text, inquiry sketches, theme-thread and course-comparison summaries.
- `tools/sow.json`: the SOW grid data: 2027 school calendar and MT events, assessment pattern and 2026 component formats, oral coaching framework, pacing rules, E21CC moves (with MOE definitions and milestones), VMV and desired-student-outcome mapping, CPDD listening and speaking tasks per unit, the full CL textbook writing prompts, and the SEAB 2027 syllabus links with assessment objectives.

See `HANDOFF.md` for what changed on each date, how to change things, the data model and the open gaps.
