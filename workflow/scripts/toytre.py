import toytree

# Get input tree files from Snakemake
newick = snakemake.input.nwk
newtips_list = snakemake.input.added
outfile = snakemake.output[0]

# Load and re-root the tree
with open(newick) as f:
    tree1 = toytree.tree(f.read())
rtree = tree1.root("~Pratylenchus")

# Load tip names of newly-added sequences
with open(newtips_list) as f:
    tips_to_mark = {line.strip() for line in f if line.strip()}

# Mapping of species substrings to colors
species_colors = {
    "javanica": "#0675b9",
    "floridensis": "#f205cb",
    "arenaria": "#049e28",
    "incognita": "#f90505",
    "haplanaria": "#aa11f1",
    "ethiopica": "#cd6df9",
    "konaensis": "#e7c2f8",
    "arabicida": "#c9b2d4",
    "paranaensis": "#a78fb3",
    "hispanica": "#bd8ed2",
    "luci": "#dbb6ed",
    "enterolobii": "#f16435",
    "hapla": "#c85490",
    "partityla": "#d6557c",
    "microtyla": "#f2a6b0",
    "spartelensis": "#f2c6d4",
    "dunensis": "#f2729a",
    "duytsi": "#f6477e",
    "graminicola": "#7bbbe3",
    "oryzae": "#83cdfa",
    "kralli": "#a6cde5",
    "naasi": "#70a7c9",
    "minor": "#1181c7",
    "chitwoodi": "#5384a3",
    "fallax": "#5ea9d7"
}

# Function to get color based on species name
def get_color(tip):
    return next((color for species, color in species_colors.items() if species in tip), "#33373a")

# Generate color list using list comprehension
colorlist = [get_color(tip) for tip in rtree.get_tip_labels()]

# Draw tree
canvas, axes, mark = rtree.draw(
    return_axes=True,
    width=800,
    height=1600,
    node_hover=True,
    node_sizes=4,
    tip_labels_colors=colorlist,
)

# Optional: Add markers to newly added tips
# mark2 = rtree.annotate.add_tip_markers(
#     axes=axes,
#     tipnames=tips_to_mark,
#     size=8,
#     color="red",
#     marker="o"
# )

# Save to HTML
toytree.save(canvas, outfile)
