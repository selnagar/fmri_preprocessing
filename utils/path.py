import os


def join_or_make(a: str, *args: str) -> str:
    """
    Join paths and create directories if they don't exist.

    Args:
        a (str): Initial path.
        *args (str): Additional paths to join.

    Returns:
        str: Joined path.

    """
    for arg in args:
        a = os.path.join(a, arg)

        if not os.path.exists(a):
            os.makedirs(a)

    return a