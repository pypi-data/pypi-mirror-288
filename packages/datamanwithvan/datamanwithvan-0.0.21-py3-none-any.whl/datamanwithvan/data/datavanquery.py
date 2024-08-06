import logging

from datamanwithvan.utils.statuscodes import StatusCodes

# Section 4 : Before anything else, set up the logger...
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
con_form = logging.Formatter(
    '%(asctime)s - %(name)s (%(levelname)s) : %(message)s')
console_handler.setFormatter(con_form)
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
# End of Section 4


class DatamanwithvanQuery:

    query_1 = ""
    StatusCodesObj = StatusCodes()

    def __init__(self):
        pass

    def get_query_1(self, param_1, param_2):
        query_1 = "{param_1} {param_2}"
        return query_1
