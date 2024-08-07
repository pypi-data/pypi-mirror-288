import os
import logging
import pkg_resources

from dynaconf import Dynaconf
from datamanwithvan.utils import messages
from datamanwithvan.utils import statuscodes

# Section 48 : Before anything else, set up the logger...
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
cons_frm = logging.Formatter(
    '%(asctime)s - %(name)s (%(levelname)s) : %(message)s')
console_handler.setFormatter(cons_frm)
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
# End of Section 48

package_name = "datamanwithvan"
version = pkg_resources.get_distribution(package_name).version


class datamanwithvanConfig:
    """_summary_

    Raises:
        lumache.InvalidKindError: _description_

    Returns:
        _type_: _description_
    """

    # Section 49 : Defaults
    general_samepeerreplications = False
    general_nativersync = True
    general_app_log_file = "/var/log/datamanwithvan/dmwv.log"
    general_job_log_store = "file"
    general_job_log_path = "/var/log/datamanwithvan/jobs/"
    datapeers = {}
    backenddatabase_dbtype = ""
    backenddatabase_server = ""
    backenddatabase_dbname = ""
    backenddatabase_port = 1433
    backenddatabase_schema = ""
    backenddatabase_uid = "***************"
    backenddatabase_region = "us-east-1"
    backenddatabase_pwd = "***************"
    backenddatabase_repl_rules_table = "dv_replicationrules"
    backenddatabase_log_table_prefix = "dv_replication_log_"
    # HINT: Define new config parameters here
    # End of section 49

    def __init__(self, config_file, runtime_params):
        """_summary_

        Args:
            config_file (_type_): _description_
        """
        ret = []

        if config_file:
            ret = self._load_config_from_file(config_file)
            if ret[0] != statuscodes.StatusCodes.conf_loading_success:
                logger.error(f"Failed to load {config_file} ({ret[0]})"
                             ". Proceeding with defaults...")
                self._config_loading_sequence(dmConf=None,
                                              runtime_params=runtime_params)
            else:
                logger.info(f"Loaded {config_file} successfully")
                self._config_loading_sequence(dmConf=ret[1],
                                              runtime_params=runtime_params)
        else:
            logger.debug("No config file given. Proceed with defaults...")
            self._config_loading_sequence(dmConf=None,
                                          runtime_params=runtime_params)

    def _load_config_from_file(self, config_file):
        """
        Return a list of random ingredients as strings.

        :param kind: Optional "kind" of ingredients.
        :type kind: list[str] or None
        :raise lumache.InvalidKindError: If the kind is invalid.
        :return: The ingredients list.
        :rtype: list[str]

        """
        status = 0
        dmConf = None
        settings_dict = []

        if config_file:
            # It's stupid, did it to shorten the line for linting
            _msg = messages.DatamanwithvanMessages.msg_info_load_conf
            msg = f"{_msg} {config_file}"
            logger.info(msg)

            if os.access(config_file, os.R_OK):
                # TODO: Read the config file, load it...
                try:
                    dmConf = Dynaconf(settings_files=[config_file],
                                      environments=False)
                    status = statuscodes.StatusCodes.conf_loading_success
                    settings_dict = dmConf.as_dict()
                    logger.info(f"Serialized dmConf is: {settings_dict}")
                except Exception as configFileNotFound:
                    logger.error(f"Can't load {config_file}:"
                                 f" {configFileNotFound}")
                    status = statuscodes.StatusCodes.status_cnf_not_load
            else:
                logger.error(f"Can't load {config_file}: File does not exist")
                status = statuscodes.StatusCodes.stat_code_cnf_not_exist
        else:
            logger.error("No Datamanwithvan config file was specified..")
            status = statuscodes.StatusCodes.stat_code_conf_not_provided

        return [status, settings_dict]

    def _config_loading_sequence(self, dmConf=None, runtime_params=None):
        """_summary_

        Args:
            dmConf (_type_, optional): _description_. Defaults to None.
        """
        for conf_name, conf_value in self.__dict__.items():
            # Order of precedence:
            # 1. Environmental variables
            # 2. Runtime parameters
            # 3. Config file parameters
            # 4. Default values
            # That being said, (3) is processed first,
            # (2) is processed second and (1) is
            # processed last.
            if dmConf:
                for param_sect in dmConf:
                    for parameters in dmConf[param_sect]:
                        if not isinstance(parameters, dict):
                            setattr(
                                self,
                                f"{param_sect.lower()}_{parameters}",
                                dmConf[param_sect][parameters])
                        if isinstance(parameters, dict):
                            self.datapeers[param_sect.lower()] = parameters

            if runtime_params:
                for rt_params in runtime_params:
                    if not isinstance(runtime_params[rt_params], dict):
                        setattr(
                            self,
                            f"{rt_params.lower()}",
                            runtime_params[rt_params])
                    if isinstance(runtime_params[rt_params], dict):
                        self.datapeers[rt_params] = runtime_params[rt_params]

            if os.getenv(f"DMWV_{conf_name.upper()}"):
                setattr(self,
                        conf_name,
                        os.getenv(f"DMWV_{conf_name.upper()}"))
