#!/bin/sh

if [ $# -ne 3 ]
then
	echo "Usage: $0 <input file> <out directory> <split pieces>"
	exit 1
fi

input_file=$1
out_dir=$2
split_pieces=$3

total_lines=`wc -l $input_file | awk '{print $1}'`
piece_lines=`expr $total_lines / $split_pieces`

echo "split file: $input_file, total lines: $total_lines, split to $split_pieces, each piece: $piece_lines"

counter=0
output_file=1
for line in `cat $input_file`:
do
	if [ $counter -lt $piece_lines ]
	then
		echo $line >> $out_dir/$output_file
		counter=`expr $counter + 1`
	else
		output_file=`expr $output_file + 1`
		counter=0
	fi
done
