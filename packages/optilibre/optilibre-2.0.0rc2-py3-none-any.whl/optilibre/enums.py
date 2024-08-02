from enum import Enum


class ImageCodecName(Enum):
    jpeg = "jpeg"
    jpegxl = "jpegxl"

    def __str__(self):
        return self.value

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__


class AudioCodecName(Enum):
    aac = "aac"
    ogg = "ogg"

    def __str__(self):
        return self.value

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__


class VideoCodecName(Enum):
    libx264 = "libx264"
    libx265 = "libx265"

    def __str__(self):
        return self.value

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__


class VideoContainerName(Enum):
    avi = "avi"
    mkv = "mkv"
    mp4 = "mp4"

    def __str__(self):
        return self.value

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__
