from Bio import SeqIO
import re

input_file = snakemake.input.raw
output_file = snakemake.output.seqs
log_altered = snakemake.output.log
log_all = snakemake.output.names


def sanitize_fasta_headers_and_sequences(input_file, output_file, log_altered, log_all):
    altered_headers = 0
    altered_sequences = 0


    # Parse all records first to check for empty input
    records = list(SeqIO.parse(input_file, "fasta"))
    if not records:
        print(f"No records found in {input_file}")
        return

    with open(output_file, "w") as out_handle, open(
        log_altered, "w"
    ) as altered_handle, open(log_all, "w") as all_handle:

        # Write header for TSV log file of altered records
        altered_handle.write("Original_Header\tAltered_Header\n")

        for record in records:
            header_changed = False
            sequence_changed = False

            # Write all original headers
            all_handle.write(f"{record.description}\n")

            # Sanitize header to remove whitespace and ()[]:;
            original_description = record.description
            cleaned_description = re.sub(r"[:;()\s]", "_", original_description)
            cleaned_description = re.sub(r"_+", "_", cleaned_description)
            if cleaned_description != original_description:
                altered_headers += 1
                record.description = cleaned_description
                header_changed = True

            # Sanitize sequence to remove -.? symbols
            original_seq = str(record.seq)
            cleaned_seq = re.sub(r"[-.?]", "", original_seq)
            if cleaned_seq != original_seq:
                altered_sequences += 1
                record.seq = record.seq.__class__(cleaned_seq)
                sequence_changed = True

            # Log altered headers as TSV
            if header_changed or sequence_changed:
                altered_handle.write(f"{original_description}\t{record.description}\n")

            # Write validated fasta record to output file
            SeqIO.write(record, out_handle, "fasta")

    print(f"FASTA file cleaning and validation of {input_file}")
    print("--------------------------------------------------------")
    print(f"Number of altered FASTA headers: {altered_headers}")
    print(f"Number of altered FASTA sequences: {altered_sequences}")
    print(f"Altered record headers written to TSV: {log_altered}")
    print(f"All sequence names written to: {log_all}")
    print(f"All validated FASTA records written to: {output_file}")


sanitize_fasta_headers_and_sequences(input_file, output_file, log_altered, log_all)
