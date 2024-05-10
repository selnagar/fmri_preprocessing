from typing import List
import re


def parse_subject_range(subject_range: str) -> List[str]:
    '''
    Parse the subject range string into a list of subjects.

    Args:
        subject_range (str): A string containing the subject range.

    Returns:
        List[str]: A list of subjects.
    '''
    def extract_range(subject_range: str) -> List[int]:
        '''
        Extract numbers from a string.

        Args:
            subject_range (str): A string containing numbers.

        Returns:
            List[int]: A list of numbers.
        '''
        numbers = re.findall(r'\d+', subject_range)
        out = [int(num) for num in numbers]

        if len(out) != 2:
            raise ValueError(f'Invalid range: {subject_range}')

        return out

    start, end = extract_range(subject_range)
    return [f'sub-{i:02d}' for i in range(start, end + 1)]


def parse_subjects_subset(arr: list[str], pattern: str) -> list[str]:
    """
    Filters and expands a list of subjects based on a regex pattern.

    For each item in `arr`, if it matches `pattern`, it's expanded using `parse_subject_range`.
    Otherwise, it's added directly to the output list.

    Args:
        arr (list[str]): List of subject strings or ranges.
        pattern (str): Regex pattern to identify subject ranges.

    Returns:
        list[str]: Expanded list of individual subjects.
    """
    out = []
    for item in arr:
        if re.match(pattern, item):
            out.extend(parse_subject_range(item))
        else:
            out.append(item)
    return out


def find_in_string(string: str, pattern: str) -> str:
    """
    Find a pattern in a string.

    Args:
        string (str): The string to search in.
        pattern (str): The pattern to search for.

    Returns:
        str: The matched pattern.

    Raises:
        ValueError: If the pattern is not found in the string.

    """
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    else:
        raise ValueError(f'Could not find {pattern} in {string}')


