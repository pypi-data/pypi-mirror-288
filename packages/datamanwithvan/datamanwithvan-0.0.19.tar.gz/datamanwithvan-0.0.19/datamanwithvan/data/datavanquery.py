import logging

from datamanwithvan.utils.statuscodes import StatusCodes

# Section 4 : Before anything else, set up the logger...
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_format = logging.Formatter('%(name)s : %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)
# End of Section 4


class DatamanwithvanQuery:

    query_1 = ""
    StatusCodesObj = StatusCodes()

    def __init__(self):
        pass

    def get_query_1(self, param_1, param_2):
        query_1 = "{param_1} {param_2}"
        return query_1
