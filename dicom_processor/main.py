import os
import argparse
from utils.user_interface import get_user_input
from utils.io_utils import find_patient_dirs, find_dicom_files
from processing.series_fixer import fix_dicom_series

def main():
    parser = argparse.ArgumentParser(description='DICOM 시리즈 처리 도구')
    parser.add_argument('--input', '-i', type=str, default=r'C:\Users\user\Desktop\DATSET\aview_upload\서종현',
                        help='입력 디렉토리 경로')
    parser.add_argument('--output', '-o', type=str, default=r'C:\Users\user\Desktop\DATSET\aview_upload\서종현_modifited_test',
                        help='출력 디렉토리 경로')
    parser.add_argument('--prefix', '-p', type=str, default='COV-SCO',
                        help='환자 디렉토리 접두사')
    parser.add_argument('--reverse', '-r', action='store_true',
                        help='슬라이스를 역순으로 정렬')
    
    args = parser.parse_args()
    
    # 디렉토리 존재 여부 확인
    if not os.path.exists(args.input):
        print(f"오류: 입력 디렉토리가 존재하지 않습니다: {args.input}")
        return 1
        
    # 출력 디렉토리 생성
    os.makedirs(args.output, exist_ok=True)

    # 환자 디렉토리 찾기
    patient_dirs = find_patient_dirs(args.input, args.prefix)
    if not patient_dirs:
        print(f"처리할 환자 디렉토리가 없습니다: {args.input}")
        return 0

    # 정렬 순서 설정 (명령줄 인수가 없으면 사용자에게 물어봄)
    reverse_sorting = args.reverse
    if not args.reverse:
        reverse_sorting = get_user_input("슬라이스를 역순으로 정렬하시겠습니까? (y/n)", "y").lower() == 'y'

    # 환자별 처리
    for patient_dir in patient_dirs:
        patient_name = os.path.basename(patient_dir)
        new_patient_id = os.path.basename(patient_dir)
        print(f"환자: {patient_name}")
        
        ord_dirs = [os.path.join(patient_dir, d) for d in os.listdir(patient_dir)]
        for ord_dir in ord_dirs:
            dir_suffix = f'modified_{os.path.basename(ord_dir)}'
            if reverse_sorting:
                dir_suffix += '_reversed'
            output_dir = os.path.join(args.output, patient_name, dir_suffix)
            os.makedirs(output_dir, exist_ok=True)

            print(f"처리 중: {ord_dir}")
            dcm_files = find_dicom_files(ord_dir)
            
            if not dcm_files:
                print(f"DICOM 파일이 없습니다: {ord_dir}")
                continue
                
            # DICOM 파일 정렬 및 InstanceNumber 재설정
            num_files = fix_dicom_series(
                dcm_files, 
                output_dir, 
                new_patient_id=new_patient_id,
                reverse_order=reverse_sorting
            )
            
            print(f"{num_files}개 파일 처리 완료")
            print('--------------------------------')

    print("모든 처리가 완료되었습니다.")
    return 0

if __name__ == "__main__":
    exit(main()) 