from ast import Dict, List


def get_fmap_by_run_num(val: str, dictionary: Dict[str, List[str]]) -> str:
    """
    Get the fmap number based on the run number.

    Args:
        val (str): The run number.
        dictionary (Dict[str, List[str]]): A dictionary containing mapping of run numbers to fmap numbers.

    Returns:
        str: The corresponding fmap number.

    """
    for k, v in dictionary.items():
        if val in v:
            return k