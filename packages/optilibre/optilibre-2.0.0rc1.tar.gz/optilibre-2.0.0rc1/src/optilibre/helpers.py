import logging
import os
import shutil
import pathlib
import typing

from optilibre import supported_config_version_min


def ensure_folder_exists(path: pathlib.Path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except PermissionError:
        logging.exception("Can't create path {}. No Permission.".format(str(path)))



def get_escaped_path(path: typing.Union[str, pathlib.Path]) -> pathlib.Path:
    """
    Return a Path from provided path (it helps convert str with escape char (\\) to a valid Path)
    """
    if type(path) is str and '\\' in path:
        return pathlib.Path(path.replace('\\', ''))
    else:
        return pathlib.Path(path)


def get_path_as_escaped_str(path: pathlib.Path) -> str:
    return str(path).replace(" ", "\\ ")


def check_version(conf_version):
    if conf_version < supported_config_version_min:
        raise ValueError("Config version ({}) mismatched minimum supported version ({})".format(
            conf_version, supported_config_version_min
        ))
    else:
        logging.debug("Config file version ({}) is supported".format(conf_version))


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    return shutil.which(name) is not None


def path_exist(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        logging.error("Path (%s) doesn't exist or is not a directory." % path)
        # RETURN
        return False
    else:
        # RETURN
        return True

