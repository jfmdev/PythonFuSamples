#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Copyright (c) 2013, Jose F. Maldonado
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
#
#    - Redistributions of source code must retain the above copyright notice, this 
#    list of conditions and the following disclaimer.
#    - Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation and/or 
#    other materials provided with the distribution.
#    - Neither the name of the author nor the names of its contributors may be used 
#    to endorse or promote products derived from this software without specific prior 
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH 
# DAMAGE.

from gimpfu import *

def save_to_files(image, layer, outputFolder):
    ''' Save the current layer into a PNG file, a JPEG file and a BMP file.
    
    Parameters:
    image : image The current image.
    layer : layer The layer of the image that is selected.
    outputFolder : string The folder in which to save the images.
    '''
    # Indicates that the process has started.
    gimp.progress_init("Saving to '" + outputFolder + "'...")
    
    try:
        # Save as PNG
        gimp.pdb.file_png_save(image, layer, outputFolder + "\\" + layer.name + ".png", "raw_filename", 0, 9, 0, 0, 0, 0, 0)
        
        # Save as JPEG
        gimp.pdb.file_jpeg_save(image, layer, outputFolder + "\\" + layer.name + ".jpg", "raw_filename", 0.9, 0, 0, 0, "Creating with GIMP", 0, 0, 0, 0)
        
        # Save as BMP
        gimp.pdb.file_bmp_save(image, layer, outputFolder + "\\" + layer.name + ".bmp", "raw_filename")
    except Exception as err:
        gimp.message("Unexpected error: " + str(err))
    
register(
    "python_fu_test_save_to_files",
    "Save to files",
    "Save the current layer into a PNG file, a JPEG file and a BMP file.",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2013",
    "<Image>/Filters/Test/Save to files",
    "*",
    [
        (PF_DIRNAME, "outputFolder", "Output directory", ""),
    ],
    [],
    save_to_files)

main()
