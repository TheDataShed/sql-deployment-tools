# Pull in requirements and install dependencies
python3 -m pip install -r ./requirements/test.txt --upgrade

#remove previous test results
rm -rf ./test-results/

# Discover unit tests
python3 -m pytest