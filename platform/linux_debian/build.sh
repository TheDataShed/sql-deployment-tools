#! /bin/bash

# Install the required Python libraries, including `pyinstaller`
pip install --upgrade pip
pip install \
    --quiet \
    --requirement requirements/build.txt

# Keep things clean: destroy the `dist/debian/` directory if it exists.
rm -rf dist/debian/

# Create the executable!
pyinstaller \
    ./src/sql-deployment-tools.py \
    --clean \
    --noconfirm \
    --log-level WARN \
    --onefile \
    --console \
    --add-data "./src/sql:sql" \
    --distpath="dist/debian"

# Run the app to check it has at least built!
./dist/debian/sql-deployment-tools --help
