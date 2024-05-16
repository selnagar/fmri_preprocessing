#! ./venv/bin/python

import os
import sys
sys.path.append('./')

from utils.path import save_script
from utils.argparsers.bashgenparser import BashGenArgParser
from utils.bash.generators import BashScriptGenerator
from utils.parse import find_in_string
import argparse


class BashGroupsGenerator(BashScriptGenerator):
    def __init__(self, args: argparse.Namespace):
        super().__init__(args)
        self.group_size = args.group_size

    def generate(self) -> list[str]:
        '''
        Generates bash script for every group of participants based on group size input

        Returns:
            list[str]: A list of bash script for every group of participants
        '''
        all_scripts = [bash_str for bash_str in self]
        group_scripts = self.split_list(all_scripts)
        group_scripts = [''.join(group_script) for group_script in group_scripts]
        group_scripts = [self.kernel + group_script for group_script in group_scripts]

        return group_scripts

    def split_list(self, lst: list[str]) -> list[list[str]]:
        return [lst[i:i+self.group_size] for i in range(0, len(lst), self.group_size)]


if __name__ == '__main__':
    parser = BashGenArgParser()
    parser.add_argument(
        '-gs', '--groupsize',
        dest='group_size',
        type=int,
        default=3,
        help='how many participants per bash script (default 3)'
    )
    args = parser.parse_args()
    args.subjects = sorted(args.subjects)
    bashgen = BashGroupsGenerator(args)
    bash_script = bashgen.generate()
    subject_groups = bashgen.split_list(args.subjects)
    pattern = r'-?(\d+)'
    subject_groups = [f'{group[0]}:{find_in_string(group[-1], pattern)}' if len(group) > 1 else group[0] for group in subject_groups]

    for grup, script in zip(subject_groups, bash_script):
        save_script(
            os.path.join(
                bashgen.dir_code,
                f'run_fmriprep_group_{grup}.sh'
            ),
            script
        )
