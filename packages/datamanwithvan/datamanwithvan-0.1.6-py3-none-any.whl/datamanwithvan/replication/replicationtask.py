import logging

from datetime import datetime, timezone
from datamanwithvan.utils.statuscodes import StatusCodes

# Section 24 : Before anything else, set up the logger...
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
# End of Section 24


class ReplicationTask:
    """_summary_

    Returns:
        _type_: _description_
    """
    StatusCodesObj = StatusCodes()
    verbosity = True
    config = ""
    replication_item = {
        "status": None,
        "origin_path": "",
        "targeet_path": "",
        "started": "",
        "finished": "",
        "size_bytes": 0,
        "comments": ""
    }
    task_metadata = {
        "repl_rule_id": None,
        "status": None,
        "started": "",
        "finished": "",
        "items": [],          # This array contains replication_item items
        "origin_agent": "",
        "target_agent": "",
        "comments": ""
    }

    def __init__(self, replication_rule, config, verbosity=True) -> None:
        """_summary_

        Args:
            replication_rule (_type_): _description_
            config (_type_): _description_
            verbosity (bool, optional): _description_. Defaults to True.
        """
        # Section 86 : Set up the logger
        file_handler = logging.FileHandler(config.general_app_log_file)
        file_frm = logging.Formatter(
            '%(asctime)s - %(name)s (%(levelname)s) : %(message)s')
        file_handler.setFormatter(file_frm)
        logger.addHandler(file_handler)
        self.verbosity = verbosity
        if verbosity:
            console_handler.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
        # End of Section 86
        self.task_metadata["started"] = datetime.now(timezone.utc).timestamp()
        logger.info(replication_rule)
        logger.info(config)
        self.config = config

    def _get_data_deltas(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        deltas = {}

        logger.info("Not implemented: delta evaluation")

        return deltas

    def run_task(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        # TODO: Elect 1 random origin agent

        # TODO: Elect 1 random target agent

        deltas = self._get_data_deltas()

        # TODO: For each delta item, make a replication item
        # and transfer it

        logger.info(deltas)

        return self.task_metadata
