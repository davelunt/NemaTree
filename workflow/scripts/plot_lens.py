from Bio import SeqIO
import pandas as pd
import altair as alt

# Specify file locations via Snakemake
fasta_file = snakemake.input[0]
seq_lengths_tsv = snakemake.output.tsv
html_outfile = snakemake.output.html
png_outfile = snakemake.output.png
sample_name = snakemake.wildcards.sample

# Characters to exclude from length calculation
exclude_chars = set("-?N")

# Parse FASTA and compute cleaned sequence lengths
data = []
for record in SeqIO.parse(fasta_file, "fasta"):
    cleaned_seq = "".join(base for base in str(record.seq) if base not in exclude_chars)
    data.append({
        "Header": record.description,
        "Sequence Length": len(cleaned_seq)
    })

# Create and sort DataFrame
df = pd.DataFrame(data)
df_sorted = df.sort_values(by="Sequence Length", ascending=True)

# Save sorted data to TSV
df_sorted.to_csv(seq_lengths_tsv, sep="\t", index=False)

# Bin sequence lengths into intervals of 5
bin_step = 5
df_sorted["Length Bin"] = (df_sorted["Sequence Length"] // bin_step) * bin_step

# Group by bin and aggregate headers
bin_summary = df_sorted.groupby("Length Bin").agg({
    "Header": lambda x: ", ".join(x),
    "Sequence Length": "count"
}).reset_index().rename(columns={
    "Sequence Length": "Count",
    "Header": "Headers"
})

# Create histogram with Altair
hist = (
    alt.Chart(bin_summary)
    .mark_bar(color="red")
    .encode(
        alt.X("Length Bin:Q", title="Sequence Length"),
        alt.Y("Count:Q", title="Number of Sequences per Bin"),
        tooltip=[alt.Tooltip("Headers:N", title="Sequence Headers")]
    )
    .properties(
        title=f"{sample_name} Sequence Lengths Histogram",
        width=1200,
    )
)

# Add count labels above bars
text = hist.mark_text(
    align="center",
    baseline="bottom",
    dy=-2,
    color="black"
).encode(
    text=alt.Text("Count:Q", format=",")
)

# Combine chart and labels
total = hist + text

# Save outputs
total.save(html_outfile)
total.save(png_outfile, scale_factor=2)
