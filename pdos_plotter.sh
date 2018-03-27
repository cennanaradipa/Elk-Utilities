#!/bin/bash

# script to convert all pdos files to atom-based pdos
# must use gnuplot script to plot
# current script is only for non-polarized calculation
# bug: adding total DOS would cancel spin down and spin up moments
# resolved by creating a whole new routine elk-pdos.py

printf "=%.0s" {1..50}
echo -e "\nConvert PDOS.OUT to PDOS Total (atoms) "
printf "=%.0s" {1..50}

# input how many atoms are available
echo -e "\nHow many species of atoms are in this PDOS?\n"
read -p "Input here and press enter: " SPECIES

printf "\n%s species entered. Finding number of files..\n"  $SPECIES

printf "\nInput working directory (PDOS file locations:\n"
read -p "Input here and press enter: " WORKDIR

printf "\nMoving to working directory..\n"
cd $WORKDIR

printf  "\nRemoving old .total files from current folders..\n"
rm -f -v *.total

for i in `seq $SPECIES`;
do
        FILE=`printf "S%02d" $i`
        NFILE=`ls ./PDOS_*.OUT | grep "$FILE" | wc -l | xargs`
        printf "\nFound %s files for species #%d\nConverting files..\n" $NFILE $i
        for j in `seq $NFILE` ;
        do
                CONVERT=`ls PDOS_*.OUT | grep "$FILE" | sed "${j}q;d"` 
                echo $CONVERT $j
                python ~/Desktop/elk_newdata/pdos.py $CONVERT
        done
        printf "\nFile conversion done. Collecting into 1 species file..\n"
        paste "PDOS_${FILE}"*.total > temp.txt
        printf  "\nRemoving unnecessary columns\n"
        awk '{ for (i=3;i<=NF;i+=2) $i="" } 1' temp.txt > temp2.txt
        awk '{ for(i=2; i<=NF;i++) j+=$i; print $1, j; j=0 }' temp2.txt > PDOS_${FILE}.all
        printf "\nSpecies #%d done. Written to %s \n" $i PDOS_${FILE}.all
done

rm -f -v temp*.txt
