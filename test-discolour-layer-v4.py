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
#
# -------------------------------------------------------------------------------------
#
# This file is a basic example of a Python plug-in for GIMP.
#
# It can be executed by selecting the menu option: 'Filters/Test/Discolour layer v4'
# or by writing the following lines in the Python console (that can be opened with the
# menu option 'Filters/Python-Fu/Console'):
# >>> image = gimp.image_list()[0]
# >>> layer = image.layers[0]
# >>> gimp.pdb.python_fu_test_discolour_layer_v4(image, layer)

from gimpfu import *

def discolour_layer_v4(img, layer) :
    ''' Converts a layer to gray scale, without modifying his type (RGB or RGBA).
    Note that this version is the fastest, since it make use of tiles.
    
    Parameters:
    img : image The current image.
    layer : layer The layer of the image that is selected.
    '''
    # Indicates that the process has started.
    gimp.progress_init("Discolouring " + layer.name + "...")

    # Set up an undo group, so the operation will be undone in one step.
    pdb.gimp_image_undo_group_start(img)

    # Get the layer position.
    pos = 0;
    for i in range(len(img.layers)):
        if(img.layers[i] == layer):
            pos = i
    
    # Create a new layer to save the results (otherwise is not possible to undo the operation).
    newLayer = gimp.Layer(img, layer.name + " temp", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
    img.add_layer(newLayer, pos)
    layerName = layer.name
    
    # Clear the new layer.
    pdb.gimp_edit_clear(newLayer)
    newLayer.flush()
    
    # Convert the pixels to gray scale.
    try:
        # Calculate the number of tiles.
        tn = int(layer.width / gimp.tile_width())
        if (layer.width % gimp.tile_width() > 0):
            tn += 1
        tm = int(layer.height / gimp.tile_height())
        if (layer.height % gimp.tile_height() > 0):
            tm += 1

        
        # Iterate over the tiles.
        for i in range(tn):
            for j in range(tm):
                # Update the progress bar.
                gimp.progress_update(float(i*tm + j) / float(tn*tm))
        
                # Get the tiles.
                srcTile = layer.get_tile(False, j, i)
                dstTile = newLayer.get_tile(False, j, i)
        
                # Iterate over the pixels of each tile.
                for x in range(srcTile.ewidth):
                    for y in range(srcTile.eheight):
                        # Get the pixel and calculate his gray value.
                        pixel = srcTile[x,y]
                        gray = (ord(pixel[0]) + ord(pixel[1]) + ord(pixel[2]))/3
                        res = chr(gray) + chr(gray) + chr(gray)
                        
                        # If the image has an alpha channel (or any other channel) copy his values.
                        if(len(pixel) > 3):
                            for k in range(len(pixel)-3):
                                res += pixel[k+3]
                                
                        # Save the value in the result layer.
                        dstTile[x,y] = res
        
        # Update the new layer.
        newLayer.flush()
        newLayer.merge_shadow(True)
        newLayer.update(0, 0, newLayer.width, newLayer.height)
        
        # Remove the old layer.
        img.remove_layer(layer)
        
        # Change the name of the new layer (two layers can not have the same name).
        newLayer.name = layerName
    except Exception as err:
        gimp.message("Unexpected error: " + str(err))
    
    # Close the undo group.
    pdb.gimp_image_undo_group_end(img)
    
    # End progress.
    pdb.gimp_progress_end()

register(
    "python_fu_test_discolour_layer_v4",
    "Discolour layer v4",
    "Converts a layer to gray scale. This version is the fastest, since it make use of tiles.",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2013",
    "<Image>/Filters/Test/Discolour layer v4",
    "RGB, RGB*",
    [],
    [],
    discolour_layer_v4)

main()
