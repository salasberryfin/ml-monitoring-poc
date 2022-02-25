import os


DRIFT_THRESHOLD = os.getenv("DRIFT_THRESHOLD", "0.005")


def get_drift(pvalue: float) -> int:
    """
    Compare pvalue to given threshold and return 1 if drifted

    Args:
        pvalue:float    output from drift analysis

    Return:
        bool            1 if drifted | 0 is not drifted
    """

    if pvalue >= float(DRIFT_THRESHOLD):
        return 1

    return 0
