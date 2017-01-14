#!/bin/sh

usage="	Usage:\n
	\t$0 <path> <name> <limit>\n
	count the line number of files match <name> in the <path> which line number less than <limit>"

if [ $# -lt 2 ]
then
	echo $usage
	exit 0
fi

path=$1
name=$2
limit=10000

if [ $# -gt 2 ]
then
	limit=$3
fi
echo $limit
echo "counting the line number of file $name in $path..."

total_line=0
files=`find $path -iname $name`
for file in $files
do
	echo $file
	line=`wc -l $file | awk '{print $1}'`
	if [ $line -lt $limit ]
	then
		total_line=$(($total_line+$line))
		echo "$line in file: $file"
	fi
done

echo "job done, total line number is: $total_line"
