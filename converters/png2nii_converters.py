# -*- coding:utf-8 -*-
"""
Created on Fri. JAN. 10 16:43:09 2025
@author: JUN-SU Park

[PNG to NIfTI Converter]

This script provides functionality to convert a series of PNG images to a NIfTI format.

1. Reads PNG images from the input directory.
2. Converts the images into a 3D NIfTI file and saves it to the output directory.

Example Usage:
    Run this script directly or import `convert_png_to_nii` in another project.
"""

import os
import numpy as np
from PIL import Image
import SimpleITK as sitk
from concurrent.futures import ThreadPoolExecutor
import pydicom


def read_image(png_path):
    """Read a PNG image and return as a numpy array."""
    with Image.open(png_path) as img:
        return np.array(img)


def convert_png_to_nii(input_dir, reference_dcm_dir, output_dir: str = None, file_name: str = None, label_num: int = 1):
    """
    Converts a series of PNG images to a NIfTI file.

    Args:
        input_dir (str): Path to the directory containing the PNG images.
        reference_dcm_dir (str): Path to a directory containing DICOM files to determine the sorting order of PNG files.
        output_dir (str, optional): Path to save the converted NIfTI file. Defaults to a 'nii' folder in the parent directory of `input_dir`.
        file_name (str, optional): Name of the output NIfTI file. Defaults to the name of the `input_dir`.
        label_num (int, optional): Number of labels for scaling the image array. Defaults to 1.

    Returns:
        None: The function saves the converted NIfTI file directly to the specified `output_dir`.
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(input_dir), 'nii')

    os.makedirs(output_dir, exist_ok=True)

    if file_name is None:
        file_name = os.path.basename(input_dir)

    # Get DICOM file order using SimpleITK
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(reference_dcm_dir)
    # Extract the last number from each DICOM filename
    dicom_numbers = [os.path.basename(f).split('.')[-2] for f in dicom_names]
    
    # Create PNG filenames based on DICOM order
    png_files = []
    base_name = os.path.basename(os.listdir(input_dir)[0]).rsplit('.', 2)[0]  # Get the common part of PNG filename
    for num in dicom_numbers:
        png_name = f"{base_name}.{num}.png"
        png_path = os.path.join(input_dir, png_name)
        if os.path.exists(png_path):
            png_files.append(png_path)

    # Use ThreadPoolExecutor for parallel image reading
    with ThreadPoolExecutor() as executor:
        image_stack = list(executor.map(read_image, png_files))

    # Convert the list of images to a 3D numpy array
    image_3d_array = np.stack(image_stack, axis=0)

    # Scale the image array to the number of labels
    image_3d_array = (image_3d_array / int(255 / label_num)).astype(np.uint8)

    # Convert numpy array to SimpleITK image
    image_3d = sitk.GetImageFromArray(image_3d_array)

    sitk.WriteImage(image_3d, os.path.join(output_dir, f'{file_name}.nii.gz'))


if __name__ == '__main__':
    input_dir = r'C:\Users\user\Desktop\DATSET\Test_Dataset\SEG_CT\nii_converter_test\edited_mask'
    file_name = '1_mask'
    label_num = 2
    convert_png_to_nii(input_dir, file_name=file_name, label_num=label_num)
