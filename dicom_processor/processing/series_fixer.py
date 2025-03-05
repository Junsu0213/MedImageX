import os
import uuid
import pydicom
from .orientation import set_orientation
from .slice_analysis import get_slice_position, analyze_slice_spacing

def modify_and_save_dicom(input_file, output_file, instance_number=None, orientation_code=None, new_patient_id=None):
    """
    DICOM 파일을 읽어서 InstanceNumber, 방향 정보, 환자 ID를 변경한 후 새 파일로 저장합니다.
    
    instance_number: 새로운 InstanceNumber (None이면 변경하지 않음)
    orientation_code: 방향 코드 (None이면 변경하지 않음)
    new_patient_id: 새로운 환자 ID (None이면 변경하지 않음)
    """
    try:
        # DICOM 파일 읽기
        ds = pydicom.dcmread(input_file)
        
        # InstanceNumber 변경
        if instance_number is not None:
            original_instance = ds.InstanceNumber if hasattr(ds, 'InstanceNumber') else "알 수 없음"
            ds.InstanceNumber = instance_number
            print(f"InstanceNumber 변경: {original_instance} -> {instance_number}")

        # 방향 정보 변경
        if orientation_code is not None:
            if hasattr(ds, 'ImageOrientationPatient'):
                print(f"원래 방향: {ds.ImageOrientationPatient}")
            else:
                print("원래 파일에 ImageOrientationPatient 태그가 없습니다.")
                ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]  # 기본값 설정
            
            if set_orientation(ds, orientation_code):
                print(f"변경된 방향: {ds.ImageOrientationPatient}")

        # 환자 ID 변경
        if new_patient_id is not None:
            original_id = ds.PatientID if hasattr(ds, 'PatientID') else "알 수 없음"
            ds.PatientID = new_patient_id
            print(f"환자 ID 변경: {original_id} -> {new_patient_id}")
        
        # 변경된 DICOM 파일 저장
        ds.save_as(output_file)
        print(f"파일이 저장되었습니다: {output_file}")
        return True

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return False

def fix_dicom_series(dcm_files, output_dir, new_patient_id=None, orientation_code=None, reverse_order=False):
    """
    DICOM 시리즈를 분석하고 수정하여 연속적인 시리즈로 만듭니다.
    빠진 슬라이스를 감지하고 자동으로 가장 가까운 슬라이스로 채우며,
    모든 슬라이스의 위치 정보를 일관되게 재생성합니다.
    """
    # DICOM 파일과 해당 슬라이스 위치를 저장할 리스트
    file_positions = []
    
    # 각 DICOM 파일의 슬라이스 위치 추출
    for dcm_file in dcm_files:
        try:
            ds = pydicom.dcmread(dcm_file)
            position = get_slice_position(ds)
            file_positions.append((dcm_file, position, ds, False))  # 마지막 False는 복제 여부
        except Exception as e:
            print(f"파일 읽기 오류 ({dcm_file}): {str(e)}")
    
    # 파일이 없는 경우 처리
    if not file_positions:
        print("처리할 DICOM 파일이 없습니다.")
        return 0
    
    # 슬라이스 위치에 따라 정렬
    file_positions.sort(key=lambda x: x[1], reverse=reverse_order)
    
    # 슬라이스 간격 분석 및 빠진 슬라이스 감지
    spacing, missing_slices = analyze_slice_spacing(file_positions)
    
    if missing_slices:
        print(f"\n주의: {len(missing_slices)}개의 슬라이스가 빠진 것으로 감지되었습니다.")
        print(f"일반적인 슬라이스 간격: {spacing:.2f}")
        print("빠진 슬라이스 위치:")
        for pos in missing_slices:
            print(f"  - 위치 {pos:.2f}")
        
        # 빠진 슬라이스를 가장 가까운 슬라이스로 복제하여 채우기
        new_file_positions = []
        
        # 기존 파일 위치 복사
        for item in file_positions:
            new_file_positions.append(item)
        
        # 빠진 슬라이스마다 가장 가까운 슬라이스 찾아 복제
        for missing_pos in missing_slices:
            # 가장 가까운 슬라이스 찾기
            closest_idx = min(range(len(file_positions)), 
                             key=lambda i: abs(file_positions[i][1] - missing_pos))
            
            closest_file, _, closest_ds, _ = file_positions[closest_idx]
            
            # 새 DICOM 객체 생성 (복제)
            new_ds = pydicom.dcmread(closest_file)
            
            # 위치 정보 업데이트
            if hasattr(new_ds, 'SliceLocation'):
                new_ds.SliceLocation = missing_pos
            
            if hasattr(new_ds, 'ImagePositionPatient'):
                # Z축 위치만 변경
                pos = list(new_ds.ImagePositionPatient)
                pos[2] = missing_pos
                new_ds.ImagePositionPatient = pos
            
            # 새 SOPInstanceUID 생성 (고유 식별자)
            new_ds.SOPInstanceUID = str(uuid.uuid4())
            
            # 복제된 슬라이스 추가 (마지막 True는 복제 여부)
            new_file_positions.append((closest_file, missing_pos, new_ds, True))
        
        # 슬라이스 위치에 따라 다시 정렬
        new_file_positions.sort(key=lambda x: x[1], reverse=reverse_order)
        file_positions = new_file_positions
        
        print(f"{len(missing_slices)}개의 빠진 슬라이스를 복제하여 채웠습니다.")
    
    # 슬라이스 위치 정보 완전 재생성
    # 첫 번째 슬라이스와 마지막 슬라이스의 위치를 기준으로 균등한 간격으로 재설정
    total_slices = len(file_positions)
    
    # 첫 번째와 마지막 슬라이스의 위치 정보 가져오기
    first_position = file_positions[0][1]
    last_position = file_positions[-1][1]
    
    # 방향에 따라 시작과 끝 위치 결정
    if reverse_order:
        start_pos = last_position
        end_pos = first_position
    else:
        start_pos = first_position
        end_pos = last_position
    
    # 전체 범위 계산
    total_range = abs(end_pos - start_pos)
    
    # 슬라이스 간격 계산 (균등 분배)
    if total_slices > 1:
        new_spacing = total_range / (total_slices - 1)
    else:
        new_spacing = 0
    
    print(f"\n슬라이스 위치 정보 재생성:")
    print(f"시작 위치: {start_pos:.2f}, 끝 위치: {end_pos:.2f}")
    print(f"슬라이스 수: {total_slices}, 새 간격: {new_spacing:.2f}")
    
    # 각 슬라이스의 새 위치 계산 및 저장
    for i, (dcm_file, _, ds, is_cloned) in enumerate(file_positions):
        # 새 위치 계산
        if reverse_order:
            new_position = start_pos - (i * new_spacing)
        else:
            new_position = start_pos + (i * new_spacing)
        
        # 복제된 슬라이스인 경우
        if is_cloned:
            output_file = os.path.join(output_dir, f"slice_{i+1:04d}.dcm")
            
            # 위치 정보 업데이트
            if hasattr(ds, 'SliceLocation'):
                ds.SliceLocation = new_position
            
            if hasattr(ds, 'ImagePositionPatient'):
                pos = list(ds.ImagePositionPatient)
                pos[2] = new_position
                ds.ImagePositionPatient = pos
            
            # InstanceNumber 설정
            ds.InstanceNumber = i + 1
            
            # 방향 정보 설정
            if orientation_code is not None:
                set_orientation(ds, orientation_code)
            
            # 환자 ID 설정
            if new_patient_id is not None:
                ds.PatientID = new_patient_id
            
            # 저장
            ds.save_as(output_file)
            print(f"복제된 슬라이스 저장: {output_file}, 위치: {new_position:.2f}")
        
        # 기존 파일인 경우
        else:
            output_file = os.path.join(output_dir, os.path.basename(dcm_file))
            
            # 기존 파일 읽기
            ds_orig = pydicom.dcmread(dcm_file)
            
            # 위치 정보 업데이트
            if hasattr(ds_orig, 'SliceLocation'):
                ds_orig.SliceLocation = new_position
            
            if hasattr(ds_orig, 'ImagePositionPatient'):
                pos = list(ds_orig.ImagePositionPatient)
                pos[2] = new_position
                ds_orig.ImagePositionPatient = pos
            
            # InstanceNumber 설정
            ds_orig.InstanceNumber = i + 1
            
            # 방향 정보 설정
            if orientation_code is not None:
                set_orientation(ds_orig, orientation_code)
            
            # 환자 ID 설정
            if new_patient_id is not None:
                ds_orig.PatientID = new_patient_id
            
            # 저장
            ds_orig.save_as(output_file)
            print(f"파일 저장: {output_file}, 위치: {new_position:.2f}")
    
    return total_slices 