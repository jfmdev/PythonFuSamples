Python-Fu samples
=================

**Python-Fu samples** is a package that contains 12 scripts, developed using Python and GIMP 2.8, which objective is to serve as templates and as code samples to programmers that are new in Python-Fu scripting.

In order to install these scripts, you must copy them in the _plug-ins_ folder of GIMP (normally `GIMP 2/lib/gimp/2.0/plug-ins`).
After installed, the scripts can be found in `Filters -> Test` .

## Basic scripts

These scripts are basic examples of how to create a Python plugin.

 * **test-hello-world** only displays a 'Hello world' message, this is the more simplest example.
 * **test-invert-layer** inverts the current layer.
 * **test-say-something** ask to the user to enter an string and then displays that string.

## File scripts

These script shows how to open and save files.

 * **test-save-to-files** ask to the user for an output folder, and then saves the current layer in a PNG file, a JPEG file and a BMP file.
 * **test-open-to-layer** ask to the user to select an image file and then opens that file in a new layer.

## Pixel level scripts

These scripts shows how to perform pixel level operations.

 * **test-discolour-layer-v1** converts an image to grey scale. This script is the most simple, but also the most slow and buggy.
 * **test-discolour-layer-v2** similar to v1, makes uses of pixel regions objects and corrects the bug related to the 'Undo' button.
 * **test-discolour-layer-v3** is a bit more efficient that v1 and v2, since it converts the pixel regions objects to arrays, but still very slow compared to v4.
 * **test-discolour-layer-v4** is the most efficient version, since it makes use of tiles.
 * **test-split-channels** split an image into his RGB channels.

## Batch scripts

These scripts shows how to perform batch operations over a group of images located in a folder. They ask to the user for the input folder, in which the images are located, and for the output folder, in which the new images are going to be saved.

 * **test-batch-invert** inverts all the images in a folder.
 * **test-batch-cartoon** apply the cartoon filter to all the images in a folder.


License
-------

Python-Fu Samples is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Python-Fu Samples is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Python-Fu Samples. If not, see <http://www.gnu.org/licenses/>.