# Mark tips that have been added to tree with a specific color
# take list of added sequences from fasta file validation output .txt
# results/reporting/validated/{sample}_all_fasta_headers.txt

import toytree

# Load tree FIX THIS NAMING
tree = toytree.tree("results/iqtree/{sample}_iqtree.treefile", tree_format=1)

# Load tip names from a text file
tips_to_mark = set()
with open("tips_to_mark.txt") as f:
    for line in f:
        tip = line.strip()
        if tip:  # Skip empty lines
            tips_to_mark.add(tip)

# Draw the tree and get the matplotlib axes object
# tree, axes = tree.draw(return_axes=True)

# store the objects returned from a drawing
canvas, axes, mark1 = tree.draw()

# Add markers to the specified tips
mark2 = tree.annotate.add_tip_markers(
    axes=axes,
    tipnames=tips_to_mark,
    size=8,
    color="red",
    marker="o"
)
