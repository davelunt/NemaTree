import toytree

# Get input tree files from Snakemake
newick = snakemake.input.nwk
newtips_list = snakemake.input.added
outfile = snakemake.output[0]

# Load the tree and reroot
with open(newick) as f:
    tree1 = toytree.tree(f.read())
rtree = tree1.root("~Pratylenchus")
# Pratylenchus

# Load tip names of newly-added sequences
with open(newtips_list) as f:
    tips_to_mark = {line.strip() for line in f if line.strip()}

# Create a color list for tip labels
tip_colors = [
    "red" if name in tips_to_mark else "black" for name in rtree.get_tip_labels()
]

# Draw tree and get axes
canvas, axes, mark1 = rtree.draw(
    width=800,
    height=1600,
    # node_hover=True,
    node_sizes=3,
    tip_labels_colors=tip_colors,
)

# call annotate method w/ 'axes' as an arg
mark2 = rtree.annotate.add_tip_markers(axes=axes, size=6, color="#52373A", marker="o")

# Save to HTML
toytree.save(canvas, outfile)
