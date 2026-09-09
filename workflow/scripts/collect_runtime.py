#!/usr/bin/env python
"""Collect per-job runtime data from Snakemake metadata for the dashboard.

Runs as a Snakemake `script:` rule. Emits a per-job detail CSV and a
per-rule summary CSV from the metadata records in .snakemake/metadata.

Records belong to this run only if their recovered sample is in
config.yaml; everything else is old-debris and is excluded with a count.
"""
import base64
import csv
import json
import statistics
import sys
from pathlib import Path

META_DIR = Path(".snakemake/metadata")

# Where the sample name ends in each output filename, longest first.
SAMPLE_MARKERS = sorted(
    [
        "_mafft_cialign",
        "_mafft_duplist.txt",
        "_mafft_nodups.fas",
        "_mafft.fas",
        "_checkaddseqs_log.txt",
        "_length_histogram.png",
        "_length_histogram.html",
        "_lengths.tsv",
        "_alnseqlength_histogram.png",
        "_alnseqlength_histogram.html",
        "_alnseqlengths.tsv",
        "_seqkit_report.md",
        "_validated.fas",
        "_all_fasta_headers.txt",
        "_clean_fasta_log.txt",
    ],
    key=len,
    reverse=True,
)

def decode_record_name(name: str) -> str | None:
    """Metadata filenames are the base64 of the output file path.
    Inferred empirically; not a documented Snakemake guarantee."""
    try:
        return base64.urlsafe_b64decode(name + "===").decode()
    except Exception:
        return None

def extract_sample(paths: list[str]) -> str | None:
    """Recover the sample name from a record's paths, or None if no
    marker matches (new rule? stale record? add to SAMPLE_MARKERS)."""
    for p in paths:
        name = Path(p).name
        for marker in SAMPLE_MARKERS:
            if marker in name:
                return name.split(marker)[0]
    return None

def unquote(s: str) -> str:
    """Strip Snakemake's repr-quoting from params entries."""
    return s.strip().strip("'\"")

def main() -> None:
    import yaml

    config_path = snakemake.input.config
    detail_csv = snakemake.output.detail
    summary_csv = snakemake.output.summary

    with open(config_path) as fh:
        config_samples = set(yaml.safe_load(fh)["samples"])

    jobs = []
    skipped_stale = 0
    warned_versions = set()

    for path in META_DIR.rglob("*"):
        if not path.is_file():
            continue
        try:
            meta = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        if meta.get("incomplete"):
            continue

        version = meta.get("record_format_version")
        if version != 6 and version not in warned_versions:
            print(
                f"Warning: {path.name} uses record_format_version {version} "
                f"(collector built for v6) — attempting anyway.",
                file=sys.stderr,
            )
            warned_versions.add(version)

        # Validate the fields we rely on; values must be non-null
        # (interrupted runs can leave explicit nulls).
        required_ok = (
            isinstance(meta.get("rule"), str)
            and isinstance(meta.get("starttime"), (int, float))
            and isinstance(meta.get("endtime"), (int, float))
        )
        if not required_ok:
            print(
                f"Warning: {path.name} missing or null rule/starttime/endtime; "
                f"skipping (likely an interrupted or in-flight job).",
                file=sys.stderr,
            )
            continue

        output_path = decode_record_name(path.name)
        candidates = (
            meta.get("input") or []
        ) + [unquote(p) for p in meta.get("params") or []] + (
            [output_path] if output_path else []
        )
        sample = extract_sample(candidates)

        if sample is None:
            print(
                f"Warning: no sample marker matched in {path.name} "
                f"(rule '{meta['rule']}'); check SAMPLE_MARKERS; skipping.",
                file=sys.stderr,
            )
            continue
        if sample not in config_samples:
            skipped_stale += 1  # counted, not warned per record
            continue

        jobs.append(
            {
                "rule": meta["rule"],
                "job_hash": meta.get("job_hash") or "",
                "runtime_secs": round(meta["endtime"] - meta["starttime"], 2),
                "sample": sample,
                "inputs": ";".join(meta.get("input") or []),
                "shellcmd": " ".join((meta.get("shellcmd") or "").split()),
            }
        )

    if skipped_stale:
        print(
            f"Note: excluded {skipped_stale} record(s) for samples not in "
            f"config.yaml (old runs / removed samples).",
            file=sys.stderr,
        )

    found_samples = {j["sample"] for j in jobs if j["sample"]}
    missing = config_samples - found_samples
    if missing:
        print(
            f"Warning: no jobs found for configured sample(s): {sorted(missing)}",
            file=sys.stderr,
        )

    # ---- detail CSV: one row per job ----
    with open(detail_csv, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "rule", "job_hash", "runtime_secs", "sample", "inputs", "shellcmd",
            ],
        )
        writer.writeheader()
        writer.writerows(jobs)

    # ---- summary CSV: one row per rule ----
    by_rule: dict[str, list[float]] = {}
    for job in jobs:
        by_rule.setdefault(job["rule"], []).append(job["runtime_secs"])

    with open(summary_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["rule", "n_jobs", "total_secs", "median_secs", "max_secs"]
        )
        for rule, runtimes in sorted(by_rule.items()):
            writer.writerow(
                [
                    rule,
                    len(runtimes),
                    round(sum(runtimes), 2),
                    round(statistics.median(runtimes), 2),
                    max(runtimes),
                ]
            )


main()
