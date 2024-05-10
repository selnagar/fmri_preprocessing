import os
import sys

sys.path.append('./')
from utils.path import save_script
from utils.argparsers.bashgenparser import BashGenArgParser
from utils.bash.generators import BashScriptGenerator


if __name__ == '__main__':
    parser = BashGenArgParser()
    args = parser.parse_args()
    bashgen = BashScriptGenerator(args)
    bash_script = bashgen.generate()

    save_script(
        os.path.join(bashgen.dir_code, 'run_fmriprep.sh'),
        bash_script
    )
