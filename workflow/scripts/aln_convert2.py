
from Bio import AlignIO

# Convert alignment format using BioPython

input_file = snakemake.input[0]
output_file = snakemake.output[0]
input_format = snakemake.params.informat
output_format = snakemake.params.outformat

try:
    with open(input_file, "r") as input_handle, open(output_file, "w") as output_handle:
        AlignIO.convert(input_handle, input_format, output_handle, output_format)
except Exception as e:
    print(f"Error during alignment conversion: {e}")
