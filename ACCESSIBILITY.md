# PDF accessibility requirements

This is a short working note. Move its enduring authoring and release guidance
into the README when the accessibility work is complete, then remove this
file.

## Tagged-PDF setup

Book/container documents must enable tagged output before `\documentclass`:

```tex
\DocumentMetadata{
  lang=en-US,
  testphase=phase-II
}
```

Use a current TeX Live release and build the master with `just build-master`.
That recipe includes the extra pdfTeX memory needed by the tagged master.

## Authoring requirements

- Preserve the logical heading and list hierarchy.
- Use `\accessibleimage[options]{path}{description}` for informative images.
  Describe the instructional point, not merely the file or its appearance.
- Use `\accessibleartifact[options]{path}` for decorative images whose content
  is already conveyed by nearby text.
- Do not add raw `\includegraphics` to remediated book content. The helpers
  pass `alt=` and `artifact` directly to `graphicx`, which creates the correct
  tagged-PDF image structure.
- Give tables clear headers, a readable order, and captions associated with
  the table. Keep figure captions associated with their figures.
- Write descriptive link text and do not rely on color alone to convey meaning.
- Write equations so their spoken reading is meaningful; manually inspect
  complex displays and matrices.

## Release checks

Before describing a PDF as accessible:

1. Run Acrobat Pro's **Accessibility Check**.
2. In Acrobat's **Tags** pane, inspect representative headings, paragraphs,
   lists, tables, equations, links, and figures. Figure Properties should show
   meaningful alternate text, not an asset path. Decorative graphics should
   not appear as meaningful figures.
3. Confirm document title and language in **File → Properties → Description**.
4. Use Read Out Loud or a screen reader to sample reading order across a
   chapter, including a figure, table, and equation.
5. Record findings with the PDF page, tag type, and source location.

## Ongoing review

Treat tag-structure warnings as review items rather than automatic proof of a
defect. Generated lists/links and matrix-heavy content warrant particular
attention. `LinearAlgebra.tex` has a temporary paragraph-tagging suppression
around legacy matrix material; do not remove it without retesting the full
master and checking the resulting PDF.
