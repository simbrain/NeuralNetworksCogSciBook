python := env_var_or_default("PYTHON", "python3")

# Show the two usual build paths.
default:
    @echo "Container document (for example Book_124): just build Book_124.tex"
    @echo "Master book: just build NeuralNetworksCogsci.tex"

# Compile a document without changing its container setup.
build document:
    latexmk -pdf -interaction=nonstopmode -halt-on-error {{document}}

# Prepare and compile a custom container document with CustomGlossary.tex.
prep document:
    {{python}} scripts/prepare_container_document.py {{document}} --use-custom-glossary
    latexmk -pdf -interaction=nonstopmode -halt-on-error {{document}}

# Update the master document's author line and validate its full glossary.
prep-master document="NeuralNetworksCogsci.tex":
    {{python}} scripts/prepare_container_document.py {{document}}

# Check glossary coverage without changing a container document.
check-glossary document="NeuralNetworksCogsci.tex":
    {{python}} scripts/create_custom_glossary.py --check {{document}}
