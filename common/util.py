#!/usr/bin/env python3

import cv2
import os


def escape_home_in_path(sPath):
    return os.path.expanduser(sPath)


def save_image(aImage, sPathToImage):
    """saves a given image to the given location"""
    cv2.imwrite(escape_home_in_path(sPathToImage), aImage)


def load_image(sPathToImage):
    """load an image from disk"""
    return cv2.imread(escape_home_in_path(sPathToImage))


def create_path(sPath):
    """ create a path if it is not existend yet"""
    sPathEscape = os.path.expanduser(sPath)
    try:
        if not os.path.exists(sPathEscape):
            os.makedirs(sPathEscape)
        return sPathEscape
    except:
        print("some error occurred while creating dir %s" % (sPathEscape))


def check_if_path_exists(sPath):
    """ returns Ture if a given path is existend """
    sPathEscape = os.path.expanduser(sPath)
    return os.path.exists(sPathEscape)


def list_all_images_in_directory(sDirectoryPath):
    """ returns as list of all images in a given subfolder """
    sDirectoryPathEscaped = escape_home_in_path(sDirectoryPath)
    if not check_if_path_exists(sDirectoryPathEscaped):
        raise Exception("path %s does not exist" % sDirectoryPathEscaped)
    if not sDirectoryPathEscaped.endswith("/"):
        sDirectoryPathEscaped += "/"
    aFiles = next(os.walk(sDirectoryPathEscaped))[2]
    # filter image files
    return [sDirectoryPathEscaped +
            m for m in aFiles if m.lower().endswith((".png", ".bmp", ".jpg", ".jpeg", ".tiff"))]
