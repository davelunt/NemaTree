# Plot lengths of sequences in a fasta file as a histogram
# --------------------------------------------------------
from Bio import SeqIO
import pandas as pd
import altair as alt

# specify FASTA file
fasta_file = 'resources/samples/2012_114.fas'
# fasta_file = snakemake.input[0]

# Read sequences and store headers and lengths
data = [{'Header': record.id, 'Sequence Length': len(record.seq)} for record in SeqIO.parse(fasta_file, "fasta")]

# Create a DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to a TSV file
df.to_csv('sequence_lengths.tsv', sep='\t', index=False)

# Determine the maximum sequence length
max_length = df['Sequence Length'].max()

# Altair histogram of sequence lengths
hist = alt.Chart(df).mark_bar(color='red').encode(
    alt.X('Sequence Length:Q', bin=alt.Bin(extent=[1, max_length], maxbins=100)),
    y='count()'
).properties(
    title='Sequence Lengths (bp)',
    width=800,
)
# put count numbers above bars
text = hist.mark_text(
    align='center',
    baseline='middle',
    dy=-10,
    color='black'
).encode(
    x=alt.X('Sequence Length:Q', bin=alt.Bin(extent=[1, max_length], maxbins=100)),
    text=alt.Text('count():Q', format=',')
)

# html_outfile = snakemake.output.html
# png_outfile = snakemake.output.png

total = hist + text

# Save HTML and PNG files
total.save('sequence_length_histogram.html')
total.save('sequence_length_histogram.png', scale_factor=2)
# total.save(html_outfile)
# total.save(png_outfile, scale_factor=2)
