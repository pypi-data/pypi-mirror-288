from typing import List, Optional, Dict

import numpy as np

from .constants import AA_TO_INDEX


def verify_sequence(sequence: str) -> bool:
    """
    Verifies that a sequence contains only valid amino acids.

    :param sequence: A peptide sequence.
    :type sequence: str

    :return: True if the sequence is valid, False otherwise.
    :rtype: bool
    """
    return all(aa in AA_TO_INDEX for aa in sequence)


def bin_encode_sequences(sequences: List[str],
                         charges: Optional[List[int]] = None,
                         aa_index_map: Optional[Dict[str, int]] = None,
                         ignore_index_error: bool = False) -> np.ndarray:

    if aa_index_map is None:
        aa_index_map = AA_TO_INDEX

    max_len = len(aa_index_map) + 1 if charges is None else len(aa_index_map) + 2
    np_arrays = np.zeros((len(sequences), max_len), dtype=int)

    for i, sequence in enumerate(sequences):
        try:
            for aa in sequence:
                aa_index = aa_index_map[aa]
                np_arrays[i, aa_index] += 1

            if charges is not None:
                np_arrays[i, -2] = len(sequence)
                np_arrays[i, -1] = charges[i]
            else:
                np_arrays[i, -1] = len(sequence)

        except KeyError as e:
            if ignore_index_error:
                np_arrays[i] = np.zeros(max_len)
            else:
                raise ValueError(f"Invalid amino acid: {e} in sequence: {sequence}")

    return np_arrays
