from Bio import Entrez, SeqIO

# Set your email (required by NCBI)
Entrez.email = "dave.lunt@gmail.com"

# Input and output file paths
accession_file = "../../config/alvarez_accn.txt"
# accession_file = snakemake.input.accessions
output_file = "../../resouces/gb/alvarez_seqs.gb"
# output_file = snakemake.output[0]


# Read accession numbers from file
with open(accession_file, "r") as file:
    accession_numbers = [line.strip() for line in file if line.strip()]

# Fetch sequences from GenBank rettype="gb" is alternative, elsewhere "genbank"
with Entrez.efetch(db="nucleotide", id=",".join(accession_numbers), rettype="gb", retmode="text") as handle:
    records = list(SeqIO.parse(handle, "genbank"))

# Save sequences to output file
SeqIO.write(records, output_file, "genbank")

print(f"Fetched {len(records)} sequences and saved to {output_file}")
