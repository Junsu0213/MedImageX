def get_slice_position(ds):
    """DICOM 파일에서 슬라이스 위치를 추출합니다."""
    # SliceLocation 태그가 있으면 사용
    if hasattr(ds, 'SliceLocation'):
        return float(ds.SliceLocation)
    
    # ImagePositionPatient 태그가 있으면 Z축 위치 사용
    elif hasattr(ds, 'ImagePositionPatient'):
        # Z축 위치 (일반적으로 세 번째 값)
        return float(ds.ImagePositionPatient[2])
    
    # 둘 다 없으면 InstanceNumber 사용
    elif hasattr(ds, 'InstanceNumber'):
        return float(ds.InstanceNumber)
    
    # 아무것도 없으면 0 반환
    else:
        return 0.0

def analyze_slice_spacing(file_positions):
    """슬라이스 간격을 분석하고 빠진 슬라이스를 감지합니다."""
    if len(file_positions) < 2:
        return None, []
    
    # 슬라이스 위치만 추출 (4개 값 중 두 번째 값)
    positions = [pos for _, pos, _, _ in file_positions]
    
    # 슬라이스 간 간격 계산
    spacings = [abs(positions[i+1] - positions[i]) for i in range(len(positions)-1)]
    
    # 가장 일반적인 간격 찾기 (중앙값 사용)
    median_spacing = sorted(spacings)[len(spacings)//2]
    
    # 빠진 슬라이스 위치 감지
    missing_slices = []
    for i in range(len(positions)-1):
        current_spacing = abs(positions[i+1] - positions[i])
        if current_spacing > median_spacing * 1.5:  # 간격이 일반적인 간격의 1.5배 이상이면
            # 빠진 슬라이스 수 계산
            num_missing = round(current_spacing / median_spacing) - 1
            
            # 빠진 슬라이스 위치 추정
            direction = 1 if positions[i+1] > positions[i] else -1
            for j in range(1, num_missing + 1):
                missing_pos = positions[i] + direction * median_spacing * j
                missing_slices.append(missing_pos)
    
    return median_spacing, missing_slices 