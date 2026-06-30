# Visualize a phylogenetic tree with toytree, marking new sequences
# -----------------------------------------------------------------

import toytree
import os

# Snakemake
newick = snakemake.input.nwk
newtips_list = snakemake.input.added
outfile = snakemake.output

# Load the tree
with open(newick) as f:
    tree1 = toytree.tree(f.read())

# Tree rooting config
cfg = snakemake.config.get("rooting", {})
outgroup_root = cfg.get("outgroup_root", False)
midpoint_root = cfg.get("midpoint_root", False)
mad_root = cfg.get("mad_root", False)
outgroup_name = cfg.get("outgroup_name", None)
outgroup_list = cfg.get("outgroup_list", False)
listnames = cfg.get("outgroup_list_names", [])

# Enforce exactly one rooting method is True
flags_true = sum(
    [bool(outgroup_root), bool(outgroup_list), bool(midpoint_root), bool(mad_root)]
)
if flags_true != 1:
    raise ValueError(
        "Config error: Exactly one of rooting.outgroup_root, rooting.outgroup_list, "
        "rooting.midpoint_root, or rooting.mad_root must be True."
    )

# Apply rooting method with midpoint fallback
if outgroup_root:
    if not outgroup_name or not isinstance(outgroup_name, str):
        raise ValueError(
            "Config error: rooting.outgroup_root=True requires rooting.outgroup_name (string)."
        )
    pattern_label = f"~{outgroup_name}"
    try:
        rtree = tree1.root(pattern_label)
        print(f"Rooted on outgroup pattern: {pattern_label}")
    except Exception as e:
        print(
            f"Warning: Outgroup pattern '{pattern_label}' failed ({e}). Falling back to midpoint root."
        )
        rtree = tree1.mod.root_on_midpoint()

elif outgroup_list:
    if not isinstance(listnames, list) or not listnames:
        raise ValueError(
            "Config error: rooting.outgroup_list=True requires rooting.outgroup_list_names "
            "(a non-empty list of tip labels or patterns)."
        )

    labels = set(tree1.get_tip_labels())
    missing = [n for n in listnames if (not n.startswith("~") and n not in labels)]
    if missing:
        print(
            f"Warning: These outgroup names are not present exactly in the tree (patterns ignored): {missing}"
        )

    try:
        rtree = tree1.root(*listnames)
        print(f"Rooted on outgroup(s): {listnames}")
    except Exception as e:
        print(
            f"Warning: Outgroup rooting with {listnames} failed ({e}). Falling back to midpoint."
        )
        rtree = tree1.mod.root_on_midpoint()

elif midpoint_root:
    rtree = tree1.mod.root_on_midpoint()
    print("Rooted on midpoint.")

elif mad_root:
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
# Add a triangle if in newly added tips
tip_labels = [f"▲ {name}" if name in tips_to_mark else name for name in original_names]

# Read from config file whether and how to colour species names
color_by_species = snakemake.config.get("color_by_species", False)
species_colors = snakemake.config.get("species_colors", {})

# Generate tip colours
tip_colors = [
    (
        "red"
        if name in tips_to_mark
        else (
            next(
                (color for species, color in species_colors.items() if species in name),
                "black",
            )
            if color_by_species
            else "black"
        )
    )
    for name in original_names
]

# Draw tree and get axes
canvas, axes, mark1 = rtree.draw(
    width=800,
    height=1600,
    node_sizes=3,
    tip_labels=tip_labels,
    tip_labels_colors=tip_colors,
)

# Annotate tips
rtree.annotate.add_tip_markers(axes=axes, size=6, color="#52373A", marker="o")

# Save to HTML
toytree.save(canvas, str(outfile))
print(f"Saved tree plot to {outfile}")
