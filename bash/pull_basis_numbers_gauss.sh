#### This script pulls the atom identities and basis functions for that atom under a specific basis set. This is ran after the basis_func.sh script

rm -f basis.xls
rm -f primitive.xls
rm -f cartesian.xls
rm -f comb*

for i in {1..118}
	do
		grep -B 4 'Charge =' ${i}.log | grep "This job runs" | awk '{ print $4 }' > atom
		grep -B 4 'Charge =' ${i}.log | grep "This job runs" | awk '{ print $7 }' > basis
		grep "basis functions," ${i}.log | awk '{ print $1 }' > function
		grep "basis functions," ${i}.log | awk '{ print $4 }' > function2
		grep "basis functions," ${i}.log | awk '{ print $7 }' > function3
#		grep "basis functions," ${i}.log | awk '{ print $2 }' > id
#		grep "basis functions," ${i}.log | awk '{ print $5 }' > id2
#		grep "basis functions," ${i}.log | awk '{ print $8 }' > id3
		paste atom function function2 function3 >> comb
		rm atom
	        rm function*
		 

done

awk '{gsub(" ",",",$0);print $0}' comb | sed "s/,$//g" > comb1

grep "basis functions," 1.log | awk '{ print $2 }' > id
grep "basis functions," 1.log | awk '{ print $5 }' > id2
grep "basis functions," 1.log | awk '{ print $8 }' > id3

paste basis id id2 id3 > functions.xls
cat comb1 >> functions.xls

#rm id*
rm basis
rm comb*
