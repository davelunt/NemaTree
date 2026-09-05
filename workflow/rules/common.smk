# Samples from config
SAMPLES = list(config["samples"].keys())


def get_raw_input(wildcards):
    """Retrieves the original raw user path for the initial rule."""
    return config["samples"][wildcards.sample]


def get_added_seqs(wildcards):
    """
    Evaluates files *already processed* inside results/
    ie downstream input function. Selects based on config file
    """
    if config.get("enforce_minlength", False):
        return f"results/samples/{wildcards.sample}_valid_minlen.fas"
    else:
        return f"results/samples/{wildcards.sample}_validated.fas"


# get correct reference alignment from config
# -------------------------------------------
VALID_LOCI = {"SSU", "LSU"}
VALID_SCOPES = {"genus", "clades123"}


def get_reference(config):
    """Resolve the reference alignment path from locus and scope choices."""
    locus = config["locus"]
    scope = config["scope"]

    if locus not in VALID_LOCI:
        raise ValueError(
            f"config 'locus' must be one of {sorted(VALID_LOCI)}, got '{locus}'"
        )
    if scope not in VALID_SCOPES:
        raise ValueError(
            f"config 'scope' must be one of {sorted(VALID_SCOPES)}, got '{scope}'"
        )

    return config["reference_alignments"][locus][scope]


def get_cialignment(wildcards):
    """
    Pass the current alignment, which can vary based on config
    """
    if config.get("cialign_len_filter", False):
        return f"results/cialign/{wildcards.sample}_mafft_cialign_shortremoved_cleaned.fasta"
    else:
        return f"results/mafft/{wildcards.sample}_mafft_nodups.fas"


def cialign_short_retain_arg():
    """
    Pass the file of sequences to retain, irrespective of length, if
    config retain_short_list_seqs: True
    """
    if config.get("retain_short_list_seqs", False):
        return f'--remove_short_retain_list "{config["cialign_retain_short_list"]}"'
    return ""


# rooting the tree in toytree
# ---------------------------
VALID_ROOTING_METHODS = {"outgroup", "outgroup_list", "midpoint", "mad"}

def get_rooting(config):
    """Validate the rooting config and resolve it to a clean dict:
    {"method": <str>} plus the parameter that method needs."""

    rooting = config["rooting"]
    method = rooting.get("method")

    if method not in VALID_ROOTING_METHODS:
        raise ValueError(
            f"config 'rooting.method' must be one of "
            f"{sorted(VALID_ROOTING_METHODS)}, got '{method}'"
        )

    if method == "outgroup":
        name = rooting.get("outgroup_name")
        if not name or not isinstance(name, str):
            raise ValueError(
                "config 'rooting.method=outgroup' requires a string "
                "'rooting.outgroup_name'"
            )
        return {"method": method, "outgroup_name": name}

    if method == "outgroup_list":
        # Resolve the correct list automatically from the chosen locus
        lists = rooting.get("outgroup_lists", {})
        locus = config["locus"]
        names = lists.get(locus)
        if not names:
            raise ValueError(
                f"config 'rooting.method=outgroup_list' requires a non-empty "
                f"'rooting.outgroup_lists[{locus}]'"
            )
        return {"method": method, "outgroup_list_names": names}

    # midpoint and mad need no parameters
    return {"method": method}


# get sequence substitution model from config
# -------------------------------------------
def get_substitution_model(config):
    """Resolve the IQ-TREE substitution model for the chosen locus."""
    locus = config["locus"]
    models = config.get("subst_models", {})

    if locus not in VALID_LOCI:
        raise ValueError(f"config 'locus' must be one of {sorted(VALID_LOCI)}, got '{locus}'")
    if locus not in models:
        raise ValueError(
            f"config 'subst_models' has no entry for locus '{locus}'. "
            f"Available: {sorted(models)}"
        )

    return models[locus]
