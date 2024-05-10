import logging
from utils.argparsers import BaseArgParser
from utils.parse import parse_subjects_subset


class BashGenArgParser(BaseArgParser):
    """
    A specialized argument parser for automating the creation of bash scripts for preprocessing fMRI data.

    This class extends `BaseArgParser` to define command-line arguments specific to the generation of bash scripts for fMRI data preprocessing. It includes options for specifying subjects, sessions, project directory, and logging level.

    Methods:
        setup():
            Defines the command-line arguments specific to the bash script generation process.

        parse_args():
            Parses the command line arguments, sets up logging based on the specified log level, and processes the subject lists for inclusion and exclusion. It also hardcodes a field map dictionary for demonstration purposes.
    """
    def __init__(
        self,
        description='A tool for automating the creation of bash scripts tailored for preprocessing fMRI data.'
    ):
        """
        Initializes the BashGenArgParser with a default description.

        Args:
            description (str, optional): A brief description of the tool. Defaults to a predefined string explaining its purpose.
        """
        super().__init__(description)

    def setup(self):
        """
        Sets up command line arguments specific to the bash script generation.

        This method overrides the `setup` method of `BaseArgParser` to add arguments for specifying subjects, sessions to process, project directory, and logging level.
        """
        self.add_argument('subjects', metavar='SUBJECT', type=str, nargs='+',
                          help='subjects to include in the bash script (e.g. sub-01 sub-02 sub-03 or sub-01:03)')
        self.add_argument(
            '--exclude',
            dest='exclude',
            type=str,
            nargs='+',
            default=list(),
            help='list of subjects to exclude (e.g. sub-01 sub-02 sub-03 or sub-01:03)'
        )
        self.add_argument('--sessions', dest='sessions', type=str, nargs='+', default=['ses-01', 'ses-02'],
                          help='list of sessions to process (default: ses-01 ses-02)')
        self.add_argument('--project-dir', dest='project_dir', type=str, default='/data/pt_02703/fMRIprep',
                          help='project directory path (default: /data/pt_02703/fMRIprep)')
        self.add_argument(
            '--loglevel',
            dest='loglevel',
            type=str,
            default='info',
            help='Logging level to use. Can be info, debug, error or critical. Default is info.'
        )

    def parse_args(self):
        """
        Parses the command line arguments and configures logging.

        This method extends `parse_args` from `BaseArgParser` to include additional processing for the bash script generation tool. It sets up logging based on the specified log level, processes the subject lists for inclusion and exclusion, and hardcodes a field map dictionary for demonstration purposes.

        Returns:
            argparse.Namespace: An object containing the parsed command line arguments, with additional processing applied.
        """
        args = super().parse_args()
        logging.basicConfig(
            level={'info': logging.INFO, 'debug': logging.DEBUG, 'error': logging.ERROR, 'critical': logging.CRITICAL}[args.loglevel],
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        pattern = r'sub-\d{2}:\d{2}'
        subjects = parse_subjects_subset(args.subjects, pattern)
        excluded = parse_subjects_subset(args.exclude, pattern)

        subjects = list(set(subjects) - set(excluded))
        args.subjects = subjects
        # FIXME: it is hardcode
        args.fmap_dict = {
            '01': ['01','02','03'],
            '02': ['04','05','06'],
            '03': ['07','08','09','10']
        }
        return args