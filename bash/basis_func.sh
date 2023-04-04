### This script creates and sbatches a gaussian calculation for each atom with a chosen basis set to determine the number of basis functions with that basis set.
### Requires atoms.txt file


echo "What basis do you want to run?"
read basis
numatoms=`wc -l atoms.txt | awk '{print $1}'`
a=1
b=2
for i in $(eval echo "{1..$numatoms}")
	do
		elecnum=`head -n $i atoms.txt | tail -n1 | awk '{print $2}'`
		atom=`head -n $i atoms.txt | tail -n1 | awk '{print $1}'`
		echo "%nproc=4" >> ${elecnum}.com
		echo "%mem=11000MB" >> ${elecnum}.com
		echo "#P HF/${basis}" >> ${elecnum}.com
		echo "" >> ${elecnum}.com
		echo "This job runs ${atom} with a ${basis} basis function" >> ${elecnum}.com
		echo "" >> ${elecnum}.com
		if [ `expr $elecnum % 2` == 0 ];
			then
				echo "0 1" >> ${elecnum}.com
			else
				echo "0 2" >> ${elecnum}.com
		fi
		echo "$atom  0.0000  0.0000  0.0000" >> ${elecnum}.com
		echo '' >> ${elecnum}.com
done

for i in {1..118}
	do
		cp gaussian.sh gaussian_${i}.sh
		sed -i "s/job/${i}/g" gaussian_${i}.sh
		sbatch gaussian_${i}.sh
done
