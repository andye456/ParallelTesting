[[ $# -ne 1 ]] && echo arg1 = number of tests && exit 1
tests=$1

echo "The Images are available:"
docker images
echo "The following Containers still running:"
docker ps -a

