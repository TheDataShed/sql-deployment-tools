sudo apt-get install libxml2-utils

if test -f "./test-results/unit-test-results.xml"; then
    tests=$(xmllint --xpath 'string(/testsuites/testsuite[@name="pytest"]/@tests)' ./test-results/unit-test-results.xml)
    skipped=$(xmllint --xpath 'string(/testsuites/testsuite[@name="pytest"]/@skipped)' ./test-results/unit-test-results.xml)

    if [ "$tests" = 0 ]
    then
            echo "No tests in test output found!!!"
            exit 1
    fi

    if [ "$skipped" = $tests ]
    then
        echo "No tests ran!!!"
        exit 1
    fi
else
echo "No test results file found!!!"
exit 1
fi