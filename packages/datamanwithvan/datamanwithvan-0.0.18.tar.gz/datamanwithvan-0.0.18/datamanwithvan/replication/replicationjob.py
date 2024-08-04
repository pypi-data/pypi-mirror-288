import urllib
import logging

from sqlalchemy import create_engine, text
from datamanwithvan.config.config import datamanwithvanConfig
from datamanwithvan.utils import messages
from datamanwithvan.replication import datamanwithvanmover
from datamanwithvan.utils.statuscodes import StatusCodes


class ReplicationJob:

    replication_job_id = None
    configuration = datamanwithvanConfig()
    content = None
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    con_frmt = logging.Formatter('%(name)s : %(levelname)s - %(message)s')
    console_handler.setFormatter(con_frmt)
    logger.addHandler(console_handler)
    query_engine = None
    StatusCodesObj = StatusCodes()
    verbosity = True

    def __init__(self, replication_job_id, configuration, verbosity):
        self.replication_job_id = replication_job_id
        self.configuration = configuration
        self.content = messages.DatamanwithvanMessages()
        self.query_engine = self._getQueryEngine()
        # Section 85 : Set up the logger
        self.verbosity = verbosity
        if verbosity:
            self.console_handler.setLevel(logging.DEBUG)
            self.logger.setLevel(logging.DEBUG)
        # End of Section 85

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
        self.logger.info(query_engine)

        return result

    def _checkout_replication_job(self, jobMetadata):
        """_summary_

        Args:
            jobMetadata (_type_): _description_

        Returns:
            _type_: _description_
        """

        self.logger.info(messages.DatamanwithvanMessages.warn_not_implemented)

        return messages.DatamanwithvanMessages.warn_not_implemented

    # TODO: Uncomment and implement this method
    def _getQueryEng_mysql(self, configuration):
        return messages.DatamanwithvanMessages.warn_not_implemented

    # TODO: Uncomment and implement this method
    def _getQueryEng_cosmosdb(self, configuration):
        return messages.DatamanwithvanMessages.warn_not_implemented

    # TODO: Uncomment and implement this method
    def _getQueryEng_dynamodb(self, configuration):
        return messages.DatamanwithvanMessages.warn_not_implemented

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
        server = configuration.backenddatabase.server
        database = configuration.backenddatabase.database
        uid = configuration.backenddatabase.uid
        pwd = configuration.backenddatabase.pwd

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

        # Encode the connection string for SQLAlchemy
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
        funcname = f"_getQueryEng_{self.configuration.backenddatabase.dbtype}"
        func = getattr(self,
                       funcname,
                       None)
        if callable(func):
            return func(self.configuration)
        else:
            self.logger.error(messages.DatamanwithvanMessages.err_fn_no_found)

    def _getReplicationRules(self, replication_job_id, query_engine):
        """
        """
        result = []
        status = self.StatusCodesObj.stat_code_generic
        rules = []

        try:
            with query_engine.connect() as connection:
                sch = self.configuration.backenddatabase.schema
                tbl = self.configuration.backenddatabase.repl_rules_table
                query = f"""SELECT *
                from {sch}.{tbl}
                where id={replication_job_id} and enabled=1"""

                rules = connection.execute(text(query))

                if len(rules.fetchall()) == 0:
                    status = 1
                else:
                    status = 0

        except Exception as e:
            self.logger.error(f"Could not fetch replication rules"
                              f"for Job ({replication_job_id}) : {e}")
            status = 2

        result = [status, rules]

        return result

    def runjob(self, replication_job_id):
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

        self.logger.info(f"Starting replication job {replication_job_id}")

        # runjob step 1: Check-in the new job
        x = self._checkin_replication_job(replication_job_id)
        jobMetadata["operations"].append(x)
        # end of runjob step 1

        # runjob step 2: Get Replication Rules
        replication_rules = self._getReplicationRules(
            replication_job_id, self.query_engine)
        self.logger.info(replication_rules)
        # end of runjob step 2

        # runjob step 3: Validate the Replication Rules
        if replication_rules[0] == 0:
            self.logger.info(
                messages.DatamanwithvanMessages.msg_info_repl_rule_exist)
        if replication_rules[0] == 1:
            self.logger.warning(
                messages.DatamanwithvanMessages.msg_warn_no_rep_rule)
            return replication_rules[0]
        if replication_rules[0] == 2:
            mg = messages.DatamanwithvanMessages.msg_error_cant_fetch_rep_rule
            self.logger.error(mg)
            return replication_rules[0]
        # end of runjob step 3

        # runjob step 4: What's next?
        # TODO: we create a dmwvMover
        # object that will do the heavy work
        x = replication_rules
        y = self.configuration
        z = self.verbosity
        dmwvMoverObj = datamanwithvanmover.dmwvMover(x, y, z)
        result_assign_rules = dmwvMoverObj.assign_replication_rules()
        self.logger.info(result_assign_rules)

        result_start_tasks = dmwvMoverObj.start_replication_tasks()
        self.logger.info(result_start_tasks)
        self.logger.debug(dmwvMoverObj)
        # end of runjob step 4

        # runjob step 5: What's next?
        self._checkout_replication_job(jobMetadata)
        # end of runjob step 5

        self.logger.info(jobMetadata)
        return jobMetadata
