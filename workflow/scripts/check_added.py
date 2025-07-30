# Check seqs are added to alignment
# ---------------------------------
# This script checks if the number of records in the final alignment
# matches the sum of records in sequences-to-be-added.fas and referencelibraqry.fas
# if not there may be a problem with the sequence addition by mafft

from Bio import SeqIO

# Replace these with your actual file paths
seqs_to_add = "file1.fasta"
reflibrary = "file2.fasta"
combined_alignment = "file3.fasta"

def count_fasta_records(file_path):
    return sum(1 for _ in SeqIO.parse(file_path, "fasta"))

# Count records in each file
count1 = count_fasta_records(seqs_to_add)
count2 = count_fasta_records(reflibrary)
count3 = count_fasta_records(combined_alignment)

# Print counts
print(f"Number of records in {seqs_to_add}: {count1}")
print(f"Number of records in {reflibrary}: {count2}")
print(f"Number of records in {combined_alignment}: {count3}")

# Check if the sum of count1 and count2 equals count3
if count1 + count2 != count3:
    print("WARNING: The sum of records in the first two files does not equal the number of records in the combined alignment. Please check.")
else:
    print("Check passed: The sum of the first two file counts matches the third file.")
