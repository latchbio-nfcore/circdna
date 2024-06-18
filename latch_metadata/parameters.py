
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'input_format': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description="Specify input format. Default *FASTQ*. Options 'FASTQ' or 'BAM'.",
    ),
    'bam_sorted': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specify if bam file is sorted [false, true]. If false or not specified, bam file will be sorted!',
    ),
    'save_sorted_bam': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specify if sorted bam file should be saved [false, true]. Default: false',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'circle_identifier': NextflowParameter(
        type=str,
        default=None,
        section_title='Circular DNA identifier options',
        description="Specifies the circular DNA identification algorithm to use - available 'circle_map_realign', 'circle_map_repeats', 'circle_finder', 'circexplorer2', and 'ampliconarchitect'. Multiple circle_identifier's can be specified with a comma-separated string. E.g. `--circle_identifier 'circle_map_realign,unicycler'`.",
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'save_reference': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title=None,
        description='Save the index reference fasta in the results directory.',
    ),
    'bwa_index': NextflowParameter(
        type=typing.Optional[LatchDir],
        default=None,
        section_title=None,
        description='Path to the directory containg the BWA index files.',
    ),
    'skip_qc': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title='Process Skipping options',
        description='Skip all QC steps except for MultiQC.',
    ),
    'skip_multiqc': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title=None,
        description='Skip MultiQC step.',
    ),
    'skip_markduplicates': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title=None,
        description='Skip Picard MarkDuplicates and duplicate filtering',
    ),
    'keep_duplicates': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Keep read duplications marked by picard MarkDuplicates.',
    ),
    'save_markduplicates_bam': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Store bam with marked duplicate reads.',
    ),
    'clip_r1': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title='Read trimming options',
        description="Instructs Trim Galore to remove bp from the 5' end of read 1 (or single-end reads).",
    ),
    'clip_r2': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description="Instructs Trim Galore to remove bp from the 5' end of read 2 (paired-end reads only).",
    ),
    'three_prime_clip_r1': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description="Instructs Trim Galore to remove bp from the 3' end of read 1 AFTER adapter/quality trimming has been performed.",
    ),
    'three_prime_clip_r2': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description="Instructs Trim Galore to remove bp from the 3' end of read 2 AFTER adapter/quality trimming has been performed.",
    ),
    'trim_nextseq': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Instructs Trim Galore to apply the --nextseq=X option, to trim based on quality after removing poly-G tails.',
    ),
    'skip_trimming': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title=None,
        description='Skip the adapter trimming step.',
    ),
    'save_trimmed': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title=None,
        description='Save the trimmed FastQ files in the results directory.',
    ),
    'save_merged_fastq': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title=None,
        description='Save the merged FastQ files in the results directory.',
    ),
    'save_circle_map_intermediate': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title='circle-map options',
        description='Store bam file with read candidates for circle-map circular dna calling.',
    ),
    'save_circle_finder_intermediate': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title='Circle_finder options',
        description='Store bed files created during Circle_finder run.',
    ),
    'save_unicycler_intermediate': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title='Unicycler options',
        description='Store fastq intermediate files created during Uniycler run.',
    ),
    'aa_data_repo': NextflowParameter(
        type=typing.Optional[LatchDir],
        default=None,
        section_title='ampliconarchitect options',
        description='Absolute path to the downloaded AA data repository. See [AmpliconArchitect](https://github.com/jluebeck/AmpliconArchitect).',
    ),
    'aa_cngain': NextflowParameter(
        type=typing.Optional[str],
        default='4.5',
        section_title=None,
        description='Copy Number Threshold for seeds to be considered by AmpliconArchitect.',
    ),
    'mosek_license_dir': NextflowParameter(
        type=typing.Optional[LatchDir],
        default=None,
        section_title=None,
        description="Path to the directory containing the mosek license file 'mosek.lic'.",
    ),
    'reference_build': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description="When running AmpliconArchitect, specify reference build ['GRCh37', 'GRCh38', 'mm10']. This is *mandatory* to match fasta and AA reference build!",
    ),
    'cnvkit_cnn': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description="Path to cnn file inside the AmpliconArchitect Data Repository of the respective reference genome. By default it uses the 'aa_data_repo' and the 'reference_build' input to construct the file path.",
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

