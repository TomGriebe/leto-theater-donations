import obspython as obs  # type: ignore


def log_debug(message):
    obs.script_log(obs.LOG_DEBUG, "[DEBUG] " + str(message))


def log_info(message):
    obs.script_log(obs.LOG_INFO, "[INFO] " + str(message))


def log_warn(message):
    obs.script_log(obs.LOG_WARNING, "[WARN] " + str(message))


def log_error(message):
    obs.script_log(obs.LOG_ERROR, "[ERROR] " + str(message))
