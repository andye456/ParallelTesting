tests=3
echo "test logs"
for (( i=0; i<tests; i++ ))
do
  docker logs robot${i}
done
rebot -d output -N "Test Suite" test-cases/TC*/output/*.xml

