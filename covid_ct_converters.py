# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nibabel as nib
import numpy as np  

from preprocessing.windowing import apply_window


ds_dir = r'C:\Users\user\Desktop\DATSET\TEST\HU_threshold'
window_level = -500
window_width = 1300

for file_name in os.listdir(ds_dir):
    file_path = os.path.join(ds_dir, file_name)

    if file_path.endswith('.nii.gz'):
        nii_path = file_path    

        nii_img = nib.load(nii_path)
        data_array = nii_img.get_fdata()

        windowed_ct = apply_window(data_array, window_level, window_width)


        output_path = os.path.join(ds_dir, f'windowed_HU/windowed_[{window_level}-{window_width}]_{file_name}')
        new_img = nib.Nifti1Image(windowed_ct, nii_img.affine)
        nib.save(new_img, output_path)
        
        print(f'처리 완료: {file_name}')
