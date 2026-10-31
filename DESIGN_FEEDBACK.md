# Visual design and communication brief for Claude

Review date: 30 October 2026 (Singapore)
Site: https://kaixinbuilds.github.io/mtl-skills-roadmap/
Repository: kaixinbuilds/mtl-skills-roadmap

## Purpose and scope

The user requested feedback on aesthetics and how to drive the site's points across, then requested this brief be saved in the repository so Claude can read and act on it. This file records recommendations, not changes already implemented.

Read HANDOFF.md before implementation. Preserve its two essential comparisons: across languages for the same course, and within a language across levels of demand. Follow the existing single-file architecture and source-generation workflow: generated content belongs in tools/design.json or tools/enrich.py as appropriate, then regenerate index.html. Do not overwrite unrelated work.

The visual review covered Overview, Course map, 21CC roadmap and E21CC priorities at an approximately 920 px browser width. Findings about clipping apply to that observed width; test other widths rather than assuming. The review did not independently verify syllabus facts, audit every tab, or test every filter.

## Central recommendation

Make the site communicate conclusions before asking visitors to explore evidence. The existing calm, professional foundation is worth keeping. Strengthen hierarchy so findings, teaching implications, navigation instructions and detailed evidence have different visual importance.

Preserve these strengths:
- Serif headings and restrained colours appropriate to a professional education resource.
- Existing Paper 1/2/3 colour coding and stacked exam-weight bars.
- Explicit provenance distinguishing CPDD evidence, derived mappings and departmental inference.
- Language, course and year filters, plus access to full comparison tables.

## Priority 1: clarify the landing message

Replace the generic Overview hero emphasis with a purposeful headline. Suggested copy:

> Plan the four-year MTL learning journey.
> See how curriculum skills build towards SEC 2027, and identify opportunities for inquiry and E21CC.

Use three takeaway cards with a short title, one prominent visual or statistic, and a planning implication:

| Takeaway | Visual emphasis | Planning implication |
| --- | --- | --- |
| Shared exam structure | Three papers across CL, ML and TL | Coordinate common planning |
| Different course priorities | 65% for G1 oral and listening | Match teaching emphasis to course needs |
| Existing opportunities for inquiry | A few supported unit examples | Build from tasks already in the guides |

Validate copy against the current data before publishing. The existing numbered cards mix findings, caveats and navigation instructions; give each takeaway card one clear conclusion.

Acceptance criteria:
- A new visitor can identify the resource's purpose and its main planning messages from the first screen.
- Each featured statistic names its course and assessment component.
- Caveats remain attached to relevant claims; simplification does not remove uncertainty.

## Priority 2: reduce repeated introductions

Course map currently spends much of its first screen on the hero, instructions and controls before showing the progression. Competency pages repeat the title and explanation inside the main panel.

Use this structure: title -> short purpose -> key takeaway -> filters -> visual evidence. Remove duplicate title/intro blocks. Place longer usage instructions and mapping methodology in expandable sections, while retaining essential provenance information beside the visual.

Acceptance criteria:
- The useful visual starts substantially earlier on desktop and tablet.
- No page repeats essentially the same heading and introductory paragraph immediately below its hero.
- Help and methodology remain easy to find and keyboard accessible.

## Priority 3: show progression before unit detail

The Course map's dense cells, wrapped labels and long task descriptions obscure the sequence. At the reviewed width, Sec 4 was partly outside the visible table.

Add a compact Progression summary alongside the full detailed matrix. A possible speaking summary is:

> Sec 1: express views -> Sec 2: give reasons -> Sec 3: support arguments -> Sec 4: respond to perspectives

This is illustrative departmental synthesis, not a verified universal sequence. Derive actual summaries separately for the selected language/course from supporting records, label them as synthesis, and link to evidence. Do not imply that a skill is absent simply because a guide does not name it in a unit.

Keep compact unit cards to the skill, unit reference and evidence status. Reveal full tasks, themes, mapping rules and source notes in a click/tap detail view. Preserve the full table for careful comparison.

Acceptance criteria:
- Users can scan Sec 1-4 without reading every task description.
- Detailed evidence remains available without relying on hover.
- If a detailed table needs horizontal scrolling, its scrollability is obvious; sticky row/column headers should preserve context.
- Mobile offers a usable year/strand detail view rather than squeezing four dense columns onto one screen.

## Priority 4: strengthen visual rhythm

Many components currently share white rounded rectangles, thin borders and similar text sizes. Keep consistency, but distinguish major findings from ordinary supporting text.

Suggested direction:
- Warm off-white background, deep forest-green text and the existing muted paper colours.
- Serif for page titles and major findings; readable sans serif for body, tables and controls.
- Tinted panels reserved for key conclusions and teaching implications.
- Fewer enclosing borders around ordinary explanatory text.
- More space between major sections, less space between closely related controls.
- Small monospaced text reserved for unit references and codes.
- Use purposeful charts, progression lines and task examples rather than decorative stock photographs.

Keep colour meanings consistent. Paper, competency and provenance colours must not become ambiguous. Always pair colour with a text label or another accessible cue. Check text contrast and visible keyboard focus.

## Priority 5: make navigation discoverable

The nine destinations overflowed the visible navigation width; later sections were easy to miss. Existing NAV grouping is useful but needs clearer responsive presentation.

Possible grouping:
- Understand the curriculum: Overview, By language, Syllabus map.
- Plan teaching: Course map, Unit themes, Pedagogical design.
- Develop school priorities: 21CC, Inquiry, E21CC.

Choose a responsive grouped navigation that keeps every destination discoverable and makes the active section clear. Preserve working deep links and filter state behaviour.

Clarify the MTL / EL display control. A possible label is Content language: Original / English, but ensure the copy accurately explains which content changes, since some overview/comparison text remains English in MTL mode.

## Priority 6: make provenance and counts understandable

Heat-table notation such as 0+19 requires readers to remember a decoding rule. Prefer explicit labelled figures or two distinct bars, for example Guide-tagged: 0 and Inferred: 19. Handle derived values explicitly on E21CC rather than mislabelling them as direct CPDD priority tags.

Keep this qualification near the counts:

> Tag counts describe the available documentation and mapping; they do not measure teaching quality or competency attainment.

On E21CC priorities, align source filters with the stated evidence categories: derived and inferred. The current CPDD-tagged only label is potentially confusing because the page says CPDD does not directly tag those school priority areas. Inspect current filter semantics before changing labels or logic. Avoid accidental exclusion or double counting, and make the counting unit explicit.

Descriptors and rule explanations must work by click/tap and keyboard as well as hover.

## Priority 7: connect findings to teaching decisions

Add a small recurring What this means for planning panel, where evidence supports a useful decision. Example:

> Finding: G1 places substantial weight on oral and listening.
> Planning implication: Review the frequency and progression of spoken-interaction practice.
> Next step: Open the relevant course map.

Separate documented findings from departmental recommendations. Link next steps directly to a relevant view, preserving language/course where possible.

## Content consistency to resolve

The Overview says the TL G1 format is still to be confirmed, while its Paper 1 table gives a specific format and minimum length. HANDOFF.md already identifies this gap. Verify against an authoritative source or the TL team; do not guess or silently treat it as confirmed. Until resolved, show a consistent Provisional badge and explanatory note wherever the affected format appears.

## Suggested implementation sequence

1. Shorten introductory panels and remove duplicated headings/copy.
2. Improve responsive navigation and compact the filter presentation.
3. Add evidence-backed progression summaries and concise unit cards.
4. Standardise visual hierarchy, spacing, colour and typography.
5. Improve provenance filters/count labels and add planning implications.

If time is limited, prioritise shorter introductions, a compact progression view, and a teaching implication beside each major finding.

## Verification and handoff

- Follow HANDOFF.md's regeneration process; confirm enrichment remains idempotent when generator inputs change.
- Open every tab in EL and MTL mode; confirm console is clean.
- Check language/course/year/source/competency filters and both comparison modes after layout changes.
- Verify direct hash navigation still works on initial load.
- Inspect representative views at approximately 1440, 920, 768 and 390 px widths. Dense tables may scroll intentionally, but page navigation and primary controls must remain reachable.
- Test keyboard focus, click/tap details, readable contrast and provenance labels that do not depend on colour alone.
- Capture before/after screenshots of Overview, Course map and a competency view.
- Report what changed, what was checked, and any factual questions left unresolved. Do not claim syllabus verification without supporting sources.
