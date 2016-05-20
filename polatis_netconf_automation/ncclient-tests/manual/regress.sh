set -x
#!/bin/bash


rm -rf finalLog.csv
rm -rf demo.log

doit ()

{
    python $1.py

}


if [ $# -eq 0 ]; then
    echo "No suites"
else
    testlist=$*
fi

for test in $testlist
do
doit $test
done
