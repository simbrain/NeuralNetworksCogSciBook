# Neural Networks for Cognitive Science

Latex files and other scripts that can be used to compile a book about neural networks, especially as they are used in cognitive science. As noted in the preface (which also gives a sense of the contents of the book and the philosophy used when writing it), the book can be customized for different teaching purposes, by producing custom "container documents".

# License

This work is licensed under the Creative Commons Attribution 4.0 Attribution-ShareAlike 
CC BY-SA  License. To view a copy of this license, visit https://creativecommons.org/licenses/by-sa/4.0/. As noted in the description of the license, this allows the content here to be extended and remixed, but assumes that in such a case changes be noted ``but not in any way that suggests the licensor endorses you or your use.''  

# Versions

Calendar based versioning is used in the format `year.version`.  

# How To Use This Book

This folder contains a master document (`NeuralNetworksCogsci.tex`) whose chapter inputs define the full book.

Custom container documents can be created containing specific chapters of interest, as well as other custom docs that are in this repo but not in the master document, including abridgements of long chapters (as in [ActFuncAndLinearAlgebra.tex](ActFuncAndLinearAlgebra.tex)), syntheses and condensations of other chapters (as in [PhilosophicalOverview.tex](PhilosophicalOverview.tex)) and unfinished material. Two sample container docs are [SampleContainerDoc.tex](SampleContainerDoc.tex) and [NewMaterialContainer.tex](NewMaterialContainer.tex).

# Accessibility

PDF accessibility conventions and the current tagged-PDF pilot are documented
in [ACCESSIBILITY.md](ACCESSIBILITY.md).

## Build requirements

The supported LaTeX toolchain is **TeX Live 2026**. Tagged-PDF builds require
TeX Live 2026; build the master with `just build-master`. A small BasicTeX
installation is sufficient, provided that the `latexmk` and `cm-super`
packages are also installed.

You can make your own container document that contain only the chapters of interest to you. When doing so:

- Be sure to copy your container document directly from the master document. Every container document (including the master) starts with `\input{BookMacros}` — this single line enables tagged-PDF output (see [ACCESSIBILITY.md](ACCESSIBILITY.md)), sets `\documentclass[oneside]{book}`, and pulls in the packages, page geometry, and custom commands (`\code`, `\simref`, `\extref`, `\chapterauthor`, `\glossary`, `\figureAttributions`, `\bookReferences`, etc.) shared across all container docs. Anything specific to one container doc only (an extra package, additional `\hypersetup` keys like `pdftitle`/`pdfauthor`) goes in that doc, right after the `\input{BookMacros}` line. Edit `BookMacros.tex` itself, not a per-document copy, when changing something shared, so the change applies everywhere at once.

- It is requested that you include `Preface.tex` which credits those involved in the broader project, information about the nature of the document, and information useful to readers such as an explanation of the *-notation for external citations.*

- To prepare and compile a custom container document, use:
```
just build <container document>.tex
```
  The `.tex` suffix is optional, so `just build Book_124` is equivalent to
  `just build Book_124.tex`.

  This updates author attribution, verifies glossary coverage, generates
  `CustomGlossary.tex`, changes the container document to include it, and
  writes the corresponding PDF.
  The recipes use `python3` by default. If a system uses another Python 3
  command, set `PYTHON` first (for example, `PYTHON=py just build book_103.tex`
  on Windows).

  `just prep <container document>.tex` remains an alias for this command.
  Build the full book with `just build-master`; it retains the canonical
  `Glossary.tex` rather than using `CustomGlossary.tex`.

- If you wish, add a bibliography and figure attribution list at the end of the document (before `\end{document}`) using the shared commands from `BookMacros.tex`:
```latex
	\figureAttributions
	\bookReferences
```
  These add the corresponding table-of-contents entries and print the figure list / bibliography (`NeuralNetworksCogsci.bib`, plain numeric style).

# How To Create New Chapters

- Indicate authorship using `\chapterauthor`.
	<!-- Add parameters indicating author weight -->

- To refer to labels in chapters outside the current chapter, use the custom command `\extref`. Note that to compile a document using this command the master document must also be compiled.

- To make a glossary item use `\glossary` and be sure there is a corresponding entry in `Glossary.tex` (which is the "master" glossary document). If the displayed text differs from the glossary entry, use the optional key form, e.g. `\glossary[activation]{activations}`.

- `Glossary.tex` is the canonical, alphabetized glossary and is manually edited. The release build runs the master glossary check; run `just check-master-glossary` locally to validate that every full-book `\glossary` reference has an entry. To audit the master glossary for entries not referenced in the full book, run `just check-stranded-glossary`. To alphabetize the master glossary after editing it, run:
```
just format-glossary
```

- Use `\cite` command and update `NeuralNetworksCogsci.bib` as usual.

- When using `\caption` in the figure environment, be sure to include a bracketed sentence to be used in the figure attribution list.

- For code and file-name references use `\code{}` (defined in `BookMacros.tex`), e.g. `\code{README.md}`.

- For hyperlinks use `\weburl`

- To reference any Simbrain UI menu, submenu, or menu item (not just the Simulations menu — this also covers menus like Insert, Network, etc.), use `\simref{}` (defined in `BookMacros.tex`) with the exact label, e.g. `\simref{Classical conditioning}`. 
