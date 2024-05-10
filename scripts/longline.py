import sys
sys.path.append('./')
from utils.argparsers.bashgenparser import BashGenArgParser
from utils.bash.generators import BashScriptGenerator


if __name__ == '__main__':
    parser = BashGenArgParser()
    args = parser.parse_args()
    bashgen = BashScriptGenerator(args)
    bash_script = bashgen.generate()
