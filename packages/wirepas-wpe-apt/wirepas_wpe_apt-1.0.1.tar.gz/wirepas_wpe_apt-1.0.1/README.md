# Wirepas WPE analysis and playback tool

The goals of this python library is to evaluate quickly the positioning setup: i.e. analysing positioning performance and generate a performance report.

This folder contain a module to analyse positioning results and playback of collected measurements.


## Installation

This tool was originally created on python 3.8 but it is incompatible with 3.9+
due to thread comportement changes.

This library can be install locally from source directly with the following command:

`pip install -e .`


## How it works

The module provides tools to get previously computed locations of tags, the WNT metadata (floor plans, areas, images, ...), and the anchors positions. By placing the real positions of a few selected tags on the floor plans and setting them as planning nodes with a new network id (the same network id for all those reference positions) and the same node id as the tag they are referencing, users can check the positioning perfomances of their system over time.

For additional information, please refer to the python [WPE APT documentation](./wirepas_wpe_apt/README.md).


## Backend version

The WPE APT library has been created to work with WNT version until 4.4 and WPE until 1.7.
Users should not have to worry about their backend version as it is already handled by the tool itself.
The tool has been tested with WNT versions 4.3 and 4.4 and WPE versions 1.6 and 1.7 but should work with previous versions.


License
-------

Copyright 2024 Wirepas Ltd licensed under Apache License, Version 2.0 See file
[LICENSE](LICENSE) for full license details.
