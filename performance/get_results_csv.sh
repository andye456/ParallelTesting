# This will get the total time for the test and split it into CSV to analysis

A=$(for i in `ls ../performance_results/*.html`
do 
	#echo -n "$i,"|awk -F "/" '{print $3}'
	echo -n "$i,"
	grep "\"elapsed\"" $i | tr "," "\n"| grep "\[{\"elapsed\"" | grep -v "\[\[" | awk -F ":" '{print $4}' | tr "\"" " "
done)
echo "$A" | sort -n
