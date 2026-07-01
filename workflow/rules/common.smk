from logging import config
from pathlib import Path

# reference alignments
# if config["clades123"]:
#     REFERENCE = config["reference_alignment_clades123"]
# else:
#     REFERENCE = config["reference_alignment"]

if config["clades123"]:
    REFERENCE = f"resources/reference/{config['reference_alignment_clades123']}.fas"
else:
    REFERENCE = f"resources/reference/{config['reference_alignment']}.fas"

REF_FILTERED = f"results/{config['reference_alignment']}_filtered.fas"

# get the reference alignment, either filtered or not according to config file
def get_ref_alignment(_wc):
    # return the path that downstream rules should use
    return REF_FILTERED if config.get("remove_seqs", False) else REFERENCE

# get the stub name of reference alignment without path or suffix
def get_ref_alignment_stub(_wc):
    ref_path = Path(get_ref_alignment(_wc))  # convert to Path object
    return ref_path.stem  # returns filename without suffix


def get_added_seqs(wildcards):
    return (
        f"results/samples/{wildcards.sample}_minlength.fas"
        if config.get("enforce_minlength", False)
        else f"results/samples/{wildcards.sample}_validated.fas"
    )
