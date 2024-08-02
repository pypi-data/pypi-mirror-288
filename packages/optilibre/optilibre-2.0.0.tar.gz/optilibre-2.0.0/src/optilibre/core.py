import logging
import os
import optilibre.helpers as helpers

from optilibre import models as models, enums as enums
from optilibre.helpers import path_exist, get_path_as_escaped_str
from pathlib import Path


def cmd_src_on_success_failure(folder: [models.VideoFolder, models.ImageFolder], subdir_relative: Path, status: 'success, failure') -> str:
    """
    Return shell cmd to execute on success or failure for the src file.
    :param subdir_relative:
    :param status: ['success', 'failure']
    :param folder:
    :return:
    """
    src_on_keyword = 'src_on_' + status
    src_on_keyword_dest = src_on_keyword + '_dest'

    on_success_failure = folder.__getattribute__(src_on_keyword)
    cmd_on_success_failure = ""
    if on_success_failure == 'keep':
        logging.debug(f"Keep src file on {status}.")
    elif on_success_failure == 'move':
        if not folder.__getattribute__(src_on_keyword_dest):
            logging.warning("%s was defined as 'move' but not %s was defined. Default back to 'keep'." %
                            (src_on_keyword, src_on_keyword_dest))

        dest = folder.__getattribute__(src_on_keyword_dest)
        if subdir_relative:
            dest = Path(os.path.join(dest, subdir_relative))
            helpers.ensure_folder_exists(dest)
        if not path_exist(dest):
            logging.warning("Default back to keep src file on %s" % status)
        else:
            cmd_on_success_failure = "mv {0} " + get_path_as_escaped_str(path=dest) + "/{1}"
            logging.debug("CMD on success or failure (move) {}".format(cmd_on_success_failure))
    elif on_success_failure == 'delete':
        cmd_on_success_failure = "rm {0}"

    return cmd_on_success_failure


def do_src_on_done(exit_code: int, file, folder: [models.VideoFolder, models.ImageFolder], subdir_relative: Path, log_prefix=None):
    """
    Launch shell cmd to execute on success or failure, to move, delete ... src file.
    :param subdir_relative: (if subdir) subdir where the file was located (relative to in_path)
    :param exit_code:
    :param file:
    :param folder:
    :param log_prefix: a string which will be added to the beginning of each log line
    :return:
    """

    if exit_code == 0:
        cmd = cmd_src_on_success_failure(folder=folder, subdir_relative=subdir_relative, status='success')
        logging.debug(f"{log_prefix}Exit code was successful.")
    else:
        cmd = cmd_src_on_success_failure(folder=folder, subdir_relative=subdir_relative, status='failure')
        logging.debug(f"{log_prefix}Exit code was not successful %s" % str(exit_code))

    cmd = cmd.format(get_path_as_escaped_str(path=file), get_path_as_escaped_str(path=os.path.basename(file)))
    logging.debug(f"{log_prefix}Execute post convert (empty if 'keep'): %s" % cmd)
    os.system(cmd)

    return None


def build_cmdline_video(folder: models.VideoFolder) -> str:
    """
    Build cmdline options
    :param folder:
    :return: cmdline (without in and out files)
    """

    # Set default options if not already set
    if "map_metadata" not in folder.advanced_options:
        folder.advanced_options['map_metadata'] = 0
    if "n" not in folder.advanced_options or "y" not in folder.advanced_options:
        folder.advanced_options['n'] = ''
    if folder.video.codec == enums.VideoCodecName.libx265 and "dst_range" not in folder.advanced_options:
        # enable full color range for x265 per default
        folder.advanced_options['dst_range'] = 1

    # Build cmdline
    cmdline_options = ""
    if folder.advanced_options:
        for opt in folder.advanced_options.items():
            cmdline_options += f" -{ opt[0] } { opt[1]}"

    cmdline_audio = ""
    if folder.audio.enabled:
        cmdline_audio = "-c:a " + str(folder.audio.codec)
        for opt in folder.audio[str(folder.audio.codec)].items():
            cmdline_audio += f" -{ opt[0] } { opt[1]}"

    cmdline_video = ""
    if folder.video.enabled:
        cmdline_video = "-c:v " + str(folder.video.codec)
        for opt in folder.video[str(folder.video.codec)].items():
            cmdline_video += f" -{ opt[0] } { opt[1]}"

    return "ffmpeg -i " + "'{}'" + cmdline_options + " " + cmdline_audio + " " + cmdline_video + " " + "'{}'"
