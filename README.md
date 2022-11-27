# Neural Networks for Cognitive Science

Latex files and other scripts that can be used to compile a book about neural networks, especially as they are used in cognitive science. As noted in the preface (which also gives a sense of the contents of the book and the philosophy used when writing it), the book can be customized for different teaching purposes, by producing custom "container documents".

# Versions

Calendar based versioning is used in the format `year.major.minor`.  New public releases are created tagged at `major` version updated but not at `minor` version updates (though the PDF should be updated with every release).

# How To Use This Book

This folder contains a master document (`Book_master.tex`) that compiles every chapter. The master document is a container document with all of the chapters.

You can make your own container document that contain only the chapters of interest to you. When doing so:

- Be sure to copy your container document directly from the master document. The custom commands at the top of the master document are required in all container documents.

- It is requested that you include `Preface.tex` which credits those involved in the broader project, information about the nature of the document, and information useful to readers such as an explanation of the *-notation for external citations.*

- Set author attribution for your container document using: `python create_authorship_order.py <container document>.tex`. The author order will automatically be set in the container document. (Assumes Python 2)

- If you wish, compile a custom glossary for the container document using: `python create_custom_glossary <container document>.tex`. Then include `CustomGlossary.tex` in your container document.

- If you wish, add a bibliography using:
```latex
	\bibliography{NeuralNetworksCogsci}{}
	\bibliographystyle{plain}
```

- Be sure to include `\listoffigures` which prints a figure attribution list.

# How To Create New Chapters

- Indicate authorship using `\chapterauthor`.
	<!-- Add parameters indicating author weight -->

- To refer to labels in chapters outside the current chapter, use the custom command `\extref`. Note that to compile a document using this command the master document must also be compiled.

- To make a glossary item use `\glossary` and be sure there is a corresponding entry in `Glossary.txt` (which is the "master" glossary document).

- Use `\cite` command and update `NeuralNetworksCogsci.bib` as usual.

- When using `\caption` in the figure environment, be sure to include a bracketed sentence to be used in the figure attribution list.

- For code references use `\texttt`