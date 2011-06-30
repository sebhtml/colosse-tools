n=$(ls /rap|wc -l)
j=1
for i in $(ls /rap)
do 
	echo "$j/$n $i"
	j=$(($j+1))
	./ViewProjectUsage.py $i 12 > $i.txt
done

bash sort-usages.sh

