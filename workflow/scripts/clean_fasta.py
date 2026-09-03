from Bio import SeqIO
from Bio.Seq import Seq
import re

input_file = snakemake.input.raw
output_file = snakemake.output.seqs
log_altered = snakemake.output.log
log_all = snakemake.output.names

def sanitize_fasta_headers_and_sequences(
    input_file: str, output_file: str, log_altered: str, log_all: str
) -> None:
    """Sanitize FASTA headers (replace ()[];: and whitespace with _) and
    sequences (strip gap/ambiguous symbols -?). Writes a TSV of altered
    headers, but only if any headers were changed (optional record file).

    Fails loudly if the file is unreadable, contains no records, or if any
    header/sequence would be empty after sanitization.
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
    altered_rows = []  # buffered TSV rows; file written only if non-empty

    with open(output_file, "w") as out_handle, \
         open(log_all, "w") as all_handle:

        for index, record in enumerate(records, start=1):
            # Log all original headers
            all_handle.write(f"{record.description}\n")

            # Sanitize header: replace ()[];: and whitespace with _
            original_description = record.description
            cleaned_description = re.sub(r"[\[\]():;\s]", "_", original_description)
            cleaned_description = re.sub(r"_+", "_", cleaned_description)
            cleaned_description = cleaned_description.strip("_")

            # Single check: fail loudly if header is empty either originally
            # or became empty after sanitization (e.g., '>(x)' or bare '>')
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

            # Sanitize sequence: remove gap/ambiguous symbols
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

            if cleaned_seq != original_seq:
                altered_sequences += 1
                record.seq = Seq(cleaned_seq)

            SeqIO.write(record, out_handle, "fasta")

    # Write the alteration TSV only if any headers were actually changed;
    # this file is optional record keeping, so it may legitimately not exist.
    if altered_rows:
        with open(log_altered, "w") as altered_handle:
            altered_handle.write("Original_Header\tAltered_Header\n")
            altered_handle.write("\n".join(altered_rows) + "\n")

    print(f"FASTA file cleaning and validation of {input_file}")
    print("--------------------------------------------------------")
    print(f"Number of altered FASTA headers: {altered_headers}")
    print(f"Number of altered FASTA sequences: {altered_sequences}")
    if altered_rows:
        print(f"Altered record headers written to TSV: {log_altered}")
    else:
        print("No altered headers; alteration TSV not written")
    print(f"All sequence names written to: {log_all}")
    print(f"All validated FASTA records written to: {output_file}")

sanitize_fasta_headers_and_sequences(input_file, output_file, log_altered, log_all)