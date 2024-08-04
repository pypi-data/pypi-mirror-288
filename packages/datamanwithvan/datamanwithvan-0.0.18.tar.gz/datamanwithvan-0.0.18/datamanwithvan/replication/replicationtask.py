import logging

from datetime import datetime, timezone
from datamanwithvan.utils.statuscodes import StatusCodes
from datamanwithvan.utils.messages import DatamanwithvanMessages

# Section 4 : Before anything else, set up the logger...
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_format = logging.Formatter('%(name)s : %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)
# End of Section 4


class ReplicationTask:
    """_summary_

    Returns:
        _type_: _description_
    """
    StatusCodesObj = StatusCodes()
    verbosity = True
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
        # Section 85 : Set up the logger
        self.verbosity = verbosity
        if verbosity:
            console_handler.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
        # End of Section 85
        self.task_metadata["started"] = datetime.now(timezone.utc).timestamp()
        logger.info(replication_rule)
        logger.info(config)

    def _get_data_deltas(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return DatamanwithvanMessages.warn_not_implemented
