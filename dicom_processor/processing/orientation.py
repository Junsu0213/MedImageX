def set_orientation(ds, orientation_code):
    """
    DICOM 파일의 ImageOrientationPatient 값을 지정된 방향 코드에 따라 설정합니다.
    
    orientation_code: 원하는 방향 코드 (예: 'RAP', 'LPS' 등)
    """
    # 방향 코드에 따른 ImageOrientationPatient 값 매핑
    orientation_values = {
        # 일반적인 축 방향 (Axial)
        'LPH': [1, 0, 0, 0, 1, 0],  # Left-Posterior-Head
        'RAH': [-1, 0, 0, 0, -1, 0],  # Right-Anterior-Head
        'RPS': [-1, 0, 0, 0, 1, 0],  # Right-Posterior-Superior
        'LAS': [1, 0, 0, 0, -1, 0],  # Left-Anterior-Superior
        
        # 관상면 방향 (Coronal)
        'LSH': [1, 0, 0, 0, 0, 1],  # Left-Superior-Head
        'RIH': [-1, 0, 0, 0, 0, 1],  # Right-Inferior-Head
        'RSF': [-1, 0, 0, 0, 0, -1],  # Right-Superior-Feet
        'LIF': [1, 0, 0, 0, 0, -1],  # Left-Inferior-Feet
        
        # 시상면 방향 (Sagittal)
        'PSH': [0, 1, 0, 0, 0, 1],  # Posterior-Superior-Head
        'AIH': [0, -1, 0, 0, 0, 1],  # Anterior-Inferior-Head
        'ASF': [0, -1, 0, 0, 0, -1],  # Anterior-Superior-Feet
        'PIF': [0, 1, 0, 0, 0, -1],  # Posterior-Inferior-Feet
    }
    
    if orientation_code in orientation_values:
        ds.ImageOrientationPatient = orientation_values[orientation_code]
        return True
    else:
        print(f"지원되지 않는 방향 코드: {orientation_code}")
        return False 