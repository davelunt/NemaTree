# This script parses GenBank files and outputs sequences in FASTA format
# and a TSV file with species, accession, description, length, and sequence.

from Bio import SeqIO
import csv

# Input and output file paths
input_file=snakemake.input[0]
fasta_output = snakemake.output.fasta
tsv_output = snakemake.output.tsv

# Open the output FASTA and TSV files
with open(fasta_output, "w") as fasta_out, open(tsv_output, "w", newline='') as tsv_out:
    tsv_writer = csv.writer(tsv_out, delimiter='\t')
    # Write header row for TSV
    tsv_writer.writerow(["Species", "Accession", "Description", "Length", "Sequence"])

    for record in SeqIO.parse(input_file, "genbank"):
        # Extract species name and accession
        species = record.annotations.get("organism", "Unknown_species").replace(" ", "_")
        accession = record.id
        description = record.description
        sequence = str(record.seq)
        length = len(record.seq)

        # Write to FASTA with custom header
        record.id = f"{species}_{accession}"
        record.description = ""
        SeqIO.write(record, fasta_out, "fasta")

        # Write to TSV
        tsv_writer.writerow([species, accession, description, length, sequence])
