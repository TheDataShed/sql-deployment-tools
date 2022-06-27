#! /bin/bash

# Install unixodbc and freetds
brew install unixodbc freetds jq

unixodbc_ver=$((brew info unixodbc --json) | jq -r '.[0].linked_keg')

#Set flags for unixodbc
export LDFLAGS="-L/opt/homebrew/Cellar/unixodbc/$unixodbc_ver/lib"
export CPPFLAGS="-I/opt/homebrew/Cellar/unixodbc/$unixodbc_ver/include"

#Set up venv
python3 -m venv .venv
source ./.venv/bin/activate

# Install the required Python libraries, including `pyinstaller`
pip install --upgrade pip
pip install \
    --quiet \
    --requirement requirements/build.txt

# Keep things clean: destroy the `dist/macosx/` directory if it exists.
rm -rf dist/macosx/

# Create the executable!
PyInstaller ./src/sql-deployment-tools.py \
    --clean \
    --noconfirm \
    --log-level WARN \
    --onefile \
    --console \
    --add-data "./src/sql:sql" \
    --distpath="dist/macosx"

# Run the app to check it has at least built!
./dist/macosx/sql-deployment-tools --help
