# Script removes unwanted characters from FASTA headers and sequences
# These characters cause issues in newick treefiles

from Bio import SeqIO
import re

input_file = snakemake.input[0]
output_file = snakemake.output.seqs
log_file = snakemake.output.log

def sanitize_fasta_headers_and_sequences(input_file, output_file, log_file):
    altered_headers = 0
    altered_sequences = 0

    with open(output_file, "w") as out_handle, open(log_file, "w") as log_handle:
        for record in SeqIO.parse(input_file, "fasta"):
            header_changed = False
            sequence_changed = False

            # Sanitize header
            original_description = record.description
            cleaned_description = re.sub(r'[:;()\s]', '_', original_description)
            cleaned_description = re.sub(r'_+', '_', cleaned_description)
            if cleaned_description != original_description:
                altered_headers += 1
                record.description = cleaned_description
                header_changed = True

            # Sanitize sequence
            original_seq = str(record.seq)
            cleaned_seq = re.sub(r'[-.?]', '', original_seq)
            if cleaned_seq != original_seq:
                altered_sequences += 1
                record.seq = record.seq.__class__(cleaned_seq)
                sequence_changed = True

            # Log altered records using full header
            if header_changed or sequence_changed:
                log_handle.write(f"{original_description}\n")

            SeqIO.write(record, out_handle, "fasta")

    print(f"Number of altered fasta headers: {altered_headers}")
    print(f"Number of altered fasta sequences: {altered_sequences}")
    print(f"Altered record headers written to: {log_file}")

# Example usage
sanitize_fasta_headers_and_sequences("input.fasta", "output.fasta", "records_cleaned_log.txt")
