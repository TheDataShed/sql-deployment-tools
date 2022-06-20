#! /bin/bash

# Install the required Python libraries, including `pyinstaller`
pip install \
    --quiet \
    --requirement requirements/build.txt

# Keep things clean: destroy the `dist/unix/` directory if it exists.
rm -rf dist/unix/

# Create the executable!
pyinstaller \
    ssis-deployment.py \
    --clean \
    --noconfirm \
    --log-level WARN \
    --onefile \
    --console \
    --add-data "./sql:sql" \
    --distpath="dist/unix"

# Run the app to check it has at least built!
./dist/unix/ssis-deployment --help
