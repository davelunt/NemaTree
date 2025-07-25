# Script removes unwanted characters from FASTA headers
# These characters cause issues in newick treefiles

from Bio import SeqIO
import re

input_file = snakemake.input[0]
output_file = snakemake.output[0]

def sanitize_fasta_headers(input_file, output_file):
    altered_count = 0

    with open(output_file, "w") as out_handle:
        for record in SeqIO.parse(input_file, "fasta"):
            original_description = record.description
            # Replace specified characters with underscores
            cleaned_description = re.sub(r'[:;()\s]', '_', original_description)
            # Collapse multiple underscores into one
            cleaned_description = re.sub(r'_+', '_', cleaned_description)

            if cleaned_description != original_description:
                altered_count += 1
                record.description = cleaned_description
            SeqIO.write(record, out_handle, "fasta")

    print(f"Number of altered fasta headers: {altered_count}")

# Example usage
sanitize_fasta_headers("input.fasta", "output.fasta")
