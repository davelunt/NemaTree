from Bio import SeqIO
from collections import defaultdict

input_file = "results/mafft/alvarez_mafft.fas"
output_file = "results/mafft/alvarez_mafft_uniq.fas"

# Dictionary to count occurrences of each description
description_counts = defaultdict(int)

# List to store modified records
unique_records = []

for record in SeqIO.parse(input_file, "fasta"):
    desc = record.description
    description_counts[desc] += 1

    if description_counts[desc] > 1:
        # Append suffix to make it unique
        new_desc = f"{desc}_{description_counts[desc] - 1}"
        record.description = new_desc
        record.id = new_desc.split()[0]  # Update ID to match new description
    else:
        record.id = desc.split()[0]  # Ensure ID matches description

    unique_records.append(record)

# Write modified records to output file
SeqIO.write(unique_records, output_file, "fasta")
