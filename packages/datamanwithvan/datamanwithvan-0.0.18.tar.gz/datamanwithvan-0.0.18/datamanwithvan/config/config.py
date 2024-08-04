# config/config.py
# Keeping it here for reference purposes, since we're using
# Dynaconf to load the configuration inside the main script.
import os
import logging
import pkg_resources

from dynaconf import Dynaconf
from datamanwithvan.utils import messages
from datamanwithvan.utils import statuscodes


class datamanwithvanConfig:

    dmConf = None
    path_to_config = None
    # Section 48 : Before anything else, set up the logger...
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    cons_frm = logging.Formatter('%(name)s : %(levelname)s - %(message)s')
    console_handler.setFormatter(cons_frm)
    logger.addHandler(console_handler)
    # End of Section 48
    status = statuscodes.StatusCodes.stat_code_generic
    package_name = "datamanwithvan"
    version = pkg_resources.get_distribution(package_name).version
    # Section 49 : Defaults
    app_file_log = "/var/log/datamanwithvan/dmwv.log"
    # End of section 49

    def _load_config_from_file(self, args_config):
        """
        Return a list of random ingredients as strings.

        :param kind: Optional "kind" of ingredients.
        :type kind: list[str] or None
        :raise lumache.InvalidKindError: If the kind is invalid.
        :return: The ingredients list.
        :rtype: list[str]

        """
        if args_config:
            # It's stupid, did it to shorten the line for linting
            _msg = messages.DatamanwithvanMessages.msg_info_load_conf
            msg = f"{_msg} {args_config}"
            self.logger.info(msg)

            if os.access(args_config, os.R_OK):
                # TODO: Read the config file, load it...
                try:
                    self.dmConf = Dynaconf(
                        settings_files=[args_config],
                        environments=False
                    )
                    self.status = statuscodes.StatusCodes.conf_loading_success
                    settings_dict = self.dmConf.to_dict()
                    self.logger.debug(settings_dict)
                except Exception as configFileNotFound:
                    self.logger.error(f"Can't load {args_config}:"
                                      f"{configFileNotFound}")
                    self.status = statuscodes.StatusCodes.status_cnf_not_load
            else:
                self.logger.error(f"Can't load {args_config}: "
                                  "File does not exist")
                self.status = statuscodes.StatusCodes.stat_code_cnf_not_exist
        else:
            self.logger.error("No Datamanwithvan config file was specified..")
            self.status = statuscodes.StatusCodes.stat_code_conf_not_provided

        return self.status

    def set_config_file(self, args_config):
        return self._load_config_from_file(args_config)

    def __init__(self):
        pass
