# check that sequences were added to the reference alignment and exit if not

from Bio import SeqIO

# Files from Snakemake
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

# Initial log baseline
log_messages = [
    f"Number of records in {seqs_to_add}: {count1}",
    f"Number of records in {reflibrary}: {count2}",
    f"Number of records in {combined_alignment}: {count3}",
]


def write_log_and_fail(error_message):
    """Helper to ensure logs are fully captured before crashing the pipeline."""
    log_messages.append(f"FATAL ERROR: {error_message}")
    with open(logfile, "w") as f:
        f.write("\n".join(log_messages) + "\n")
    raise ValueError(error_message)


# Throw exception and quit if count1 is zero
if count1 == 0:
    write_log_and_fail(f"No new sequences found in {seqs_to_add}. Nothing to process.")

# Throw exception and quit if count2 is zero
if count2 == 0:
    write_log_and_fail(f"The reference library {reflibrary} is empty.")

# Throw exception and quit if count3 is less than or equal to count2
if count3 <= count2:
    write_log_and_fail(
        f"Combined alignment count ({count3}) is not greater than reference alignment count ({count2}). "
        f"No records appear to have been added"
    )

# Warn if count3 is less than count1 + count2
if count3 < (count1 + count2):
    log_messages.append(
        f"WARNING: Combined alignment has fewer sequences ({count3}) than expected ({count1 + count2}). "
        f"Some sequences may have had identical IDs and were merged/dropped by the aligner."
    )
else:
    log_messages.append(
        "Check passed: Target sequence counts match expected totals."
    )

# Standard success pathway execution
for message in log_messages:
    print(message)

with open(logfile, "w") as f:
    f.write("\n".join(log_messages) + "\n")
