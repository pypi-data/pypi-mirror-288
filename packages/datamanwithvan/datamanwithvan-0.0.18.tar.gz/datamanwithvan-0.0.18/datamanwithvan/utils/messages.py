import pkg_resources


class DatamanwithvanMessages:
    pkgname = "datamanwithvan"
    msg_info_version_number = pkg_resources.get_distribution(pkgname).version
    msg_info_welcome = r"""
    ___      _                          __    __ _ _   _                   __
   /   \__ _| |_ __ _  /\/\   __ _ _ __/ / /\ \ (_| |_| |____   ____ _  /\ \ \
  / /\ / _` | __/ _` |/    \ / _` | '_ \ \/  \/ | | __| '_ \ \ / / _` |/  \/ /
 / /_/| (_| | || (_| / /\/\ | (_| | | | \  /\  /| | |_| | | \ V | (_| / /\  /
/___,' \__,_|\__\__,_\/    \/\__,_|_| |_|\/  \/ |_|\__|_| |_|\_/ \__,_\_\ \/
"""
    msg_info_welcome_footer = "Yet another data replication tool!"
    msg_info_repl_rule_exist = "All good, rest not implemented yet"
    msg_info_load_conf = "Loading configuration from file"
    msg_error_cant_fetch_rep_rule = "Unable to fetch replication rules"
    msg_error_no_conf = "Unable to find a usable configuration. Exiting now.."
    msg_error_no_cnf_pro = "No Datamanwithvan config file was specified..."
    msg_warn_no_rep_rule = "This job has no active rules to run"
    warn_not_implemented = "Not implemented yet"
    err_fn_no_found = "Function not found"
    err_no_quiet_and_verbose = "Quiet & verbose params can't be set together"

    def __init__(self):
        pass
