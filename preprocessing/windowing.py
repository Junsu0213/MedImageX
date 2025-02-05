# -*- coding:utf-8 -*-
"""
Created on Wed. FEB. 05 15:02:11 2025
@author: JUN-SU Park

[CT, MRI Image Windowing]

This script provides functionality to apply window level/width adjustments to CT images.
Specifically designed for lung CT images to enhance visualization of different tissue densities.

1. Applies window level/width settings to CT images in Hounsfield Units (HU)
2. Normalizes the resulting image to 8-bit grayscale (0-255)

Example Usage:
    Run this script directly or import `apply_lung_window` in another project.
    
    # For general lung visualization
    windowed_ct = apply_lung_window(ct_array, window_level=-600, window_width=1500)
"""

import numpy as np

def apply_window(data_array, window_level=-600, window_width=1500):
    """
    Applies window level/width adjustments to CT images for better visualization.

    Args:
        data_array (numpy.ndarray): Input CT or MRI image array in Hounsfield Units
        window_level (int, optional): Center of the window in HU. Defaults to -600.
        window_width (int, optional): Width of the window in HU. Defaults to 1500.

    Returns:
        numpy.ndarray: Windowed and normalized CT or MRI image as 8-bit unsigned integer array
    """
    window_min = window_level - window_width/2
    window_max = window_level + window_width/2
    
    # Clip HU values to window range
    data_array = np.clip(data_array, window_min, window_max)
    
    # Normalize to 0-255 range
    data_array = ((data_array - window_min) / (window_max - window_min) * 255.0)
    return data_array.astype(np.uint8)
