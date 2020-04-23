[[ $# -ne 1 ]] && echo arg1 = number of tests && exit 1
tests=$i

for (( i=0; i<tests; i++ ))
do
  docker stop robot${i}
  docker rm robot${i}
  docker image rm tc${i}_robot${i}
  docker stop sut${i}
  docker rm sut${i}
  docker image rm tc${i}_sut${i}
done


echo "The following Images Still running:"
docker images
echo "The following Containers still running:"
docker ps -a