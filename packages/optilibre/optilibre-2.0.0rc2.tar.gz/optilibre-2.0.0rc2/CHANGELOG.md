# Changelog

<!--next-version-placeholder-->

## v2.0.0-dev (31/07/2024)
### Feature
- This version introduce a new config file format and a way more robust configuration handling

### Fixes
- Jpeg files not being copied to the newly converted folder when jpegoptim skip it

### Changes
- v2 format for config files, more robust, less verbose, easier to read
- better logging in threaded functions
- migrate from setup.cfg to pyproject.toml

## v1.2.2 (27/04/2023)
### Fixes

- Ignore dest/out directories if they are in input folder

## v1.2.0 (26/04/2023)

### Feature

- Process images and videos recursively

### Changes

- Better build process