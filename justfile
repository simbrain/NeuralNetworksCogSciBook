python := env_var_or_default("PYTHON", "python3")

# Show the two usual build paths.
default:
    @echo "Container document (for example Book_124): just build Book_124.tex"
    @echo "Master book: just build NeuralNetworksCogsci.tex"

# Compile a document without changing its container setup.
# $max_repeat is raised because a from-scratch build of the full book needs
# more than latexmk's default 5 passes to stabilize (table of contents, figure
# attributions, bibliography, xr cross-references, and PDF tagging).
build document:
    latexmk -pdf -interaction=nonstopmode -halt-on-error -e '$max_repeat=9' {{document}}

# Prepare and compile a custom container document with CustomGlossary.tex.
prep document:
    {{python}} scripts/prepare_container_document.py {{document}} --use-custom-glossary
    latexmk -pdf -interaction=nonstopmode -halt-on-error -e '$max_repeat=9' {{document}}

# Update the master document's author line and validate its full glossary.
prep-master document="NeuralNetworksCogsci.tex":
    {{python}} scripts/prepare_container_document.py {{document}}

# Check glossary coverage without changing a container document.
check-glossary document="NeuralNetworksCogsci.tex":
    {{python}} scripts/create_custom_glossary.py --check {{document}}
