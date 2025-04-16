import os
import shutil
current_dir = os.getcwd()
for dirs,subdirs,files in os.walk(current_dir):
    base_dir = os.path.basename(os.path.normpath(dirs))
    if base_dir == "migrations":
        for file in files:
            file_path = os.path.join(dirs,file)
            if os.path.basename(file_path) == "__init__.py":
                pass
            else:
                os.remove(file_path)
        
        for subdir in subdirs:
            subdir_path = os.path.join(dirs,subdir)
            if os.path.basename(subdir_path) == "__pycache__":
                shutil.rmtree(subdir_path)