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
# It can be executed by selecting the menu option: 'Filters/Test/Split channels'
# or by writing the following lines in the Python console (that can be opened with the
# menu option 'Filters/Python-Fu/Console'):
# >>> image = gimp.image_list()[0]
# >>> layer = image.layers[0]
# >>> gimp.pdb.python_fu_test_split_channels(image, layer)

from gimpfu import *

def split_channels(img, layer) :
    ''' Creates three layers with the RGB channels of the selected layer.
    
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
            
    # Create the new layers.
    layerR = gimp.Layer(img, layer.name + " Red", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
    layerG = gimp.Layer(img, layer.name + " Green", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
    layerB = gimp.Layer(img, layer.name + " Blue", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
    img.add_layer(layerR, pos)
    img.add_layer(layerG, pos)
    img.add_layer(layerB, pos)
    
    # Clear the new layers.
    pdb.gimp_edit_clear(layerR)
    layerR.flush()
    pdb.gimp_edit_clear(layerG)
    layerG.flush()
    pdb.gimp_edit_clear(layerB)
    layerB.flush()
    
    # Separate the channels.
    try:
        # Calculate the number of tiles.
        tn = int(layer.width / 64)
        if(layer.width % 64 > 0):
            tn += 1
        tm = int(layer.height / 64)
        if(layer.height % 64 > 0):
            tm += 1
        
        # Iterate over the tiles.
        for i in range(tn):
            for j in range(tm):
                # Update the progress bar.
                gimp.progress_update(float(i*tm + j) / float(tn*tm))
        
                # Get the tiles.
                tile = layer.get_tile(False, j, i)
                tileR = layerR.get_tile(False, j, i)
                tileG = layerG.get_tile(False, j, i)
                tileB = layerB.get_tile(False, j, i)
        
                # Iterate over the pixels of each tile.
                for x in range(tile.ewidth):
                    for y in range(tile.eheight):
                        # Get the pixel and separate his colors.
                        pixel = tile[x,y]
                        pixelR = pixel[0] + "\x00\x00"
                        pixelG = "\x00" + pixel[1] + "\x00"
                        pixelB = "\x00\x00" + pixel[2]
                        
                        # If the image has an alpha channel (or any other channel) copy his values.
                        if(len(pixel) > 3):
                            for k in range(len(pixel)-3):
                                pixelR += pixel[k+3]
                                pixelG += pixel[k+3]
                                pixelB += pixel[k+3]
                                
                        # Save the value in the channel layers.
                        tileR[x,y] = pixelR
                        tileG[x,y] = pixelG
                        tileB[x,y] = pixelB
        
        # Update the new layers.
        tileR.flush()
        tileR.merge_shadow(True)
        tileR.update(0, 0, tileR.width, tileR.height)
        tileG.flush()
        tileG.merge_shadow(True)
        tileG.update(0, 0, tileG.width, tileG.height)
        tileB.flush()
        tileB.merge_shadow(True)
        tileB.update(0, 0, tileB.width, tileB.height)
        
    except Exception as err:
        gimp.message("Unexpected error: " + str(err))
    
    # Close the undo group.
    pdb.gimp_image_undo_group_end(img)
    
    # End progress.
    pdb.gimp_progress_end()

register(
    "python_fu_test_split_channels",
    "Split channels",
    "Creates three layers with the RGB channels of the selected layer.",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2013",
    "<Image>/Filters/Test/Split channels",
    "RGB, RGB*",
    [],
    [],
    split_channels)

main()
