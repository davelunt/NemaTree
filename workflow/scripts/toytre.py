# Draw trees using the toytree package
# ------------------------------------

import toytree

# get input tree files from snakemake
newick = snakemake.input.nwk

#  get a list of newly-added tipnames
newtips_list = snakemake.input.added
# newick = "results/fasttree/2012_114_mafft_trimal_fasttree.nwk"

# outfile, html format
outfile = snakemake.output[0]
# outfile = "results/reporting/toytree/2012_114_mafft_trimal_fasttree_midpoint.html"

# Load the tree from file
with open(newick) as f:
    tree1 = toytree.tree(f.read())

# re-root on internal edge selected using a regex string
rtree = tree1.root("~Pratylenchus")

# Load tip names of newly-added-sequences from text file
tips_to_mark = set()
with open(newtips_list) as f:
    for line in f:
        tip = line.strip()
        if tip:  # Skip empty lines
            tips_to_mark.add(tip)

colorlist = ["#0675b9" if "javanica" in tip
             else "#f205cb" if "floridensis" in tip
             else "#049e28" if "arenaria" in tip
             else "#f90505" if "incognita" in tip
             else "#aa11f1" if "haplanaria" in tip
             else "#cd6df9" if "ethiopica" in tip
             else "#e7c2f8" if "konaensis" in tip
             else "#c9b2d4" if "arabicida" in tip
             else "#a78fb3" if "paranaensis" in tip
             else "#bd8ed2" if "hispanica" in tip
             else "#dbb6ed" if "luci" in tip
             else "#f16435" if "enterolobii" in tip
             else "#c85490" if "hapla" in tip
             else "#d6557c" if "partityla" in tip
             else "#f2a6b0" if "microtyla" in tip
             else "#f2c6d4" if "spartelensis" in tip
             else "#f2729a" if "dunensis" in tip
             else "#f6477e" if "duytsi" in tip
             else "#7bbbe3" if "graminicola" in tip
             else "#83cdfa" if "oryzae" in tip
             else "#a6cde5" if "kralli" in tip
             else "#70a7c9" if "naasi" in tip
             else "#1181c7" if "minor" in tip
             else "#5384a3" if "chitwoodi" in tip
             else "#5ea9d7" if "fallax" in tip
             else "#33373a" for tip in rtree.get_tip_labels()]


# draw a plot and store the Canvas object to a variable
canvas, axes, mark = rtree.draw(
    return_axes=True,  # Return the matplotlib axes object
    width=800,
    height=1600,
    node_hover=True, 
    node_sizes=4, 
    # tip_labels_align=True,
    tip_labels_colors=colorlist,
    );

# # Add markers to the specified tips
# mark2 = rtree.annotate.add_tip_markers(
#     axes=axes,
#     tipnames=tips_to_mark,
#     size=8,
#     color="red",
#     marker="o")

# save annotated tree to HTML file
toytree.save(canvas, outfile)


# https://eaton-lab.org/toytree/draw-options/#tip_labels_colors
# make list of hex color values based on tip labels
# colorlist = ["#d6557c" if "rex" in tip else "#5384a3" for tip in rtre.get_tip_labels()]
# rtre.draw(
#     tip_labels_align=True, 
#     tip_labels_colors=colorlist
