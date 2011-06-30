

n=$(ls /rap|wc -l)
j=1

# dump the usage of all projects
for i in $(ls /rap)
do 
	echo "$j/$n $i"
	j=$(($j+1))
	./ViewProjectUsage.py $i > $i.txt
done

bash sort-usages.sh

