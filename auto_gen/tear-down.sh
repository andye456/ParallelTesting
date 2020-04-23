tests=$1
echo "test logs"
for (( i=0; i<tests; i++ ))
do
  docker logs robot${i}
done
rebot --prerebotmodifier RebotGetElapsedTests.py --prerebotmodifier RebotGetElapsedSuite.py -d output -N "Test Suite" test-cases/TC*/output/*.xml

