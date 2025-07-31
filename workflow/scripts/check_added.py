from Bio import SeqIO

# files from snakemake
seqs_to_add = snakemake.input.seqs_to_add
combined_alignment = snakemake.input.combined_alignment
reflibrary = snakemake.params.reflibrary
logfile = snakemake.output.log


def count_fasta_records(file_path):
    return sum(1 for _ in SeqIO.parse(file_path, "fasta"))


# Count records in each file
count1 = count_fasta_records(seqs_to_add)
count2 = count_fasta_records(reflibrary)
count3 = count_fasta_records(combined_alignment)

# Prepare log messages
log_messages = [
    f"Number of records in {seqs_to_add}: {count1}",
    f"Number of records in {reflibrary}: {count2}",
    f"Number of records in {combined_alignment}: {count3}",
]

if count1 + count2 != count3:
    log_messages.append(
        "WARNING: The sum of records in the first two files does not equal the number of records in the combined alignment. Please check."
    )
else:
    log_messages.append(
        "Check passed: The sum of sequences in the first two files matches the final alignment."
    )

# Print to console and write to log file
for message in log_messages:
    print(message)

with open(logfile, "w") as f:
    for message in log_messages:
        f.write(message + "\n")
