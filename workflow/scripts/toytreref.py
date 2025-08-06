import toytree

# Get input tree files from Snakemake
newick = snakemake.input.nwk
# newick = "results/iqtree/alvarez_mafft_cialign_iqtree.treefile"
outfile = snakemake.output[0]
# outfile = "results/reporting/toytree/alvareztest_mafft_cialign_iqtree.html"

# Load the tree and reroot
with open(newick) as f:
    tree1 = toytree.tree(f.read())
rtree = tree1.root("~_OG")

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
    "spartelensis": "#c67891",
    "dunensis": "#d46286",
    "duytsi": "#f6477e",
    "graminicola": "#7bbbe3",
    "oryzae": "#83cdfa",
    "kralli": "#a6cde5",
    "naasi": "#70a7c9",
    "minor": "#1181c7",
    "chitwoodi": "#5384a3",
    "fallax": "#5ea9d7",
}


# Function to get color based on species name
def get_color(tip):
    return next(
        (color for species, color in species_colors.items() if species in tip),
        "#33373a",
    )


# Generate color list
colorlist = [get_color(tip) for tip in rtree.get_tip_labels()]

# Draw tree and get axes
canvas, axes, mark1 = rtree.draw(
    width=800,
    height=1600,
    # node_hover=True,
    node_sizes=3,
    tip_labels_colors=colorlist,
)

# call annotate method w/ 'axes' as an arg
mark2 = rtree.annotate.add_tip_markers(axes=axes, size=6, color="#52373A", marker="o")

# Save to HTML
toytree.save(canvas, outfile)
