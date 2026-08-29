# PDF accessibility

Status: accessibility remediation is in progress. Tagged output remains
experimental in this toolchain; do not describe a release as fully accessible
until it has passed an external PDF check and a screen-reader spot check.

Compile `Book_124.tex` (for example, `just build Book_124.tex`) to create the
pilot PDF. Tagged output remains experimental in this toolchain. The master is
also configured for tagged output and may fail in later legacy chapters until
they are remediated; every release must be checked in a PDF accessibility tool
and with a screen reader. A mixed-remediation PDF may be released when it
builds cleanly, but it must be described as partially remediated rather than
fully accessible.

## Author and reviewer checklist

- Preserve the logical document hierarchy: chapter, section, subsection, and
  list structure must match the content.
- Use `\accessibleimage[options]{path}{description}` for every informative
  raster figure. Make the description convey the instructional point; edit it
  with the figure author. Mark purely decorative graphics as artifacts rather
  than assigning alt text.
- Give every table a header row and a readable order. Keep captions with their
  figures or tables.
- Write equations so their spoken reading is meaningful; flag complex math for
  manual PDF review.
- Use descriptive link text and do not rely on color alone to convey meaning.
- Before release, check title, language, bookmarks, reading order, tags,
  images, tables, equations, and contrast in a PDF accessibility checker; then
  complete a brief screen-reader spot check.

## Current review queue

### Complex matrix displays needing a tagged-math redesign

`LinearAlgebra.tex` still disables automatic paragraph tagging because the
following structures trigger TeX Live 2023 `tagpdf` failures when it is
enabled. Review and convert them one group at a time, then retest the full
master before removing that temporary suppression.

- Gram/vector-comparison matrix (`array` plus raised `bmatrix`, around line
  671).
- Three side-by-side source-target weight-matrix examples: feed-forward,
  recurrent, and sparse recurrent (`minipage` plus header `array` and
  `pmatrix`, around lines 741, 774, and 811).
- Worked right- and left-matrix-vector products, including the hidden-layer
  and recurrent-update calculations (nested `matrix` and `pmatrix`, around
  lines 942, 964, 1001, and 1017).
- Row- and column-processing matrix products (`align*` with `bmatrix`, around
  lines 1076 and 1103).
- The block-matrix representation of a full feed-forward network (nested
  `array` and `matrix`, around line 1448).
- Matrix-heavy exercise answers, especially the recurrent-network products
  near lines 1532 and 1573--1610.

Simple column vectors and ordinary `pmatrix` displays should be manually
checked but are not the first conversion targets.

### Tagged-build warnings to investigate

The current tagged master build has no fatal errors, but still reports:

- about 230 `tagpdf` warnings in which a `Lbl` child is placed directly under
  `Document`; these appear primarily in legacy label/reference structures;
- about 43 nested-link `tagpdf` warnings, chiefly from generated lists and
  linked captions;
- two nested-marked-content pairs, around older inline/float markup;
- normal LaTeX float-placement and line-breaking warnings; and
- a small number of pdfTeX destination/PDF-inclusion warnings.

Treat the first three categories as accessibility work items. The remaining
categories should be reviewed for visible defects, but are not by themselves
proof of an accessibility failure. An external PDF checker and screen-reader
spot check are still required.

## Baseline LaTeX audit

Before broad accessibility rewrites, inventory the source and record results
chapter by chapter. The audit should identify:

- legacy and complex math, especially `eqnarray`, nested `array` environments,
  hand-built matrices, and displays near floats or footnotes;
- raw `\includegraphics` calls, separating informative figures from decorative
  graphics;
- headings, lists, tables, captions, code/listings, footnotes, and references
  that bypass the project's semantic helpers;
- preamble packages, package order, pdfTeX-specific assumptions, and custom
  commands that may conflict with tagged-PDF support; and
- tagged-build failures and warnings, PDF-checker findings, and screen-reader
  spot-check results.

Modernize source patterns rather than accumulating local tagger suppressions:
for example, replace `eqnarray` with appropriate `amsmath` environments and
adopt a dedicated accessible-math convention.

## Temporary measures to retire

- `LinearAlgebra.tex` currently disables automatic paragraph tagging after its
  chapter heading. This avoids a TeX Live 2023 `tagpdf` crash in legacy display
  math, but leaves that chapter without automatic paragraph tags. Remove this
  suppression once the chapter's math structures have been remediated and
  tagged deliberately.
- The `testphase=phase-II` tagged-PDF configuration is experimental. Retest it
  against a current LaTeX toolchain during the audit and replace or update it
  when stable support is available.
- Do not treat the absence of a compilation error as an accessibility result:
  resolve tag-structure warnings and validate the emitted PDF before calling a
  release fully accessible.

This file is intentionally project documentation rather than `AGENTS.md`:
accessibility requirements apply equally to authors, editors, and automated
contributors.
