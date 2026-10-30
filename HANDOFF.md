# MTL Skills Roadmap: handoff for Claude Code

Updated October 30, 2026 by HOD/MTL Mdm Chun Kai Xin

Repo: `kaixinbuilds/mtl-skills-roadmap`. Live page: https://kaixinbuilds.github.io/mtl-skills-roadmap/
Single-file app: `index.html` holds CSS, the embedded `const DATA={...}` JSON and the JS views. No build step; open the file in a browser. Layout: sticky site header with grouped navigation (`NAV` in the script), a hero band per tab (`hero()`), each view's sections as panels, and a site footer.

## What the page is for

A department wall chart of what the CPDD 2021-syllabus teacher guides teach in CL, ML and TL, Sec 1 to 4, G1 to HMT, mapped to SEC 2027 and to two BVSS school approaches from 2027: inquiry-based learning (IBL) and the E21CC priority areas (Adaptive Thinking, Inventive Thinking, Civic Literacy, Communication).

Two comparisons must always be easy: across languages for the same course, and within a language across levels of demand.

## What was added on 30 Oct 2026

1. **Pedagogical design tab** (`vDesign`)
   - "Progression at a glance": one card per language (`DATA.design.glance`) with an evidence line (`DATA.design.ev`).
   - "Topic-scope ladder": every unit as a pill with domain dots (self, family, school, community and culture, nation, world and region). Toggle: across languages for one course, or within one language across G1 to HMT. ML dots are the CPDD Domain row of each JATi Panduan Guru (solid). CL and TL dots are inferred from theme wording (dashed).
   - "Pedagogical design side by side": nine aspects × three languages (`tools/design.json`), the last row covering how levels of demand differ within each language.
2. **Provenance on every 21CC, IBL and priority-area tag.** Each record now has `tags: [{k, src, rule}]` with `src` = `cpdd` (tagged by CPDD), `derived` (mapped from a CPDD tag by a fixed table) or `infer` (assigned by a content rule). The 21CC, IBL and E21CC tabs have a Source filter (CPDD + inferred, CPDD only, inferred only). Blue = written into the CPDD guide, teal = derived from a CPDD tag, amber = mapped by the department through reasoning (all solid colours) (cards, tags and colour key); dashed tags carry a small `derived` or `inferred` label and a hover showing the rule. Heat cells read `CPDD+inferred` (for example `1+3`).
3. **E21CC priorities tab**: the four BVSS priority areas as a lens (`PA_AT`, `PA_IT`, `PA_CL`, `PA_CM` in `DATA.cat`, with descriptors from the school slide in `desc`). No CPDD guide tags these, so every tag is derived or inferred. An expandable "How the inferred tags are assigned" lists the rules in force.
4. **By language tab**: five new comparison rows (signature routines, how writing is taught, when the exam writing form becomes regular, oral and read-aloud preparation, topic scope) in `DATA.diff` / `DATA.diffEn`.
5. **Deep links now work on load** (`#tab-LANG-COURSE`, for example `#design-ML-G1`). Before this, the hash was only read on change.
6. `tools/enrich.py` and `tools/design.json`: the reproducible build for everything above.

## Design pass from DESIGN_FEEDBACK.md (30 Oct 2026)

- **Overview hero**: headline "Plan the four-year MTL learning journey" and three takeaway cards (shared exam structure; G1 Paper 3 weight; CPDD-tagged inquiry units), each with a planning implication and a link.
- **Every tab**: hero is title + one-line purpose; the old numbered points and "how to use" are folded into a keyboard-accessible "How to read this page". Repeated headings inside the 21CC, IBL, E21CC, Unit themes and Syllabus map panels are gone.
- **"What this means for planning" panel** on Course map, Pedagogical design, 21CC, IBL and E21CC: "From the data" (computed) kept apart from "Department suggestion".
- **Navigation**: three labelled groups (Understand the curriculum / Plan teaching / Develop school priorities), wrapping so all nine tabs stay visible; a grouped dropdown below 640 px. The display toggle is now "Content language: Original / English".
- **Course map**: a compact Summary (skill focus + unit ref + Examined badge per entry, click for full detail) is the default; Full detail keeps the old matrix. Exam papers fold into one summary line. Below 640 px the summary stacks by year.
- **Counts and provenance**: heat cells show the total plus separate guide-tagged (or derived, on E21CC) and inferred counts, with the qualification that counts describe documentation, not teaching quality. E21CC source filter reads Derived + inferred / Derived only / Inferred only (same logic as before). Tag and priority-area descriptors are listed on the page, not only on hover.
- **TL G1 Paper 1** carries a Provisional badge and note wherever it appears (Overview, By language, Course map) until next step 1 is resolved.
- Wide tables keep their first column sticky and show a "Scroll sideways" cue only when they overflow. Palette warmed slightly (off-white background, forest-green ink); paper, language and provenance colours unchanged.

## How to change things

- **Edit a design fact**: change `tools/design.json`, then `python3 tools/enrich.py`. The script rewrites the embedded DATA in place and is idempotent.
- **Edit page text** (also in `tools/design.json`, then rerun `enrich.py`): `about` is the hero text at the top of each tab (lead, the points and how-to-use folded under "How to read this page"; `over` also has `headline` and `takeaways`); `plan` is the "What this means for planning" panel per tab (`f` finding, `i` suggestion, `go`/`gl` link); `provisional` lists exam facts to badge as Provisional (`lang`, `course`, `paper`, `note`). Text in `takeaways` and `plan` may use `{tokens}` (for example `{g1p3}`, `{iblCpdd}`, `{w3}`) that the page fills from DATA, so figures cannot drift from the data (see `stats()` in `index.html`); `iblsg` is the "IBL in the Singapore context" essence section at the top of the IBL tab (from STP Knowledge Base chapter 14: key elements, inquiry cycle, 5E model, approaches, enablers, glossary); `iblx` holds one inquiry sketch per IBL-tagged unit (keyed `LANG|COURSE|SEC|BOOK|UNIT`: inquiry question, approach, four phases); these are department sketches, so review them with the units and add one when a unit gains an IBL tag; `stp` is the STP Learning Orientations card on the IBL tab (PDF and KB links, how the MTL guides line up); `cellsEn` / `evEn` are the plain-English design text shown in EL mode.
- **Edit or add an inference rule**: edit `RULES` in `tools/enrich.py` (id, test, 21CC cats, priority areas, one-line reason), rerun. Every unit is re-tagged; the rule list on the page updates itself.
- **Change the CPDD-to-priority mapping**: `DERIVE` in `tools/enrich.py` (currently CAIT → AT + IT, CCIS → CM, CGC → CL, SEC → AT).
- **Change ML domains**: the `ml(...)` lines in `tools/enrich.py` transcribe each guide's Gambaran Keseluruhan Domain row. CL and TL domain keywords are in `KW`.
- **Verify in a browser before pushing**: `node` + Playwright script, or just open the file. Check the console is clean, then click every tab once in EL and MTL mode.

## Data model (per record in `DATA.recs`)

`lang, course, sec, book, unit, theme_m, theme_en, strand, also, sub_m, sub_en, purpose, task_m, task_en, exam, syl, c21, ibl, cats` (unchanged) plus `tags` (new). `DATA.themes[*]` gains `dom` (list of domain keys) and `domSrc`. New top-level keys: `domains, prov, rules, priNote, design`.

## Known gaps and next steps (in priority order)

1. **Confirm the TL G1 written-paper format.** The Overview tab's exam data says "social-media post responding to a situation, at least 50 words, typed"; the pedagogy doc in the Claude project says "not confirmed". Check SEAB 1204 / K122 with a TL colleague and make the two agree.
2. **Add CL 综合任务 (integrated tasks) as records.** They are inquiry-shaped (news search, surveys, product design, dream boards) but not in the dataset, so CL looks thin on the IBL tab. Source: each 教师手册's 各单元教学建议. Suggested fields: strand `oral`, sub "综合任务 Integrated task", `ibl` note, and let R7 tag them.
3. **Review the inferred tags with the three units.** Rules are deliberately broad (R3 civic fires on many themes; R6 adaptive fires on "change" and "dream"). Tighten by adding negative conditions or by replacing a rule hit with a `cpdd`-style manual tag for units teachers confirm. Consider a `confirmed` provenance value for department-vetted tags.
4. **Get the missing guides**: ML Sec 4 Units 4 to 6 Panduan Guru (all courses; only the one-page overviews are on the drive) and the TL 4G1 Unit 6 lesson prep. The TL lesson-prep PDFs use legacy fonts; OCR or the Word versions are needed to read lesson steps.
5. **Design-matrix text for G2, G3 and HMT.** Cells describe G1 packages; the "levels of demand" row is the only within-language content so far. Add per-course cells once the G2/G3/HMT guides are read (CL ones are on the drive).
6. **Translations.** New comparison and design text is English-only in MTL mode (the page's existing convention for overview text). Add `zh`, `ms`, `ta` keys to `design.json` if teachers want them.
7. **Export.** A "download CSV of the current filter" button on the roadmap tabs would let the SOW work happen in Excel; the data is already flat.
8. **Hash should carry filters** (`sL, sC, sS, src, cats`) so a filtered view can be shared as a link.

## Sources read for the 30 Oct update

- Dept drive, `CPDD resources (2021 Syllabus)`: `CL/G1/G1华文教师手册（一上 to 中四）.pdf`; `ML/Teachers Guidebook/{G1,G2,G3,HML}/*.pdf` (Domain rows from every guide; G1 guides read in full); `ML/Teachers Guidebook/Overview/M4_Gambaran Keseluruhan Unit 4-6.pdf`; `TL Teachers Guide/1G1 to 4G1 TG/*கண்ணோட்டம் (Word).docx`.
- Claude project doc: "20261030_G1 CL Pedagogy and S1 to S4 Skill Progression (with ML/TL cross-reference)".
- BVSS E21CC priority areas slide (Adaptive Thinking, Inventive Thinking, Civic Literacy, Communication).
