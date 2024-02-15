#!/bin/bash -x

dir=$(pwd)
a=$dir/pathway/to/your/-a
b=$dir/pathway/to/your/-b
finished=$dir/pathway/to/your/output

num_files=$(ls -1 $a/*.bed | wc -l)
start_time=$(date +%s)

for i in $(seq 1 $num_files); do
   f=$(ls $a/*.bed | sed -n ${i}p)
   out="$(basename $f .bed).txt"
   echo "f: $f" >&2
   echo "out: $out" >&2
   for g in $(ls $b/*.bed); do
      echo "Running: bedtools intersect -wao -a \"$(basename "$f")\" -b \"$(basename "$g")\"" >&2
      bedtools intersect -a "$f" -b $g* -wao -filenames
   done > "$finished/$out"

   elapsed=$(( $(date +%s) - $start_time ))
   avg_time_per_file=$(( $elapsed / $i ))
   remaining_files=$(( $num_files - $i ))
   eta=$(( $remaining_files * $avg_time_per_file ))

   echo "Elapsed time: $elapsed seconds" >&2
   echo "ETA: $eta seconds" >&2

done
