from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, input_format: str, bam_sorted: typing.Optional[bool], save_sorted_bam: typing.Optional[bool], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], circle_identifier: str, genome: typing.Optional[str], fasta: typing.Optional[LatchFile], bwa_index: typing.Optional[LatchDir], clip_r1: typing.Optional[int], clip_r2: typing.Optional[int], three_prime_clip_r1: typing.Optional[int], three_prime_clip_r2: typing.Optional[int], trim_nextseq: typing.Optional[int], aa_data_repo: typing.Optional[LatchDir], mosek_license_dir: typing.Optional[LatchDir], reference_build: typing.Optional[str], cnvkit_cnn: typing.Optional[str], multiqc_methods_description: typing.Optional[str], save_reference: typing.Optional[bool], skip_qc: typing.Optional[bool], skip_multiqc: typing.Optional[bool], skip_markduplicates: typing.Optional[bool], keep_duplicates: typing.Optional[bool], save_markduplicates_bam: typing.Optional[bool], skip_trimming: typing.Optional[bool], save_trimmed: typing.Optional[bool], save_merged_fastq: typing.Optional[bool], save_circle_map_intermediate: typing.Optional[bool], save_circle_finder_intermediate: typing.Optional[bool], save_unicycler_intermediate: typing.Optional[bool], aa_cngain: typing.Optional[str]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('input_format', input_format),
                *get_flag('bam_sorted', bam_sorted),
                *get_flag('save_sorted_bam', save_sorted_bam),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('circle_identifier', circle_identifier),
                *get_flag('genome', genome),
                *get_flag('fasta', fasta),
                *get_flag('save_reference', save_reference),
                *get_flag('bwa_index', bwa_index),
                *get_flag('skip_qc', skip_qc),
                *get_flag('skip_multiqc', skip_multiqc),
                *get_flag('skip_markduplicates', skip_markduplicates),
                *get_flag('keep_duplicates', keep_duplicates),
                *get_flag('save_markduplicates_bam', save_markduplicates_bam),
                *get_flag('clip_r1', clip_r1),
                *get_flag('clip_r2', clip_r2),
                *get_flag('three_prime_clip_r1', three_prime_clip_r1),
                *get_flag('three_prime_clip_r2', three_prime_clip_r2),
                *get_flag('trim_nextseq', trim_nextseq),
                *get_flag('skip_trimming', skip_trimming),
                *get_flag('save_trimmed', save_trimmed),
                *get_flag('save_merged_fastq', save_merged_fastq),
                *get_flag('save_circle_map_intermediate', save_circle_map_intermediate),
                *get_flag('save_circle_finder_intermediate', save_circle_finder_intermediate),
                *get_flag('save_unicycler_intermediate', save_unicycler_intermediate),
                *get_flag('aa_data_repo', aa_data_repo),
                *get_flag('aa_cngain', aa_cngain),
                *get_flag('mosek_license_dir', mosek_license_dir),
                *get_flag('reference_build', reference_build),
                *get_flag('cnvkit_cnn', cnvkit_cnn),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_circdna", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_circdna(input: LatchFile, input_format: str, bam_sorted: typing.Optional[bool], save_sorted_bam: typing.Optional[bool], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], circle_identifier: str, genome: typing.Optional[str], fasta: typing.Optional[LatchFile], bwa_index: typing.Optional[LatchDir], clip_r1: typing.Optional[int], clip_r2: typing.Optional[int], three_prime_clip_r1: typing.Optional[int], three_prime_clip_r2: typing.Optional[int], trim_nextseq: typing.Optional[int], aa_data_repo: typing.Optional[LatchDir], mosek_license_dir: typing.Optional[LatchDir], reference_build: typing.Optional[str], cnvkit_cnn: typing.Optional[str], multiqc_methods_description: typing.Optional[str], save_reference: typing.Optional[bool] = False, skip_qc: typing.Optional[bool] = False, skip_multiqc: typing.Optional[bool] = False, skip_markduplicates: typing.Optional[bool] = False, keep_duplicates: typing.Optional[bool] = True, save_markduplicates_bam: typing.Optional[bool] = True, skip_trimming: typing.Optional[bool] = False, save_trimmed: typing.Optional[bool] = False, save_merged_fastq: typing.Optional[bool] = False, save_circle_map_intermediate: typing.Optional[bool] = False, save_circle_finder_intermediate: typing.Optional[bool] = False, save_unicycler_intermediate: typing.Optional[bool] = False, aa_cngain: typing.Optional[str] = '4.5') -> None:
    """
    nf-core/circdna

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, input_format=input_format, bam_sorted=bam_sorted, save_sorted_bam=save_sorted_bam, outdir=outdir, email=email, multiqc_title=multiqc_title, circle_identifier=circle_identifier, genome=genome, fasta=fasta, save_reference=save_reference, bwa_index=bwa_index, skip_qc=skip_qc, skip_multiqc=skip_multiqc, skip_markduplicates=skip_markduplicates, keep_duplicates=keep_duplicates, save_markduplicates_bam=save_markduplicates_bam, clip_r1=clip_r1, clip_r2=clip_r2, three_prime_clip_r1=three_prime_clip_r1, three_prime_clip_r2=three_prime_clip_r2, trim_nextseq=trim_nextseq, skip_trimming=skip_trimming, save_trimmed=save_trimmed, save_merged_fastq=save_merged_fastq, save_circle_map_intermediate=save_circle_map_intermediate, save_circle_finder_intermediate=save_circle_finder_intermediate, save_unicycler_intermediate=save_unicycler_intermediate, aa_data_repo=aa_data_repo, aa_cngain=aa_cngain, mosek_license_dir=mosek_license_dir, reference_build=reference_build, cnvkit_cnn=cnvkit_cnn, multiqc_methods_description=multiqc_methods_description)

