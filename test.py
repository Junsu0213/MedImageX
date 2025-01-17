import os
from PIL import Image

data_dir = r'C:\Users\user\Desktop\DATSET\SEG_CT\liver_spleen_mask\1.2.410.200022.500.200509081230312.110828752\103\edited_mask'
# data_dir = r'C:\Users\user\Desktop\DATSET\SEG_CT\liver_spleen_mask\1.3.12.2.1107.5.1.4.50122.4.0.17631462217092495\6\edited_mask'

png_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.png')]
png_files.sort(key=lambda x: int(os.path.basename(x).split('.')[-2]), reverse=data_dir)

for png_file in png_files:
    print(os.path.basename(png_file))
