import argparse
from glob import glob
import json
import logging
import os
from typing import Generator

from utils.bash import generate_bash_for_subject
from utils.fmaps import get_fmap_by_run_num
from utils.parse import find_in_string
from utils.path import join_or_make


class BashScriptGenerator:
    """
    A class for generating bash scripts for fMRI prepprocessing.
    """
    def __init__(self, args: argparse.Namespace):
        """
        Initializes the BashScriptGenerator object with project parameters.

        This method sets up the initial configuration for generating bash scripts
        based on the provided arguments. It initializes attributes related to
        subjects, sessions, project directory, and field map dictionary. It also prepares
        subject and session identifiers for use in script generation.

        Args:
            args (argparse.Namespace): Command line arguments containing subjects, sessions, project directory, and fmap dictionary.
            The expected properties of `args` include:
                - subjects (list): A list of subject identifiers.
                - sessions (list): A list of session identifiers.
                - project_dir (str): The root directory for the project.
                - fmap_dict (dict): A dictionary mapping functional runs to field maps.
        """
        self.subjects = args.subjects
        logging.info(f'subjects are: {self.subjects}')
        self.sessions = args.sessions
        self.project_dir = args.project_dir
        self.fmap_dict = args.fmap_dict
        self.sub2num = {
            subject: find_in_string(subject, r'sub-(\d+)')
            for subject in self.subjects
        }
        self.ses2num = {
            session: find_in_string(session, r'ses-(\d+)')
            for session in self.sessions
        }
        self._dirs_set = False
        self.kernel = '#! /bin/bash\n\n'

    def validate_dirs(self):
        """
        Validates the directory structure. If the directories are not set, it sets them up.
        """
        if not self._dirs_set:
            self.setup_dirs()
            self._dirs_set = True

    def setup_dirs(self):
        """
        Sets up the necessary directories for the project.

        This method creates and prepares the directory structure required for processing.
        It includes directories for BIDS data, code, derivatives, and working directories for fMRIPrep.
        It ensures that all necessary directories exist and are ready for use in subsequent steps of the script generation process.
        """
        self.dir_proj = self.project_dir
        logging.debug(f'Setting up directories in {self.dir_proj}...')
        self.dir_bids = join_or_make(self.dir_proj, 'data')
        self.dir_code = join_or_make(self.dir_proj, 'code', 'preprocessing', 'fmriprep')
        self.dir_deriv = join_or_make(self.dir_bids, 'derivatives')
        self.dir_work = join_or_make(self.dir_proj, 'fmriprep_work')

        self.sub_dir_work = {
            subject: os.path.join(
                self.dir_work,
                'fmriprep_wf',
                f'single_subject_{subject.split("-")[1]}_wf'
            )
            for subject in self.subjects
        }

        join_or_make(self.dir_deriv, 'fmriprep')
        join_or_make(self.dir_work, 'condor_log')
        logging.debug(f'Directories set up')

    def b0_field_source_to_json(self, subject: str):
        """
        Updates the B0 field source in the JSON files for a given subject.

        For each functional run of the specified subject, this method updates the JSON file to include the correct B0 field source information.
        This is necessary for correctly processing the MRI data with respect to field map correction.

        Args:
            subject (str): The name of the subject for which to update the B0 field source.
        """
        logging.info(f'Getting B0 field source for {subject}')
        sub_num = self.sub2num[subject]

        for session, ses_num in self.ses2num.items():
            logging.info(f'\tSession: {session}')
            dir_func = join_or_make(self.dir_bids, subject, session, 'func')
            func_jsons = glob(dir_func + '/*_bold.json')

            if len(func_jsons) == 0:
                raise OSError(f'No "*_bold.json" pattern in {dir_func}')

            logging.debug(f'func_jsons are: {func_jsons}')

            for func_json in func_jsons:
                run_num = find_in_string(func_json, r'run-(\d+)')
                fmap_num = get_fmap_by_run_num(run_num, self.fmap_dict)

                with open(func_json, 'r') as f:
                    data = json.load(f)

                data["B0FieldSource"] = f"pepolarfmap{sub_num}{ses_num}{fmap_num}"

                logging.debug(f'B0 field source is: {data["B0FieldSource"]}')

                with open(func_json, 'w') as f:
                    json.dump(data, f, indent=4)

    def b0_field_identifier_to_json(self, subject: str):
        """
        Updates the B0 field identifier in the JSON files for a given subject.

        Similar to `b0_field_source_to_json`, but for the B0 field identifier.
        This method updates each field map JSON file for the specified subject to include the correct B0 field identifier, facilitating the correct association between field maps and functional runs.

        Args:
            subject (str): The name of the subject for which to update the B0 field identifier.
        """
        logging.info(f'Getting B0 field identifier for {subject}')
        sub_num = self.sub2num[subject]

        for session, ses_num in self.ses2num.items():
            logging.info(f'\tSession: {session}')
            dir_fmap = join_or_make(self.dir_bids, subject, session, 'fmap')
            fmap_jsons = glob(dir_fmap + '/*_epi.json')

            if len(fmap_jsons) == 0:
                raise OSError(f'No "*_epi.json" pattern in {dir_fmap}')

            logging.debug(f'fmap_jsons are: {fmap_jsons}')

            for fmap_json in fmap_jsons:
                fmap_run_num = find_in_string(fmap_json, r'run-(\d+)')

                with open(fmap_json, 'r') as f:
                    data = json.load(f)

                data["B0FieldIdentifier"] = f"pepolarfmap{sub_num}{ses_num}{fmap_run_num}"

                logging.debug(f'B0 field identifier is: {data["B0FieldIdentifier"]}')

                with open(fmap_json, 'w') as f:
                    json.dump(data, f, indent=4)

    def generate_bash(self, subject: str) -> str:
        """
        Generates a bash script for a given subject.

        This method compiles the necessary commands into a bash script for processing a single subject's MRI data with fMRIPrep.
        It includes setting up the environment, running fMRIPrep with the correct parameters, and any additional processing steps required.

        Args:
            subject (str): The identifier of the subject for which to generate the bash script.

        Returns:
            str: The generated bash script as a string.
        """
        logging.debug(f'Generating bash for {subject}')
        return generate_bash_for_subject(
            subject,
            self.dir_bids,
            self.dir_deriv,
            self.dir_work,
            self.sub_dir_work[subject]
        )

    def __call__(self, subject: str) -> str:
        """
        Generates and returns the bash script for a given subject after setting up directories and updating JSON files.

        This method acts as a convenience function that wraps the directory setup, JSON file updating, and bash script generation into a single step for a given subject.

        Args:
            subject (str): The identifier of the subject for which to generate the bash script.

        Returns:
            str: The generated bash script as a string.
        """
        self.validate_dirs()
        self.b0_field_source_to_json(subject)
        self.b0_field_identifier_to_json(subject)

        return self.generate_bash(subject)

    def __iter__(self) -> Generator[str, None, None]:
        """
        Yields bash scripts for all subjects in the project.

        This method allows the BashScriptGenerator to be used in a for-loop, yielding the generated bash script for each subject in turn.
        It facilitates batch processing of all subjects in the project.

        Returns:
            Generator[str, None, None]: A generator that yields bash scripts as strings for each subject.
        """
        for subject in self.subjects:
            yield self(subject)

    def generate(self) -> str:
        """
        Generates and returns a concatenated string of all bash scripts for the project.

        This method compiles the bash scripts for all subjects into a single string, each script separated by the bash kernel.
        It is useful for creating a comprehensive script for batch processing.

        Returns:
            str: A string containing all generated bash scripts for the project, concatenated together.
        """
        return self.kernel + ''.join([bash_str for bash_str in self])


class BashSequenceGenerator(BashScriptGenerator):
    """
    A class for generating a sequence of bash scripts for fMRI preprocessing.
    """
    def generate(self) -> list[str]:
        """
        Generates and returns a list of bash scripts for the project, each prefixed with the bash kernel.

        Overrides the `generate` method of the BashScriptGenerator class to produce a list of individual bash scripts for each subject, rather than a single concatenated string.
        Each script in the list includes the bash kernel at the beginning.

        Returns:
            list[str]: A list of strings, each representing a bash script for a subject in the project.
        """
        return [self.kernel + bash_str for bash_str in self]