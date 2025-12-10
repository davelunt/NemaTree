
import toytree

# Get input tree files from Snakemake
newick = snakemake.input.nwk
newtips_list = snakemake.input.added
outfile = snakemake.output[0]

# Load the tree
with open(newick) as f:
    tree1 = toytree.tree(f.read())

# rooting config
cfg = snakemake.config.get('rooting', {})
outgroup_root = cfg.get('outgroup_root', False)
midpoint_root = cfg.get('midpoint_root', False)
mad_root = cfg.get('mad_root', False)
outgroup_name = cfg.get('outgroup_name', None)
outgroup_list = cfg.get('outgroup_list', False)

# Enforce one rooting method is True
flags_true = sum([bool(outgroup_root), bool(midpoint_root), bool(mad_root)])
if flags_true != 1:
    raise ValueError(
        "Config error: Exactly one of rooting.outgroup_root, rooting.outgroup_list, "
        "rooting.midpoint_root, or rooting.mad_root must be True."
    )

# Apply rooting method with midpoint fallback
if outgroup_root:
    if not outgroup_name or not isinstance(outgroup_name, str):
        raise ValueError("Config error: rooting.outgroup_root=True requires rooting.outgroup_name (string).")
    pattern_label = f"~{outgroup_name}"
    try:
        rtree = tree1.root(pattern_label)
        print(f"Rooted on outgroup pattern: {pattern_label}")
    except Exception as e:
        # Fallback: midpoint
        print(f"Warning: Outgroup pattern '{pattern_label}' failed ({e}). Falling back to midpoint root.")
        rtree = tree1.root_on_midpoint()

elif outgroup_list:
    names = cfg.get('outgroup_list_names', [])
    if not isinstance(names, list) or not names:
        raise ValueError("rooting.outgroup_root=True requires rooting.outgroup_list: a non-empty list of tip labels.")

    # Optional: validate presence (warn but still try root)
    labels = set(tree1.get_tip_labels())
    missing = [n for n in names if n not in labels]
    if missing:
        print(f"Warning: These outgroup names are not present in the tree: {missing}")
    try:
        # Unpack the list into separate args: root("r3", "r4", ...)
        rtree = tree1.root(*names)
        print(f"Rooted on outgroup(s): {names}")
    except Exception as e:
        print(f"Warning: Outgroup rooting with {names} failed ({e}). Falling back to midpoint.")
        rtree = tree1.root_on_midpoint()

elif midpoint_root:
    rtree = tree1.root_on_midpoint()
    print("Rooted on midpoint.")
elif mad_root:
    try:
        rtree = tree1.root_on_mad()
        print("Rooted using MAD.")
    except Exception as e:
        print(f"Warning: MAD rooting failed ({e}). Falling back to midpoint root.")
        rtree = tree1.root_on_midpoint()

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
    node_sizes=3,
    tip_labels_colors=tip_colors,
)

# Annotate tips
rtree.annotate.add_tip_markers(axes=axes, size=6, color="#52373A", marker="o")

# Save to HTML
toytree.save(canvas, outfile)
