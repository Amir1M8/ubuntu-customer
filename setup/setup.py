# #!/usr/bin/env python3
# import os
# import shutil

# dest_dir = os.path.expanduser("~/.ubuntu-customer")
# os.makedirs(dest_dir, exist_ok=True)

# folders = ["../setting", "../dconf", "../gtk", "../wallpapers"]

# for folder in folders:
#     if os.path.exists(folder):
#         for file in os.listdir(folder):
#             src = os.path.join(folder, file)
#             dst = os.path.join(dest_dir, file)
            
#             if os.path.isfile(src) and not os.path.exists(dst):
#                 shutil.copy2(src, dst)
#                 print(f"[INFO] Copying {folder}/{file}")
#             elif os.path.isfile(src):
#                 print(f"[INFO] {file} Exist.")
#     else:
#         print(f"[ERROR] {folder} not found!")

#!/usr/bin/env python3
import os
import shutil

dest_dir = os.path.expanduser("~/.ubuntu-customer")
os.makedirs(dest_dir, exist_ok=True)

folders = [
    ("../setting", "setting"),      # source, destination folder name
    ("../dconf", "dconf"),
    ("../gtk", "gtk"),
    ("../wallpapers", "wallpapers")
]

for src_folder, dest_folder_name in folders:
    if os.path.exists(src_folder):

        dest_folder = os.path.join(dest_dir, dest_folder_name)
        os.makedirs(dest_folder, exist_ok=True)
        
        for file in os.listdir(src_folder):
            src = os.path.join(src_folder, file)
            dst = os.path.join(dest_folder, file)
            
            if os.path.isfile(src) and not os.path.exists(dst):
                shutil.copy2(src, dst)
                print(f"[INFO] Copying {src_folder}/{file}")
            elif os.path.isfile(src):
                print(f"[INFO] {dest_folder_name}/{file} already exists.")
    else:
        print(f"[ERROR] {src_folder} not found!")

print("\n[INFO] Done!")