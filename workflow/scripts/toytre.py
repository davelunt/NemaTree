# Draw trees using the toytree package

import toytree  # a tree plotting library

# get input and output files from snakemake
# newick = snakemake.input[0]
newick = "results/fasttree/2012_114_mafft_trimal_fasttree.nwk"
# outfile = snakemake.output[0]
outfile = "results/reporting/toytree/2012_114_mafft_trimal_fasttree_midpoint.html"

# load the tree
# tree1 = toytree.tree(newick)

# Load the tree from file
with open(newick) as f:
    tree1 = toytree.tree(f.read())

# re-root on internal edge selected using a regex string
# rtree = tree1.root("~M_artiellia")

# get a rooted tree with MAD scores stored as features
# tree1.mod.root_on_minimal_ancestor_deviation().draw(ts='p');
# rtree = tree1.mod.root_on_minimal_ancestor_deviation()

# midpoint root
rtree = tree1.mod.root_on_midpoint()

# save the tree image to a file
# draw a plot and store the Canvas object to a variable
canvas, axes, mark = rtree.draw(
    width=800,  # Width of plot
    height=1600,  # Height of plot
    node_hover=True, 
    node_sizes=4, 
    # tip_labels_align=True,
    tip_labels_colors="red",
    );

# https://eaton-lab.org/toytree/draw-options/#tip_labels_colors
# make list of hex color values based on tip labels
# colorlist = ["#d6557c" if "rex" in tip else "#5384a3" for tip in rtre.get_tip_labels()]
# rtre.draw(
#     tip_labels_align=True, 
#     tip_labels_colors=colorlist

#mike's nb rtre and rtree are different
# colorlist = ["blue" if "Minc" in tip
#              else "black" if "Mflo" in tip
#              else "red" if "Mjav" in tip
#              else "purple" if "Mhaplanaria" in tip
#              else "green" if "Mare" in tip
#              else "#5384a3" for tip in rtree.get_tip_labels()]



# HTML allows for interactivity and embedding in web sites
toytree.save(canvas, outfile)