import urllib
import dask
import dask.threaded
import logging

from dask import delayed
from sqlalchemy import create_engine, text
from datamanwithvan.config.config import datamanwithvanConfig
from datamanwithvan.utils import messages
from datamanwithvan.utils.statuscodes import StatusCodes
from datamanwithvan.replication import replicationtask

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
con_frmt = logging.Formatter(
    '%(asctime)s - %(name)s (%(levelname)s) : %(message)s')
console_handler.setFormatter(con_frmt)
logger.addHandler(console_handler)
try:
    # TODO: How to get a default path from somewhere?
    file_handler = logging.FileHandler("/var/log/datamanwithvan/dmwv.log")
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s (%(levelname)s) : %(message)s')
    logger.addHandler(file_handler)
except Exception as e:
    print(f"Error while trying to open log file: {e}")
console_handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)


class ReplicationJob:
    """_summary_

    Returns:
        _type_: _description_
    """

    replication_job_id = None
    configuration = datamanwithvanConfig(config_file=None, runtime_params=None)
    content = None
    query_engine = None
    StatusCodesObj = StatusCodes()
    verbosity = True
    tasks = []

    def __init__(self, replication_job_id, configuration, verbosity):
        """_summary_

        Args:
            replication_job_id (_type_): _description_
            configuration (_type_): _description_
            verbosity (_type_): _description_
        """
        self.replication_job_id = replication_job_id
        self.configuration = configuration
        self.content = messages.DatamanwithvanMessages()
        self.query_engine = self._getQueryEngine()
        # Section 84 : Set up the logger
        self.verbosity = verbosity
        if verbosity:
            console_handler.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
        # End of Section 84

    def start_replication_tasks(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        results = dask.compute(*self.tasks, scheduler='threads')

        logger.debug(results)

        return results

    def _initiate_replication_tasks(self,
                                    configuration,
                                    verbosity,
                                    replication_rule):
        """_summary_

        Args:
            replication_rule (_type_): _description_
        """
        logger.info(replication_rule)
        repTaskObj = replicationtask.ReplicationTask(replication_rule,
                                                     configuration,
                                                     verbosity)
        task_metadata = repTaskObj.run_task()
        logger.info(task_metadata)

    def assign_replication_rules(self, replication_rules):
        """
        For every replication rule in the job, make a separate thread
        to handle it - dummy change 2
        """
        status = None
        try:
            num_tasks = len(replication_rules[1].fetchall())
            self.tasks = [delayed(self._initiate_replication_tasks)(
                replication_rules[1][i]) for i in range(0, num_tasks - 1)]
            status = 35
        except Exception as e:
            logger.error(f" failed to make replication tasks: {e}")
            status = 36

        return status

    def _checkin_replication_job(self, replication_job_id):
        """This function registers that a job with id replication_job_id
        has just started. If there's a backend DB set, it will

        Args:
            replication_job_id (int): The ID of the job to run

        Returns:
            dict: A dictionary containing the operation name, the status
            and any other useful, textual comments
        """
        from datetime import datetime, timezone

        result = {
            "operation": "_checkin_replication_job",
            "status": "STARTED",
            "checkin_time": datetime.now(timezone.utc).timestamp(),
            "comments": messages.DatamanwithvanMessages.warn_not_implemented
        }

        query_engine = self._getQueryEngine()
        logger.info(query_engine)

        return result

    def _checkout_replication_job(self, jobMetadata):
        """_summary_

        Args:
            jobMetadata (_type_): _description_

        Returns:
            _type_: _description_
        """

        logger.info(messages.DatamanwithvanMessages.warn_not_implemented)

        return messages.DatamanwithvanMessages.warn_not_implemented

    def _getQueryEng_mysql(self, configuration):
        return messages.DatamanwithvanMessages.warn_not_implemented

    # TODO: Uncomment and implement this method
    def _getQueryEng_cosmosdb(self, configuration):
        return messages.DatamanwithvanMessages.warn_not_implemented

    # TODO: Uncomment and implement this method
    def _getQueryEng_dynamodb(self, configuration):
        engine = ""

        return engine

    # TODO: Implement this method
    def _getQueryEng_postgresql(self, configuration):
        return messages.DatamanwithvanMessages.warn_not_implemented

    def _getQueryEng_azuresql(self, configuration):
        """_summary_

        Args:
            configuration (_type_): _description_

        Returns:
            _type_: _description_
        """
        server = configuration.backenddatabase_server
        database = configuration.backenddatabase_dbname
        uid = configuration.backenddatabase_uid
        pwd = configuration.backenddatabase_pwd

        # credential = DefaultAzureCredential()
        # token = credential.get_token(
        # "https://database.windows.net/.default").token

        # Construct connection string
        connection_string = (
            f"Driver={{ODBC Driver 18 for SQL Server}};"
            f"Server={server};"
            f"Database={database};"
            f"Uid={uid};"
            f"Pwd={pwd};"
            f"Encrypt=yes;"                # Ensure encryption
            f"TrustServerCertificate=no;"
        )

        # Encode the connection string for SQLAlchemyy
        params = urllib.parse.quote_plus(connection_string)
        engine_url = f"mssql+pyodbc:///?odbc_connect={params}"

        # Create SQLAlchemy engine
        engine = create_engine(engine_url)

        return engine

    def _getQueryEngine(self):
        """
        Returns an SQLAlchemy's QueryEngine Object.

        Parameters:
        - configuration (datamanwithvanConfig): The object containing
        Datamanwithvan's master configuration

        Returns:
        - Engine: A class `_engine.Engine` instance.
        """
        funcname = f"_getQueryEng_{self.configuration.backenddatabase_dbtype}"
        func = getattr(self,
                       funcname,
                       None)
        if callable(func):
            return func(self.configuration)
        else:
            logger.error(messages.DatamanwithvanMessages.err_fn_no_found)

    def _getReplicationRules(self, replication_job_id, query_engine):
        """_summary_

        Args:
            replication_job_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        result = []
        status = self.StatusCodesObj.stat_code_generic
        rules = []

        try:
            with query_engine.connect() as connection:
                sch = self.configuration.backenddatabase_schema
                tbl = self.configuration.backenddatabase_repl_rules_table
                query = f"""SELECT *
                from {sch}.{tbl}
                where id={replication_job_id} and enabled=1"""

                rules = connection.execute(text(query))

                if len(rules.fetchall()) == 0:
                    status = 1
                else:
                    status = 0

        except Exception as e:
            logger.error(f"Could not fetch replication rules"
                         f"for Job ({replication_job_id}) : {e}")
            status = 2

        result = [status, rules]

        return result

    def run_job(self, replication_job_id):
        """_summary_

        Args:
            replication_job_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        jobMetadata = {
            "status": -1,
            "operations": []
        }

        logger.info(f"Starting replication job {replication_job_id}")

        # runjob step 1: Check-in the new job
        x = self._checkin_replication_job(replication_job_id)
        jobMetadata["operations"].append(x)
        # end of runjob step 1

        # runjob step 2: Get Replication Rules
        replication_rules = self._getReplicationRules(
            replication_job_id, self.query_engine)
        logger.info(replication_rules)
        # end of runjob step 2

        # runjob step 3: Validate the Replication Rules
        if replication_rules[0] == 0:
            logger.info(
                messages.DatamanwithvanMessages.msg_info_repl_rule_exist)
        if replication_rules[0] == 1:
            logger.warning(
                messages.DatamanwithvanMessages.msg_warn_no_rep_rule)
            return replication_rules[0]
        if replication_rules[0] == 2:
            mg = messages.DatamanwithvanMessages.msg_error_cant_fetch_rep_rule
            logger.error(mg)
            return replication_rules[0]
        # end of runjob step 3

        # runjob step 4: Assign the rules of the replication job
        # to individual threads/tasks
        x = replication_rules[1]
        result_assign_rules = self.assign_replication_rules(x)
        logger.info(result_assign_rules)
        # end of runjob step 4

        # runjob step 5: Kick off the replication tasks
        result_start_tasks = self.start_replication_tasks()
        logger.debug(result_start_tasks)
        # end of runjob step 5

        # runjob step 6: At this point, the replication has completed.
        # Time to checkout and return all the metadata it gathered.
        self._checkout_replication_job(jobMetadata)
        # end of runjob step 6

        logger.info(jobMetadata)
        return jobMetadata
