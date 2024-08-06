import numpy as np


def calculate_rt_offset(predicted_rts: np.ndarray, experimental_rts: np.ndarray) -> float:
    diffs = predicted_rts - experimental_rts
    return float(np.mean(diffs))


def calculate_im_offset(predicted_ims: np.ndarray, experimental_ims: np.ndarray) -> float:
    diffs = predicted_ims - experimental_ims
    return float(np.mean(diffs))
