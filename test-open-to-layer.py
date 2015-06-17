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

def open_to_layer(image, layer, file):
    ''' Save the current layer into a PNG file, a JPEG file and a BMP file.
    
    Parameters:
    image : image The current image.
    layer : layer The layer of the image that is selected.
    file : string The file to open in a new layer.
    '''
    # Indicates that the process has started.
    gimp.progress_init("Opening '" + file + "'...")
    
    try:
        # Open file.
        fileImage = None
        if(file.lower().endswith(('.png'))):
            fileImage = pdb.file_png_load(file, file)
        if(file.lower().endswith(('.jpeg', '.jpg'))):
            fileImage = pdb.file_jpeg_load(file, file)
        if(file.lower().endswith(('.bmp'))):
            fileImage = pdb.file_bmp_load(file, file)
        if(file.lower().endswith(('.gif'))):
            fileImage = pdb.file_gif_load(file, file)
        
        if(fileImage is None):
            gimp.message("The image could not be opened since it is not an image file.")
        else :
            # Create new layer.
            newLayer = gimp.Layer(image, "new layer", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
            image.add_layer(newLayer, 0)               
        
            # Put image into the new layer.
            fileLayer = fileImage.layers[0]
            pdb.gimp_edit_copy(fileLayer)
            pdb.gimp_edit_paste(newLayer, True)
        
            # Update the new layer.
            newLayer.flush()
            newLayer.merge_shadow(True)
            newLayer.update(0, 0, newLayer.width, newLayer.height)
        
    except Exception as err:
        gimp.message("Unexpected error: " + str(err))
    
register(
    "python_fu_test_open_to_layer",
    "Open file in new layer",
    "Opens an image into a new layer.",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2013",
    "<Image>/Filters/Test/Open file in new layer",
    "*",
    [
        (PF_FILE, "file", "File to open", ""),
    ],
    [],
    open_to_layer)

main()
