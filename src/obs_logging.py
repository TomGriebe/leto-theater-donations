import obspython as obs  # type: ignore


def log_debug(message):
    obs.script_log(obs.LOG_DEBUG, message)


def log_info(message):
    obs.script_log(obs.LOG_INFO, message)


def log_warn(message):
    obs.script_log(obs.LOG_WARN, message)


def log_error(message):
    obs.script_log(obs.LOG_ERROR, message)
