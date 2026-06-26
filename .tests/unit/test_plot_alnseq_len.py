import os
import sys

import subprocess as sp
from tempfile import TemporaryDirectory
import shutil
from pathlib import Path, PurePosixPath

sys.path.insert(0, os.path.dirname(__file__))

import common


def test_plot_alnseq_len():

    with TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir) / "workdir"
        data_path = PurePosixPath(".tests/unit/plot_alnseq_len/data")
        expected_path = PurePosixPath(".tests/unit/plot_alnseq_len/expected")

        # Copy data to the temporary workdir.
        shutil.copytree(data_path, workdir)

        # dbg
        print("results/reporting/plots/Moleae_alnseqlengths.tsv results/reporting/plots/Moleae_alnseqlength_histogram.html results/reporting/plots/Moleae_alnseqlength_histogram.png", file=sys.stderr)

        # Run the test job.
        sp.check_output([
            "python",
            "-m",
            "snakemake", 
            "results/reporting/plots/Moleae_alnseqlengths.tsv results/reporting/plots/Moleae_alnseqlength_histogram.html results/reporting/plots/Moleae_alnseqlength_histogram.png",
            "-f", 
            "-j1",
            "--target-files-omit-workdir-adjustment",
    
            "--directory",
            workdir,
        ])

        # Check the output byte by byte using cmp.
        # To modify this behavior, you can inherit from common.OutputChecker in here
        # and overwrite the method `compare_files(generated_file, expected_file), 
        # also see common.py.
        common.OutputChecker(data_path, expected_path, workdir).check()
