import os
import sys

from utils.path import save_script
sys.path.append('./')
from utils.argparsers.bashgenparser import BashGenArgParser
from utils.bash.generators import BashSequenceGenerator


if __name__ == '__main__':
    parser = BashGenArgParser()
    args = parser.parse_args()
    bashgen = BashSequenceGenerator(args)
    bash_script = bashgen.generate()

    for subject, script in zip(args.subjects, bash_script):
        save_script(
            os.path.join(
                bashgen.dir_code,
                f'run_fmriprep_{subject}.sh'
            ),
            script
        )
