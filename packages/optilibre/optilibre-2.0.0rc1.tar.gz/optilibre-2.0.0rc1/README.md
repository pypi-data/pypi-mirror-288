# Optilibre

Optilibre is a simple python program to automatically optimize video and images files using ffmpeg
and other image optimizers.
See _Supported formats_ to have a list of supported file format you can convert to/from.

Official repo : [https://gitlab.com/daufinsyd/optilibre](https://gitlab.com/daufinsyd/optilibre)

## Installation

Simply install it using pip:
```
pip3 install optilibre
```

## Usage
Copy the **optilibre.example.conf** to **optilibre.conf** and change the values according to your need.

```
optilibre optimize --config /path/to/opilibre.conf
```

You can find a systemd service and timer in systemd folder, which you can copy to /etc/systemd/system/ . 

## Requirements

See _Supported formats_ .

## Configuration

Copy and edit **optilibre.example.conf** to **optilibre.conf** .
For each folder you want to process, create a new entry as shown in the example file.

You can put the configuration of a section in another **optilibre.toml** configuration file (see **optiimage.example.toml** and **optivideo.example.toml** for an example) by referencing it in **optilibre.conf**.

### Video
- The directive [optivideo] configure the video encoder.
- The directive [optivideo.meta] defines which meta args should ffmpeg use.
- The directive [optivideo.audio] defines which codec should ffmpeg use to audio.
- The directive [optivideo.video] defines which codec should ffmpeg use to video.
- The directive [optivideo.CODEC] defines a list of options for ffmpeg to be passed through. See man ffmpeg.

### Image
- The directive [optiimage] configure the image encoder.
- The directive [optiimage.CODEC] defines a list of options for the image encoder to be passed through. See man <image_encoder>.


## Supported formats
### Video

 - any -> h264 (requires ffmpeg with libx264 encoder)
 - any -> h265 (requires ffmpeg with libx265 encoder)

### Images

 - jpeg -> jpeg (requires jpegoptim)
 - any jpeg -> jpeg-xl (requires cjxl)

