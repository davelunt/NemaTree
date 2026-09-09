# collect data about the run from snakemake's json outputs
rule runtime_collect:
    input:
        config="config/config.yaml",
        final=TOYTREE_PLOTS,        # DAG anchor: waits for all terminal outputs
    output:
        detail="results/reporting/jobs_detail.csv",
        summary="results/reporting/summary_by_rule.csv",
    log:
        "results/reporting/collect_runtime_log.txt",
    script:
        Path(workflow.basedir) / "scripts" / "collect_runtime.py"
