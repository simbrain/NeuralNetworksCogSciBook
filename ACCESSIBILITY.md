# PDF accessibility

Status: an accessibility pilot is underway for the Preface and Introduction. As Fall 2026 unfolds more will be updated.

Compile `Book_124.tex` (for example, `just build Book_124.tex`) to create the
pilot PDF. Tagged output remains experimental in this toolchain. The master is
also configured for tagged output and may fail in later legacy chapters until
they are remediated; every release must be checked in a PDF accessibility tool
and with a screen reader.

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

## Scope and next steps

The Preface has one informative license logo. The Introduction has eleven
informative raster images; initial descriptions are in `Preface.tex` and
`Intro.tex` for editorial review. Apply the same convention chapter by chapter,
prioritizing diagrams, tables, and mathematical material.

This file is intentionally project documentation rather than `AGENTS.md`:
accessibility requirements apply equally to authors, editors, and automated
contributors.
