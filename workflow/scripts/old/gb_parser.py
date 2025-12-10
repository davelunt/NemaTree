# Transforms gb to fasta, header is species_acccession
# writes a tsv file with info

from Bio import SeqIO

INFILE = "test_genbank.gb"
OUTFILE = "fa-from-gb.fas"

# with open(INFILE, "r") as inputs:
#     for rec in SeqIO.parse(inputs, "genbank"):
#         source = [feat for feat in rec.features if feat.type == "source"][0]
#         SP = " ".join(source.qualifiers["organism"][0].split()[0:2])
#         with open(OUTFILE, "w") as outputs:
#             outputs.write(f">{rec.id} {SP}\n{rec.seq}\n")
#             # outputs.write(">%s %s\n%s\n" %(rec.id,SP,rec.seq))

with open(OUTFILE, "w") as outputs:
    for seqrecord in SeqIO.parse(INFILE, "genbank"):
        source = [feat for feat in seqrecord.features if feat.type == "source"][0]
        BINOMIAL = " ".join(source.qualifiers["organism"][0].split()[0:2])
        seqrecord.description = BINOMIAL+'-'+seqrecord.id
        SeqIO.write(seqrecord, outputs, "fasta")
        SeqIO.write(seqrecord, outputs, "fasta")

