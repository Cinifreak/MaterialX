# -*- coding: utf-8 -*-
__doc__ = 'Create materialX file conatin standard surface uber shader with input texture for given directory'


import logging
import argparse

import MaterialX

from create_material import create_mtlx_doc, SETTINGS


logger = logging.getLogger('creatematerial')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--outputFilename', dest='outputFilename', help='Filename of the output materialX document (default material.mtlx).')
    parser.add_argument('-s', '--shaderModel', dest='shaderModel', default="standard_surface", help='The shader model to use (standard_surface).')
    parser.add_argument('-c', '--colorSpace', dest='colorSpace', help='Colorsapce to set (default to `srgb_texture`).')
    parser.add_argument('-a', '--absolutePaths', dest='absolutePaths', action="store_true", help='Make the texture paths absolute inside the materialX file.')
    parser.add_argument('-t', '--tileimage', dest='tileimage', action="store_true", help='Use tileimage node instead of image node.')
    parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", help='Turn on verbose mode to create loggings.')
    parser.add_argument(dest='inputDirectory', nargs='?', help='Directory that contain textures (default to current working directory).')
    # TODO : Flag for SG names to be created in mtlx file. default, djed SG pattern or first match.
    # TODO : Flag to seperate each SG for mtlx with the name of each shading group, default combined in one mtlx file name by output file name.
    # TODO : Flag for forcing texture extension if there are multiple extensions in directory.

    options = parser.parse_args()

    texture_path = MaterialX.FilePath.getCurrentPath()

    if options.inputDirectory:
        texture_path = MaterialX.FilePath(options.inputDirectory)

        if not texture_path.isDirectory():
            logger.error("The texture directory does not exist `{}`".format(texture_path))
            return

    default_doc_name = MaterialX.FilePath('standard_surface.mtlx')
    mtlx_file = texture_path / default_doc_name
    if options.outputFilename:
        filepath = MaterialX.FilePath(options.outputFilename)

        if filepath.isAbsolute():
            mtlx_file = filepath
        else:
            mtlx_file = texture_path / filepath

    # Get shader model
    shader_model = 'standard_surface'
    if options.shaderModel:
        shader_model = options.shaderModel

    if shader_model not in SETTINGS.get('shader_model', {}):
        logger.error(f"Cannot find the shader model `{shader_model}` in the configuration")
        return

    # Colorspace
    colorspace = 'srgb_texture'
    if options.colorSpace:
        colorspace = options.colorSpace

    # Verbose
    if options.verbose:
        logger.setLevel(logging.DEBUG)

    create_mtlx_doc(
        texture_path,
        mtlx_file,
        shader_model,
        relative_paths=not options.absolutePaths,
        colorspace=colorspace,
        use_tile_image=options.tileimage
    )


if __name__ == '__main__':
    main()
