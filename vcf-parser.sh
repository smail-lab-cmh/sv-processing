#!/bin/bash

input="/path/to/vcfs"
output="/path/to/output"

mkdir -p "$output"

for file in "$input"/*.vcf; do
    filename=$(basename "$file")
    output_file="${filename%.*}.bed"
    output_path="$output/$output_file"

    awk -F '\t' '($7 == "PASS") {
        split($8, sv_fields, ";")
        split($10, gt_fields, ":")
        end_val = ""
        len_val = ""
        type_val = ""
        for (i=1; i<=length(sv_fields); i++) {
            if (sv_fields[i] ~ /^END=/) {
                split(sv_fields[i], end, "=")
                end_val = end[2]
            }
            if (sv_fields[i] ~ /^SVLEN=/) {
                split(sv_fields[i], svlen, "=")
                len_val = svlen[2]
            }
            if (sv_fields[i] ~ /^SVTYPE=/) {
                split(sv_fields[i], svtype, "=")
                type_val = svtype[2]
            }
        }
        if (len_val > 50) {
            print $1, $2, end_val, len_val, type_val
        }
    }' "$file" > "$output_path"
done
