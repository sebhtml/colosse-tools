for j in $(ls /rap)
do
	i=$j.txt
	echo "$(grep "YEAR_ENTRY	2011" $i|awk '{print $3" "$9}') $i"
done|sort -n -r|awk '{print $3"\t"$1"\t"$2}'|sed 's/.txt//g' 

