# Convert alignment format with BioPython

from Bio import AlignIO

# converts between alignment formats using BioPython
# requires specifying input file format and output file format

INPUT_HANDLE = open(snakemake.input[0], "r")
OUTPUT_HANDLE = open(snakemake.output[0], "w")

AlignIO.convert(INPUT_HANDLE, snakemake.params.informat, OUTPUT_HANDLE, snakemake.params.outformat)

OUTPUT_HANDLE.close()
INPUT_HANDLE.close()

# INPUT_HANDLE = open(snakemake.input[0], "r")
# OUTPUT_HANDLE = open(snakemake.output[0], "w")

# ALIGNMENTS = AlignIO.parse(INPUT_HANDLE, snakemake.params.informat)
# AlignIO.write(ALIGNMENTS, OUTPUT_HANDLE, snakemake.params.outformat)

# OUTPUT_HANDLE.close()
# INPUT_HANDLE.close()
