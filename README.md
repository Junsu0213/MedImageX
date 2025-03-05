# Medical Image Processing Suite

This repository contains a comprehensive set of tools for processing, converting, and analyzing medical imaging data. The suite includes DICOM series processing, format conversion utilities, and image preprocessing tools designed to prepare medical images for research, analysis, and visualization.

## Overview

The Medical Image Processing Suite provides three main categories of functionality:

1. **DICOM Processor**: Analyze and fix DICOM series files
2. **Format Converters**: Convert between medical imaging formats
3. **Image Preprocessing**: Apply preprocessing techniques to medical images

## Directory Structure

```
project_root/
├── dicom_processor/           # DICOM processing modules
│   ├── __init__.py
│   ├── main.py                # Main DICOM processor execution
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── io_utils.py        # File I/O related functions
│   │   └── user_interface.py  # User interface functions
│   └── processing/            # Processing modules
│       ├── __init__.py
│       ├── orientation.py     # Orientation information processing
│       ├── slice_analysis.py  # Slice analysis
│       └── series_fixer.py    # Series modification and regeneration
├── converters/                # Format conversion utilities
│   ├── dicom2nii_converters.py # DICOM to NIfTI conversion
│   └── png2nii_converters.py   # PNG to NIfTI conversion
├── preprocessing/             # Image preprocessing tools
│   └── windowing.py           # CT/MRI windowing functions
└── README.md
```

## Features

### DICOM Processor
- **Slice Analysis**: Analyze slice spacing and detect missing slices
- **Missing Slice Replication**: Automatically fill gaps by duplicating nearest slices
- **Metadata Modification**: Edit PatientID, InstanceNumber, and other DICOM tags
- **Orientation Setting**: Set ImageOrientationPatient values with predefined codes
- **Position Regeneration**: Recreate slice positions with consistent spacing
- **Series Reordering**: Option to reverse slice order

### Format Converters
- **DICOM to NIfTI**: Convert DICOM series to 3D NIfTI files
- **PNG to NIfTI**: Convert PNG image series to 3D NIfTI files
- **Parallel Processing**: Multi-threaded image loading for faster conversion

### Preprocessing Tools
- **CT/MRI Windowing**: Apply window level/width adjustments to enhance visualization
- **HU Normalization**: Normalize Hounsfield Units to standardized ranges
- **Grayscale Conversion**: Convert to 8-bit grayscale for consistent processing

## Requirements

```
pydicom
numpy
SimpleITK
nibabel
Pillow
```

## Installation

```bash
git clone https://github.com/yourusername/medical-image-processing.git
cd medical-image-processing
pip install -r requirements.txt
```

## Usage

### DICOM Processor

```bash
# Process DICOM series with command line interface
python -m dicom_processor.main --input "/path/to/input" --output "/path/to/output" --prefix "PATIENT-PREFIX" --reverse
```

Parameters:
- `--input`, `-i`: Input directory path
- `--output`, `-o`: Output directory path
- `--prefix`, `-p`: Patient directory prefix (default: 'COV-SCO')
- `--reverse`, `-r`: Reverse slice ordering (flag)

### Format Converters

```python
# Convert DICOM to NIfTI
from converters.dicom2nii_converters import convert_dicom_to_nii

convert_dicom_to_nii(
    input_dir='/path/to/dicom/files',
    output_dir='/path/to/output',
    file_name='output_nifti'
)

# Convert PNG masks to NIfTI
from converters.png2nii_converters import convert_png_to_nii

convert_png_to_nii(
    input_dir='/path/to/png/files',
    reference_dcm_dir='/path/to/reference/dicom',
    output_dir='/path/to/output',
    file_name='mask_nifti',
    label_num=2
)
```

### Preprocessing Tools

```python
# Apply windowing to CT images
from preprocessing.windowing import apply_window
import nibabel as nib
import numpy as np

# Load NIfTI file
nii_img = nib.load('/path/to/ct_file.nii.gz')
data_array = nii_img.get_fdata()

# Apply lung window
windowed_ct = apply_window(data_array, window_level=-600, window_width=1500)

# Save result
new_img = nib.Nifti1Image(windowed_ct, nii_img.affine)
nib.save(new_img, '/path/to/output/windowed_ct.nii.gz')
```

## Module Details

### dicom_processor.main

Main entry point for DICOM processing:
- Parses command-line arguments
- Finds patient directories
- Controls the DICOM processing workflow

### converters.dicom2nii_converters

Provides DICOM to NIfTI conversion:
- `convert_dicom_to_nii(input_dir, output_dir, file_name)`: Convert DICOM series to NIfTI

### converters.png2nii_converters

Provides PNG to NIfTI conversion:
- `convert_png_to_nii(input_dir, reference_dcm_dir, output_dir, file_name, label_num)`: Convert PNG series to NIfTI

### preprocessing.windowing

Provides windowing functions for medical images:
- `apply_window(data_array, window_level, window_width)`: Apply window level/width adjustments

## Workflow Examples

### Processing CT Data for AI Model Training

1. Use DICOM Processor to normalize and fix spacing issues in raw DICOM series
2. Convert the processed DICOM files to NIfTI format using dicom2nii_converters
3. Apply appropriate windowing for the target anatomy using the windowing module
4. Convert segmentation masks from PNG to NIfTI using png2nii_converters
5. The resulting paired image and mask NIfTI files are ready for AI model training

### Visualizing Lung CT Images

1. Convert DICOM series to NIfTI using dicom2nii_converters
2. Apply lung-specific windowing parameters (level: -600, width: 1500) using the apply_window function
3. Use the windowed images for improved visualization of lung parenchyma

## Advantages

1. **Modular Design**: Each functionality is isolated in separate modules for better maintainability
2. **Format Flexibility**: Support for various medical image formats (DICOM, NIfTI, PNG)
3. **Preprocessing Integration**: Built-in preprocessing capabilities for immediate use
4. **Research Ready**: Tools designed for preparing data for research and AI applications
5. **Automated Error Handling**: Automatic detection and correction of common issues in medical images

## Notes

- The DICOM processor automatically detects slice spacing inconsistencies
- Missing slices are filled with duplicates of the nearest available slice
- Series can be optionally reversed depending on acquisition parameters
- The converters preserve original metadata when possible
- Windowing parameters can be customized for specific anatomical structures 