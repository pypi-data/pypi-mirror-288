import filetype
import logging
import os
import re
import optilibre
import optilibre.core
import optilibre.enums as enums
import optilibre.helpers as helpers
import optilibre.models as models
import optilibre.utils.parsers as parsers
from multiprocessing import Pool
from pathlib import Path
import subprocess

from optilibre.core import build_cmdline_video
import multiprocessing

def convert_img(file: Path, shell_cmdline: str, folder: models.ImageFolder, subdir_relative: Path, out_path: Path):
    current_process = multiprocessing.current_process()
    thread_name = current_process.name
    logging.debug(f"({thread_name}) Converting {str(file)}")

    # TODO move file extension / output
    logging.info(f'({thread_name}) {shell_cmdline}')
    result = subprocess.run(shell_cmdline, shell=True, capture_output=True, text=True)
    if not result.returncode == 0:
        logging.error(f"({thread_name}) Image conversion failed (exit code: {result.returncode}) with error:\n {result.stderr} ; {result.stdout}")
    else:
        logging.debug(f"({thread_name}) Image conversion ok.")

    # Supplementary checks
    if ', skipped.' in result.stdout:  # if a file is skipped, return code is 0
        # Jpegoptim skipped the file. Copy it to converted folder.
        logging.debug(f"({thread_name}) File skipped. Copying to converted folder.")
        move_cmd = ['cp', str(file), out_path]
        subprocess.run(move_cmd)

    optilibre.core.do_src_on_done(exit_code=result.returncode, file=file, folder=folder, subdir_relative=subdir_relative, log_prefix=f"({thread_name}) ")


def process_image_folder(folder: models.ImageFolder, subdir: Path = None):
    """
    This function recursively process an "optilibre" folder and its subdir.
    For each subdir encountered, call itself with subdir as arg.
    For the subdir in argument, create the subdir in the dest folders.
    """
    if not folder.enabled:
        logging.info(f"Folder {folder.name} is disabled. Skipping.")
        return

    in_path: Path = folder.in_path
    out_path: Path = folder.out_path

    subdir_msg = ""
    if subdir:
        subdir_msg = "(subdir: {})".format(subdir.relative_to(in_path))
    logging.info("Treating folder: {} {}".format(folder.name, subdir_msg))

    success_dest_path = folder.src_on_success_dest
    failure_dest_path = folder.src_on_failure_dest
    codec = folder.codec

    relative_subdir = None
    if subdir:
        # If we are working with a sub dir. Append it to out_path.
        relative_subdir = subdir.relative_to(in_path)  # for src_on_done
        out_path = out_path.joinpath(relative_subdir)  # get subdir from absolute path and join it with out_path
        in_path = subdir

    codec_options = folder.get_codec_options()

    # Set default options for JPEGoptim
    if codec == enums.ImageCodecName.jpeg:
        # Remove dest if provided (otherwise subdir won't work because of arg as reference)
        codec_options.get('d', None)
        codec_options.get('dest', None)
        #if "d" not in local_config[codec.name.lower()] and "dest" not in local_config[codec.name.lower()]:
        codec_options['d'] = helpers.get_path_as_escaped_str(out_path)

    # Build cmdline options
    cmdline_codec_opts = ""
    if folder.get_codec_options():
        for opt in folder.get_codec_options().items():
            cmdline_codec_opts += f" -{str(opt[0])} {str(opt[1])}"
    else:
        logging.debug("No config for %s found. Using default codec values." % codec.name)

    arg_list = []  # [(file1, shell1, local_config, subdir), (...)] we split arg_list to processes
    for file in Path(in_path).glob('*'):
        # Check if we're processing a in/out/success/failure dest.
        if file in [in_path, out_path, success_dest_path, failure_dest_path]:
            logging.debug("Ignoring in/out folder ({})".format(file))
            continue

        # FILE
        if file.is_file():
            kind = filetype.guess_mime(str(file))
            if bool(re.match("image/+", str(kind))):
                logging.debug("Building cmd line for: %s" % str(file))
                file_mime = filetype.guess_mime(str(file))

                if file.suffix not in optilibre.supported_img_ext or not bool(re.match('image/+', str(file_mime))):
                    # TODO Jpeg-XL can convert non jpeg format.
                    logging.warning("Filetype: %s not supported: for file: %s. Won't convert it." % (str(file_mime), str(file)))
                    # CONTINUE
                    continue

                # JPEG jpegoptim
                if codec == enums.ImageCodecName.jpeg:
                    encoder_cmdline = "jpegoptim"
                    out_file = ""

                # JPEG XL
                elif codec == enums.ImageCodecName.jpegxl:
                    # TODO implement recursive
                    encoder_cmdline = "cjxl"
                    out_file = os.path.join(out_path, os.path.splitext(os.path.basename(file))[0] + ".jxl")
                else:
                    logging.error("Codec type not supported %s" % str(codec))
                    # CONTINUE
                    continue

                shell_cmdline = "{encoder} {in_file} {options} {outfile}".format(
                    encoder=encoder_cmdline, in_file=helpers.get_path_as_escaped_str(file), options=cmdline_codec_opts, outfile=out_file)

                arg_list.append((file, shell_cmdline, folder, relative_subdir, out_path))
            else:
                # Changing suffix
                logging.debug("Filetype: %s for file: %s isn't an image file." % (str(kind), str(file)))

        # DIRECTORY
        elif file.is_dir():
            logging.debug("{} is a directory. Recursively entering it.".format(str(file)))
            process_image_folder(folder=folder, subdir=Path(file))
        else:
            logging.debug("{} is not a file neither a dir. Ignoring it.".format(str(file)))

    # multiprocess call
    if arg_list:
        helpers.ensure_folder_exists(path=out_path)  # only create folder if there is files to convert
        with Pool() as p:
            p.starmap(convert_img, arg_list)


def process_video_folder(folder: models.VideoFolder, subdir: Path = None):
    """
    This function recursively process an "optilibre" folder and its subdir.
    For each subdir encountered, call itself with subdir as arg.
    For the subdir in argument, create the subdir in the dest folders.
    """
    if not folder.enabled:
        logging.info(f"Folder {folder.name} is disabled. Skipping.")
        return

    in_path = folder.in_path

    subdir_msg = ""
    if subdir:
        subdir_msg = "(subdir: {})".format(subdir.relative_to(in_path))
    logging.info("Treating folder: {} {}".format(folder.name, subdir_msg))

    out_path = folder.out_path
    success_dest_path = folder.src_on_success_dest
    failure_dest_path = folder.src_on_failure_dest

    relative_subdir = None
    if subdir:
        # If we are working with a sub dir. Append it to out_path.
        relative_subdir = subdir.relative_to(in_path)  # for src_on_done
        out_path = out_path.joinpath(relative_subdir)  # get subdir from absolute path and join it with out_path
        in_path = subdir
        helpers.ensure_folder_exists(path=out_path)

    cmdline = build_cmdline_video(folder=folder)

    for file in Path(in_path).glob('*'):
        # Check if we're processing a in/out/success/failure dest.
        if file in [in_path, out_path, success_dest_path, failure_dest_path]:
            logging.debug("Ignoring in/out folder ({})".format(file))
            continue

        # FILE
        if file.is_file():
            kind = filetype.guess_mime(str(file))

            if bool(re.match("video/+", str(kind))):
                logging.debug("Processing " + str(file))

                if file.suffix in optilibre.supported_video_ext:
                    out_file = os.path.join(out_path, os.path.basename(
                        file.with_suffix('.' + str(folder.container_format))
                    ))

                    ffmpeg_cmdline = cmdline.format(file, out_file)

                    logging.info(ffmpeg_cmdline)
                    exit_code = os.WEXITSTATUS(os.system(ffmpeg_cmdline))
                    optilibre.core.do_src_on_done(exit_code=exit_code, file=file, folder=folder, subdir_relative=relative_subdir)

                else:
                    logging.info("Filetype {} for {} is not (yet) supported.".format(str(file.suffix), str(file)))
            else:
                # Changing suffix
                logging.debug("Filetype: %s for file: %s isn't a video file. Ignoring it." % (str(kind), str(file)))

        # DIRECTORY
        elif file.is_dir():
            logging.debug("{} is a directory. Recursively entering it.".format(str(file)))
            process_video_folder(folder=folder, subdir=Path(file))
        else:
            logging.debug("{} is not a file. Ignoring it.".format(str(file)))


def main(config_file):
    global_config = parsers.parse_config_file(config_file_path=config_file)

    logging.info("Processing image files.")
    image_folder: models.ImageFolder
    for image_folder in global_config.image_folders:
        process_image_folder(folder=image_folder)

    logging.info("Processing video files.")
    video_folder: models.VideoFolder
    for video_folder in global_config.video_folders:
        process_video_folder(folder=video_folder)

