from pathlib import Path

REF_ORIGINAL = config["reference_alignment"]
REF_FILTERED = config["filtered_ref_alignment"]

# get the reference alignment, either filtered or not according to config file
def get_ref_alignment(_wc):
    # return the path that downstream rules should use
    return REF_FILTERED if config.get("remove_seqs", False) else REF_ORIGINAL

# get the stub name of reference alignment without path or suffix
def get_ref_alignment_stub(_wc):
    ref_path = Path(get_ref_alignment(_wc))  # convert to Path object
    return ref_path.stem  # returns filename without suffix
