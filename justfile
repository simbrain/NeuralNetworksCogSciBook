python := env_var_or_default("PYTHON", "python3")

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
