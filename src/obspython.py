OBS_TEXT_DEFAULT = "default"
OBS_TEXT_PASSWORD = "password"

LOG_DEBUG = "debug"
LOG_INFO = "info"
LOG_WARNING = "warning"
LOG_ERROR = "error"


def script_log(level, message):
    print(message)


def obs_properties_create(props, name, title, variant):
    return {}


def obs_properties_add_text(props, name, title, callback):
    return


def obs_properties_add_button(source):
    return


def obs_get_source_by_name(name):
    return name


def obs_source_release(source):
    return


def obs_source_get_settings(source):
    return {}


def obs_source_get_signal_handler(source):
    return {}


def signal_handler_connect(handler, signal, callback):
    return


def obs_source_media_stop(source):
    return


def obs_source_media_restart(source):
    return


def obs_data_set_bool(settings, name, value):
    return


def obs_data_get_string(settings, name):
    return name


def obs_source_update(source, settings):
    return


def timer_add(callback, interval):
    return


def timer_remove(callback):
    return
