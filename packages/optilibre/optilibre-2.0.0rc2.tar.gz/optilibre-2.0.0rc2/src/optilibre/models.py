import logging
import optilibre.enums as enums
import optilibre.helpers as helpers
import toml
from pathlib import Path


class AudioCodec:
    def __init__(self, *args, **kwargs):
        self.enabled = kwargs.pop('enabled')
        if self.enabled:
            # so that pop doesn't throw a key error
            self.codec: enums.AudioCodecName = enums.AudioCodecName(kwargs.pop('codec'))

            self.__dict__.update(kwargs)

    def __getitem__(self, item):
        return self.__dict__[item]

class VideoCodec:
    def __init__(self, *args, **kwargs):
        self.enabled = kwargs.pop('enabled')
        if self.enabled:
            # so that pop doesn't throw a key error
            self.codec: enums.VideoCodecName = enums.VideoCodecName(kwargs.pop('codec'))

            self.__dict__.update(kwargs)

    def __getitem__(self, item):
        return self.__dict__[item]


class Folder:
    def __init__(self, name, *args, **kwargs):
        self.name: str = name
        self.enabled: bool = bool(kwargs.pop('enabled'))

        if self.enabled:
            self.version = kwargs.get('version', None)  #
            self.in_path: Path = Path(kwargs.pop('in_path'))
            self.out_path: Path = Path(kwargs.pop('out_path'))
            self.src_on_success: str = kwargs.get('src_on_success', 'keep')
            self.src_on_failure: str = kwargs.get('src_on_failure', 'keep')
            self.advanced_options: dict = kwargs.get('advanced_options', {})

            if self.src_on_success == 'move':
                self.src_on_success_dest: Path = Path(kwargs.pop('src_on_success_dest'))
            else:
                self.src_on_success_dest = None
            if self.src_on_failure == 'move':
                self.src_on_failure_dest: Path = Path(kwargs.pop('src_on_failure_dest'))
            else:
                self.src_on_failure_dest = None

            self.__dict__.update(kwargs)


class ImageFolder(Folder):
    def __init__(self, name, *args, **kwargs):
        # Import supplementary configuration if any was provided
        if 'config_file' in kwargs:
            with open(kwargs.pop('config_file'), 'r') as f:
                config = toml.load(f)
                kwargs = dict(kwargs, **config)

        # Create base class
        super().__init__(name, *args, **kwargs)
        if not self.enabled:
            return

        # Image specific content
        self.codec: enums.ImageCodecName = enums.ImageCodecName(kwargs.pop('codec'))

        if self.codec == enums.ImageCodecName.jpeg:
            logging.debug("Setting JPEG Options")
            self.jpeg_options = kwargs.get('jpeg', {})
        elif self.codec == enums.ImageCodecName.jpegxl:
            logging.debug("Setting JPEG XL Options")
            self.jpegxl_options = kwargs.get('jpegxl', {})

        # TODO Implement other codecs


    def get_codec_options(self):
        # returns self.<codec>_options
        return self.__getattribute__(f'{self.codec}_options')

class VideoFolder(Folder):
    def __init__(self, name, *args, **kwargs):
        # Import supplementary configuration if any was provided
        if 'config_file' in kwargs:
            with open(kwargs.pop('config_file'), 'r') as f:
                config = toml.load(f)
                kwargs = dict(kwargs, **config)

        # Create base class
        super().__init__(name, *args, **kwargs)
        if not self.enabled:
            return

        # Video specific content
        self.audio = AudioCodec(**kwargs.pop('audio'))
        self.video = VideoCodec(**kwargs.pop('video'))
        self.container_format: enums.VideoContainerName = enums.VideoContainerName(kwargs.pop('container_format'))


    def get_audio_codec_options(self):
        return self.audio[str(self.audio.codec)] if hasattr(self.audio, str(self.audio.codec)) else {}

    def get_video_codec_options(self):
        return self.video[str(self.video.codec)] if hasattr(self.video, str(self.video.codec)) else {}


class GlobalConfig:
    def __init__(self, *args, **kwargs):
        optilibre_kwargs = kwargs.pop('optilibre')
        self.version: str = optilibre_kwargs.pop('version')

        try:
            helpers.check_version(conf_version=self.version)
        except ValueError as e:
            logging.critical(e)
            logging.info("Exiting Optilibre due to previous error. Migrate the config file if needed.")
            exit(1)

        self.image_folders: list[ImageFolder] = []
        self.video_folders: list[VideoFolder] = []

        if 'convert' in kwargs:
            if 'image' in kwargs['convert']:
                folder_list = kwargs['convert']['image']

                for folder in folder_list:
                    self.image_folders.append(ImageFolder(name=folder, **kwargs['convert']['image'][folder]))

            if 'video' in kwargs['convert']:
                folder_list = kwargs['convert']['video']

                for folder in folder_list:
                    self.video_folders.append(VideoFolder(name=folder, **kwargs['convert']['video'][folder]))

        self.__dict__.update(kwargs)  # store extra vars
