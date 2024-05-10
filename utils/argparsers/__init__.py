import argparse
import logging

from utils.parse import parse_subjects_subset


class BaseArgParser:
    """
    A base class for creating argument parsers with argparse.

    This class provides a structured way to define and parse command-line arguments by encapsulating the creation and configuration of an `argparse.ArgumentParser` instance.

    Attributes:
        parser (argparse.ArgumentParser): The argument parser instance.

    Methods:
        add_argument(*args, **kwargs):
            Adds an argument to the parser. Accepts the same parameters as `argparse.ArgumentParser.add_argument`.

        parse_args():
            Parses the command line arguments passed to the script and returns an object containing the arguments and their values.

        setup():
            A method intended to be overridden in subclasses to define specific arguments. By default, it does nothing.
    """
    def __init__(self, description: str):
        """
        Initializes the BaseArgParser with a description for the argument parser.

        Args:
            description (str): A brief description of what the program does, which is displayed in the help message.
        """
        self.parser = argparse.ArgumentParser(description=description)
        self.setup()

    def add_argument(self, *args, **kwargs):
        """
        Adds an argument to the parser.

        This method is a wrapper around `argparse.ArgumentParser.add_argument`, allowing for arguments to be added directly to the `BaseArgParser` instance.

        Args:
            *args: Variable length argument list for positional arguments.
            **kwargs: Arbitrary keyword arguments for named arguments.
        """
        self.parser.add_argument(*args, **kwargs)

    def parse_args(self):
        """
        Parses the command line arguments.

        This method parses the arguments provided to the command line, using the configuration defined by calls to `add_argument`.

        Returns:
            argparse.Namespace: An object containing the parsed command line arguments. Each argument is accessible as an attribute of this object.
        """
        return self.parser.parse_args()

    def setup(self):
        """
        Sets up command line arguments for the parser.

        This method is intended to be overridden in subclasses to add arguments specific to the application. By default, it does nothing and should be implemented by subclasses.
        """
        pass