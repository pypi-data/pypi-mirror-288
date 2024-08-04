import dask
import dask.threaded
import logging

from dask import delayed
from datamanwithvan.utils import messages
from datamanwithvan.utils.statuscodes import StatusCodes
from datamanwithvan.replication import replicationtask

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
con_form = logging.Formatter('%(name)s : %(levelname)s - %(message)s')
console_handler.setFormatter(con_form)
logger.addHandler(console_handler)


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

    def _transfer_data(self, replication_rule):
        status = messages.DatamanwithvanMessages.warn_not_implemented
        return status

    def _initiate_replication_tasks(self, replication_rule):
        logger.debug(replication_rule)

        repTaskObj = replicationtask.ReplicationTask(replication_rule,
                                                     self.configuration,
                                                     self.verbosity)
        logger.info(repTaskObj.task_metadata)
        self._transfer_data(replication_rule)

    def start_replication_tasks(self):
        results = dask.compute(*self.tasks, scheduler='threads')

        logger.debug(results)

        return results

    def assign_replication_rules(self):
        """
        For every replication rule in the job, make a separate thread
        to handle it
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
