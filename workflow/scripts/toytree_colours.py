# Visualize a phylogenetic tree with toytree, marking new sequences
# -----------------------------------------------------------------

import os
import toytree

# Snakemake
newick = snakemake.input.nwk
newtips_list = snakemake.input.added
outfile = snakemake.output

# Load the tree
with open(newick) as f:
    tree1 = toytree.tree(f.read())

# Tree rooting
cfg = snakemake.config.get("rooting", {})
method = cfg.get("method")

# Apply rooting, with midpoint fallback only for data-dependent failures
if cfg["method"] == "outgroup":
    pattern_label = f"~{cfg['outgroup_name']}"
    try:
        rtree = tree1.root(pattern_label)
        print(f"Rooted on outgroup pattern: {pattern_label}")
    except Exception as e:
        print(
            f"Warning: Outgroup pattern '{pattern_label}' failed ({e}). "
            f"Falling back to midpoint root."
        )
        rtree = tree1.mod.root_on_midpoint()

elif cfg["method"] == "outgroup_list":
    listnames = cfg["outgroup_list_names"]  # auto-resolved per locus

    labels = set(tree1.get_tip_labels())
    missing = [n for n in listnames if (not n.startswith("~") and n not in labels)]
    if missing:
        print(
            f"Warning: These outgroup names are not present exactly in the tree "
            f"(patterns ignored): {missing}"
        )
    try:
        rtree = tree1.root(*listnames)
        print(f"Rooted on outgroup(s): {listnames}")
    except Exception as e:
        print(
            f"Warning: Outgroup rooting with {listnames} failed ({e}). "
            f"Falling back to midpoint."
        )
        rtree = tree1.mod.root_on_midpoint()

elif cfg["method"] == "midpoint":
    rtree = tree1.mod.root_on_midpoint()
    print("Rooted on midpoint.")

elif cfg["method"] == "mad":
    try:
        rtree = tree1.mod.root_on_minimal_ancestor_deviation()
        print("Rooted using MAD.")
    except Exception as e:
        print(f"Warning: MAD rooting failed ({e}). Falling back to midpoint root.")
        rtree = tree1.mod.root_on_midpoint()


# Load tip names of newly-added sequences and handle missing files
tips_to_mark = set()
if newtips_list and os.path.exists(newtips_list):
    with open(newtips_list) as f:
        tips_to_mark = {line.strip() for line in f if line.strip()}
else:
    if newtips_list:
        print(
            f"Warning: Tip list file not found: {newtips_list}. Proceeding without highlights."
        )

# Original tip name list
original_names = rtree.get_tip_labels()


# --------------------
# Labels and styling
# --------------------

# Formatting for newly added sequences
format_added_seqs = snakemake.config.get("format_added_seqs", True)
style = snakemake.config.get("added_sequence_style", {})
added_marker = style.get("marker", "▲ ") if format_added_seqs else ""
added_color = style.get("color", "red") if format_added_seqs else None

# Prefix marker if in newly added tips
tip_labels = [
    f"{added_marker}{name}" if name in tips_to_mark else name for name in original_names
]

# Read from config file whether and how to colour species names
color_by_species = snakemake.config.get("color_by_species", False)
species_colors = snakemake.config.get("species_colors", {})


# Generate tip label colours
def get_tip_color(name):
    """Colour for tip label: red (or configured colour) for newly added
    tips, else species colour, else black."""
    if name in tips_to_mark and format_added_seqs:
        return added_color
    if color_by_species:
        return next(
            (color for species, color in species_colors.items() if species in name),
            "black",
        )
    return "black"


tip_colors = [get_tip_color(name) for name in original_names]
font_size = snakemake.config.get("font_size", 12)

# Draw tree and get axes
canvas, axes, mark1 = rtree.draw(
    width=snakemake.config.get("toytree_width", 800),
    height=snakemake.config.get("toytree_height", 1600),
    node_sizes=snakemake.config.get("toytree_node_sizes", 3),
    tip_labels=tip_labels,
    tip_labels_colors=tip_colors,
    tip_labels_style={"font-size": font_size},
    # tip_labels_style={"font-size": 6}
)

# Annotate tree tips
tipsize = snakemake.config.get("toytree_tipsize", 6)
tipcolor = snakemake.config.get("toytree_tipcolor", "#52373A")
tipmarker = snakemake.config.get("toytree_tipmarker", "o")
rtree.annotate.add_tip_markers(
    axes=axes, size=tipsize, color=tipcolor, marker=tipmarker
)

# --------------------
# Save to figure(s)
# --------------------
toytree.save(canvas, str(outfile))
print(f"Saved tree plot to {outfile}")
