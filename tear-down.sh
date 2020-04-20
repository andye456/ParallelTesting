echo "test logs"
for i in 0 1 2
do
  docker logs robot${i}
  rebot /tmp/TC*/*.xml
done


