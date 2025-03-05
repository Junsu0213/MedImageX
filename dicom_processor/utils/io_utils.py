import os

def find_patient_dirs(base_dir, prefix='COV-SCO'):
    """지정된 접두사로 시작하는 환자 디렉토리를 찾습니다."""
    return [os.path.join(base_dir, d) for d in os.listdir(base_dir) 
            if d.startswith(prefix) and os.path.isdir(os.path.join(base_dir, d))]

def find_dicom_files(directory):
    """디렉토리에서 DICOM 파일을 찾습니다."""
    return [os.path.join(directory, f) for f in os.listdir(directory) 
            if f.endswith('.dcm') and os.path.isfile(os.path.join(directory, f))] 