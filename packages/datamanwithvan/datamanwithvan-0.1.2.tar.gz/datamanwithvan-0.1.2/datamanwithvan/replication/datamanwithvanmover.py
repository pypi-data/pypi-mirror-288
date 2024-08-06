import dask
import dask.threaded
import logging

from dask import delayed
from datamanwithvan.utils.statuscodes import StatusCodes
from datamanwithvan.replication import replicationtask

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


class dmwvMover:
    replication_rules = []
    configuration = None
    verbosity = True
    StatusCodesObj = StatusCodes()

    def __init__(self, replication_rules, configuration, verbosity=True):
        self.replication_rules = replication_rules
        self.configuration = configuration
        # Section 85 : Set up the logger
        self.verbosity = verbosity
        if verbosity:
            console_handler.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
        # End of Section 85

    def _initiate_replication_tasks(self, replication_rule):
        """_summary_

        Args:
            replication_rule (_type_): _description_
        """
        logger.info(replication_rule)
        repTaskObj = replicationtask.ReplicationTask(replication_rule,
                                                     self.configuration,
                                                     self.verbosity)
        task_metadata = repTaskObj.run_task()
        logger.info(task_metadata)

    def start_replication_tasks(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        results = dask.compute(*self.tasks, scheduler='threads')

        logger.debug(results)

        return results

    def assign_replication_rules(self):
        """
        For every replication rule in the job, make a separate thread
        to handle it - dummy change 2
        """
        status = None
        try:
            num_tasks = len(self.replication_rules[1].fetchall())
            self.tasks = [delayed(self._initiate_replication_tasks)(
                self.replication_rules[1][i]) for i in range(0, num_tasks - 1)]
            status = 35
        except Exception as e:
            logger.error(f" failed to make replication tasks: {e}")
            status = 36

        return status
