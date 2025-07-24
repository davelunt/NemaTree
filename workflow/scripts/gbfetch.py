from Bio import Entrez, SeqIO

# Set your email (required by NCBI)
Entrez.email = "your.email@example.com"

# Input and output file paths
accession_file = "accessions.txt"
output_file = "sequences.fasta"

# Read accession numbers from file
with open(accession_file, "r") as file:
    accession_numbers = [line.strip() for line in file if line.strip()]

# Fetch sequences from GenBank rettype="gb" is alternative, elsewhere "genbank"
with Entrez.efetch(db="nucleotide", id=",".join(accession_numbers), rettype="fasta", retmode="text") as handle:
    records = list(SeqIO.parse(handle, "fasta"))

# Save sequences to output file
SeqIO.write(records, output_file, "fasta")

print(f"Fetched {len(records)} sequences and saved to {output_file}")
