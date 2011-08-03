for j in $(ls /rap)
do
	i=$j.txt
	consumed=$(grep "YEAR_ENTRY	2011" $i|awk '{print $3" "$9}')
	allowed=$(grep Target $i|tail -n1|awk '{print $2}')
	project=$j
	echo "$consumed $allowed $j"
done|sort -n -r #|awk '{print $3"\t"$1"\t"$2}'

