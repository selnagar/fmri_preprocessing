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
    out = []
    for item in arr:
        if re.match(pattern, item):
            out.extend(parse_subject_range(item))
        else:
            out.append(item)
    return out

