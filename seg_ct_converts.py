# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from converters.dicom2nii_converters import convert_dicom_to_nii
from converters.png2nii_converters import convert_png_to_nii


ds_dir = r'C:\Users\user\Desktop\DATSET\SEG_CT\liver_spleen_mask'
save_dir = r'C:\Users\user\Desktop\DATSET\SEG_CT\nii_dataset'
os.makedirs(save_dir, exist_ok=True)

df = pd.read_csv(os.path.join(os.path.dirname(ds_dir), 'patient_info.csv'), encoding='utf-8')

for i, row in df.iterrows():
    study_uid = row['Study UID']
    seq_num = row['Series Number']
    num = row['num']

    print(f'{num}번째 파일 변환 중...')

    dcm_dir = os.path.join(ds_dir, str(study_uid), str(seq_num), 'dcm')
    origin_mask_dir = os.path.join(ds_dir, str(study_uid), str(seq_num), 'original_mask')
    edited_mask_dir = os.path.join(ds_dir, str(study_uid), str(seq_num), 'edited_mask')

    convert_dicom_to_nii(dcm_dir, save_dir, file_name=f'{num}_CT')
    convert_png_to_nii(origin_mask_dir, dcm_dir, save_dir, file_name=f'{num}_origin_mask', label_num=2)
    convert_png_to_nii(edited_mask_dir, dcm_dir, save_dir, file_name=f'{num}_edited_mask', label_num=2)
