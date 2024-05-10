import logging
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


def save_script(savepath: str, script: str) -> None:
    """
    Save a script to a file.

    Args:
        savepath (str): The path to save the script to.
        script (str): The script to save.

    """
    with open(savepath, 'w') as f:
        f.write(script)

    logging.info(f'Script written to {savepath}')

    try:
        os.system(f'chmod a+rwx {savepath}')
    except Exception as e:
        logging.error(f'Error changing permissions:\n{e}')