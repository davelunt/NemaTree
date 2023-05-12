import toyplot  # a general plotting library
import toytree  # a tree plotting library

# get input and output files from snakemake
newick = snakemake.input[0]
outfile = snakemake.output[0]

# load the tree
tre1 = toytree.tree(newick, tree_format=5)  # ETE3 numbering?

# root tree with outgroup
# rtre = tre1.root(wildcard="Macaca")  # specify the outgroup taxon

# store the returned Canvas and Axes objects
canvas, axes = tre1.draw(
    width=300,
    height=300,
    tip_labels=True,
    tip_labels_align=True
)

# show the axes coordinates
axes.show = True
axes.x.ticks.show = True
axes.y.ticks.show = False

# draw tree as html
toyplot.html.render(canvas, outfile)
