from contextlib import redirect_stdout, redirect_stderr
import re
import traceback
from Bio import SeqIO
from Bio.Seq import Seq

# Snakemake inputs
input_file = snakemake.input.raw
output_file = snakemake.output.seqs
newnames_file = snakemake.output.newnames
original_names_file = snakemake.output.names
log = snakemake.log[0]

def sanitize_fasta_headers_and_sequences(
    input_file: str,
    output_file: str,
    newnames_file: str,
    original_names_file: str,
) -> None:
    """Sanitize FASTA headers (replace ()[];,: and whitespace with _) and
    sequences (strip -.?). Writes a .tsv file of any altered headers.

    Fails loudly if the file is unreadable, contains no records, or if any
    header/sequence is or would be empty after sanitization.
    """

    # Read and parse the FASTA file, failing loudly if unreadable
    try:
        records = list(SeqIO.parse(input_file, "fasta"))
    except Exception as e:
        raise RuntimeError(f"Failed to read '{input_file}': {e}") from e

    # Fail loudly if nothing parsed (empty file or entirely invalid content)
    if not records:
        raise RuntimeError(
            f"'{input_file}' contains no valid FASTA records."
        )

    altered_headers = 0
    altered_sequences = 0
    altered_rows = []  # file written only if non-empty

    with open(output_file, "w") as out_handle, \
         open(original_names_file, "w") as all_handle:

        for index, record in enumerate(records, start=1):
            # Log all original headers
            all_handle.write(f"{record.description}\n")

            # Sanitize header: replace ()[];,: and whitespace with _
            original_description = record.description
            cleaned_description = re.sub(r"[\[\]():,;\s]", "_", original_description)
            cleaned_description = re.sub(r"_+", "_", cleaned_description)
            cleaned_description = cleaned_description.strip("_")

            # Fail loudly if header is empty either originally
            # or became empty after sanitization
            if not cleaned_description:
                if not original_description:
                    raise ValueError(
                        f"Record {index} in {input_file} has an empty header "
                        f"(bare '>' line in the FASTA). Fix the input file."
                    )
                else:
                    raise ValueError(
                        f"Header '{original_description}' (record {index} in "
                        f"{input_file}) would be empty after sanitization. "
                        f"Fix the input file instead."
                    )

            if cleaned_description != original_description:
                altered_headers += 1
                record.id = cleaned_description
                record.description = cleaned_description
                altered_rows.append(
                    f"{original_description}\t{record.description}"
                )

            # Remove -.? symbols from sequence
            original_seq = str(record.seq)
            cleaned_seq = re.sub(r"[-.?]", "", original_seq)

            # Fail loudly if sanitization empties the sequence
            if not cleaned_seq:
                raise ValueError(
                    f"Sequence '{original_description}' (record {index} in "
                    f"{input_file}) is empty after removing gap/ambiguous "
                    f"symbols (original length {len(original_seq)}). "
                    f"Fix the input file instead."
                )

            # count if the sequence has been changed
            if cleaned_seq != original_seq:
                altered_sequences += 1

            # standardise sequence to UPPER case
            record.seq = Seq(cleaned_seq.upper())

            # write the records as fasta to a file
            SeqIO.write(record, out_handle, "fasta")

    # Write the alteration TSV only if any headers were actually changed
    if altered_rows:
        with open(newnames_file, "w") as altered_handle:
            altered_handle.write("Original_Header\tAltered_Header\n")
            altered_handle.write("\n".join(altered_rows) + "\n")

    print(f"FASTA file cleaning and validation of {input_file}")
    print("--------------------------------------------------------")
    print(f"Number of altered FASTA headers: {altered_headers}")
    print(f"Number of altered FASTA sequences: {altered_sequences}")
    if altered_rows:
        print(f"Altered record headers written to TSV: {newnames_file}")
    else:
        print("No altered headers; alteration TSV not written")
    print(f"All sequence names written to: {original_names_file}")
    print(f"All validated FASTA records written to: {output_file}")

# Redirect stdout/stderr to the Snakemake rule's log file
try:
    with open(log, "w") as log_handle, \
         redirect_stdout(log_handle), \
         redirect_stderr(log_handle):
        sanitize_fasta_headers_and_sequences(
            input_file, output_file, newnames_file, original_names_file
        )
except Exception:
    # Ensure a failed job leaves a traceback in the Snakemake log file
    with open(log, "a") as log_handle:
        traceback.print_exc(file=log_handle)
    raise
