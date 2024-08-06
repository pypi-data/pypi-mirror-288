import logging

# Section 64 : Before anything else, set up the logger...
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
# End of Section 64


class StatusCodes:
    """_summary_
    """
    stat_code_generic = 0
    stat_code_not_enough_disk_space = 1
    stat_code_enough_disk_space = 2
    conf_loading_success = 3
    status_cnf_not_load = 4
    stat_code_cnf_not_exist = 5
    stat_code_conf_not_provided = 6
    stat_code_quiet_verbose = 7

    def __init__(self):
        """_summary_
        """
        pass
