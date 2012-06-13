#!/bin/bash
#A very simple bash script to copy and rename the pictures in the desired order
oldifs=$IFS
IFS='
'
n=0
exec 6<full_list.txt

while read -u 6 file; do
    num=$(printf "%05d" $n)
    cp --preserve=timestamps "$file" ${num}_$(basename "$file")
    (( n++ ))
done

IFS=$oldifs
