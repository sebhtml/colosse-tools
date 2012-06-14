#!/bin/bash
#PBS -N convert-2012-06-11.4
#PBS -A nne-790-ab
#PBS -l walltime=16:00:00
#PBS -l nodes=1:ppn=8
#PBS -q default
#PBS -o convert-2012-06-11.4.stdout
#PBS -e convert-2012-06-11.4.stderr
cd $PBS_O_WORKDIR


outputDirectory=convert-2012-06-11.4

source /rap/nne-790-ab/software/CASAVA_v1.8.2/module-load.sh

configureBclToFastq.pl \
--input-dir Data/Intensities/BaseCalls \
--output-dir $outputDirectory \
--use-bases-mask Y*,I*,Y* \
--sample-sheet CASAVA-Sheet.csv \
--mismatches 1

# 2 does not work.

cd $outputDirectory

make -j 8
