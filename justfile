python := env_var_or_default("PYTHON", "python3")

# Show the two usual build paths.
default:
    @echo
    @echo "Master book:"
    @echo "  just build-master"
    @echo
    @echo "Container document (for example Book_124):"
    @echo "  just build Book_124"
    @echo "  (.tex is optional)"
    @echo

# Prepare and compile a container document using the existing authorship and
# custom-glossary scripts, so its PDF has current metadata and glossary.
build document:
    {{python}} scripts/prepare_container_document.py {{document}} --use-custom-glossary
    latexmk -pdf -interaction=nonstopmode -halt-on-error -e '$max_repeat=9' {{document}}

# Backwards-compatible name for the container build recipe.
prep document:
    {{python}} scripts/prepare_container_document.py {{document}} --use-custom-glossary
    latexmk -pdf -interaction=nonstopmode -halt-on-error -e '$max_repeat=9' {{document}}

# Prepare and compile the master without replacing its canonical glossary.
build-master document="NeuralNetworksCogsci.tex":
    {{python}} scripts/prepare_container_document.py {{document}}
    latexmk -pdf -interaction=nonstopmode -halt-on-error -e '$max_repeat=9' {{document}}

# Update the master document's author line and validate its full glossary.
prep-master document="NeuralNetworksCogsci.tex":
    {{python}} scripts/prepare_container_document.py {{document}}

# Check glossary coverage without changing a container document.
check-glossary document="NeuralNetworksCogsci.tex":
    {{python}} scripts/create_custom_glossary.py --check {{document}}

# Validate the canonical glossary and its references in the full book.
check-master-glossary:
    {{python}} scripts/check_master_glossary.py

# Audit for master glossary entries that are not referenced in the full book.
check-stranded-glossary:
    {{python}} scripts/create_custom_glossary.py --check --check-stranded NeuralNetworksCogsci.tex

# Alphabetize the canonical master glossary after editing it.
format-glossary:
    {{python}} scripts/create_custom_glossary.py --format
