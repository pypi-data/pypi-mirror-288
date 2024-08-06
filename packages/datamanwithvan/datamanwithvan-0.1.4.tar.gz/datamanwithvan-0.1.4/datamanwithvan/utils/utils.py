import random
import string
import shutil
import logging

from datamanwithvan.utils.statuscodes import StatusCodes

# Section 65 : Before anything else, set up the logger...
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_format = logging.Formatter(
    '%(asctime)s - %(name)s (%(levelname)s) : %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)
try:
    file_handler = logging.FileHandler("/var/log/datamanwithvan/dmwv.log")
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s (%(levelname)s) : %(message)s')
    logger.addHandler(file_handler)
except Exception as e:
    print(f"Error while trying to open log file: {e}")
console_handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
# End of Section 65


class Utils:

    dummy_attribute = None
    StatusCodesObj = StatusCodes()

    def __init__(self):
        pass

    def has_enough_disk_space(self, path, size_in_bytes):
        """_summary_

        Args:
            path (_type_): _description_
            size_in_bytes (_type_): _description_

        Returns:
            _type_: _description_
        """
        status = self.StatusCodesObj.stat_code_generic

        if shutil.disk_usage(path) <= size_in_bytes:
            status = self.StatusCodesObj.stat_code_not_enough_disk_space
        else:
            status = self.StatusCodesObj.stat_code_enough_disk_space

        return status

    def select_random_element(self, from_array):
        """
        Select a random element from the given array.

        Parameters:
        array (list): The array from which to select a random element.

        Returns:
        element: A random element from the array.
        """
        if not from_array:
            return None
        return random.choice(from_array)

    def generate_random_string(self, length):
        """
        Generate a random string of specified length containing
        numbers and Latin characters.

        Parameters:
        - length (int): The length of the string to be generated.

        Returns:
        - str: A random string of specified length.
        """
        # Define the set of characters to choose from
        characters = string.ascii_letters + string.digits
        # Use random.choices to generate a list of characters
        # of the specified length
        random_string = ''.join(random.choices(characters, k=length))
        return random_string
