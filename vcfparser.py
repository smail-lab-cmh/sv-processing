import os
import glob
import gzip

def parse_variant_line(line):
    cols = line.decode('utf-8').strip().split('\t')
    chrom, pos, filter_val, ref, alt, info, genotype_info = cols[0], cols[1], cols[6], cols[3], cols[4], cols[7], cols[9]
    genotype = genotype_info.split(':')[0]
    if filter_val != "PASS":
        return None 
    
    try:
        sv_type = [i.split('=')[1] for i in info.split(';') if i.startswith('SVTYPE')][0]
        sv_len = abs(int([i.split('=')[1] for i in info.split(';') if i.startswith('SVLEN')][0]))
        if sv_type not in ['DEL', 'DUP', 'INS', 'INV'] or sv_len < 50:
            return None
    except IndexError:
        return None 

    genotype_numeric = None
    if genotype == '0/1':
        genotype_numeric = 0.5
    elif genotype == '1/1':
        genotype_numeric = 1

    if genotype_numeric is not None:
        return chrom, pos, sv_type, sv_len, genotype_numeric
    else:
        return None

def process_vcf_file(vcf_file, output_dir):
    bed_lines = []
    with gzip.open(vcf_file, 'rb') as f:
        for line in f:
            if line.startswith(b'#'):
                continue
            variant_info = parse_variant_line(line)
            if variant_info:
                chrom, pos, sv_type, sv_len, genotype_numeric = variant_info
                end_pos = int(pos) + sv_len
                bed_lines.append(f"{chrom}\t{pos}\t{end_pos}\t{sv_len}\t{sv_type}\t{genotype_numeric}\n")

    vcf_basename = os.path.splitext(os.path.basename(vcf_file))[0].replace('.vcf.gz', '')
    bed_filename = os.path.join(output_dir, f"{vcf_basename}.bed")
    with open(bed_filename, 'w') as bed_file:
        bed_file.writelines(bed_lines)
    print(f"Generated BED file: {bed_filename}")

def process_all_vcfs(directory, output_dir):
    vcf_files = glob.glob(os.path.join(directory, '*.vcf.gz'))
    for vcf_file in vcf_files:
        process_vcf_file(vcf_file, output_dir)

input_directory = "/path/to/vcf/directory"
output_directory = "/path/to/output/directory"  
os.makedirs(output_directory, exist_ok=True)

process_all_vcfs(input_directory, output_directory)
