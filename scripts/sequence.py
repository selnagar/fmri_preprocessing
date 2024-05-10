import sys
sys.path.append('./')
from utils.argparsers.bashgenparser import BashGenArgParser
from utils.bash.generators import BashSequenceGenerator


if __name__ == '__main__':
    parser = BashGenArgParser()
    args = parser.parse_args()
    bashgen = BashSequenceGenerator(args)
    bash_script = bashgen.generate()
