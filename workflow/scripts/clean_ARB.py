# script to clean ARN fasta headers to remove taxonomy and other parts.

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import re

# Define input and output file paths
input_file = "resources/test/arb-silva.fasta"
output_file = "resources/test/arb-silva_clean_dash3.fasta"

# Function to clean and format the header
def clean_description(description):
    cleaned = re.sub(r'Eukaryota.*?Tylenchida;', '', description)
    cleaned = cleaned.replace(' ', '_')
    return cleaned

# Process the FASTA file
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for record in SeqIO.parse(infile, "fasta"):
        # Clean the description
        new_description = clean_description(record.description)
        # Replace dots with dashes in the sequence
        cleaned_seq_str = str(record.seq).replace('.', '-')
        cleaned_seq = Seq(cleaned_seq_str)
        # Create a new SeqRecord with only the cleaned description
        new_record = SeqRecord(
            cleaned_seq,
            id="",  # Empty ID so only description is used
            description=new_description
        )
        SeqIO.write(new_record, outfile, "fasta")

print(f"Cleaned FASTA records written to '{output_file}'")
