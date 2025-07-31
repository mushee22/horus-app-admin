# import os
# import shutil
# current_dir = os.getcwd()
# for dirs,subdirs,files in os.walk(current_dir):
#     base_dir = os.path.basename(os.path.normpath(dirs))
#     if base_dir == "migrations":
#         for file in files:
#             file_path = os.path.join(dirs,file)
#             if os.path.basename(file_path) == "__init__.py":
#                 pass
#             else:
#                 os.remove(file_path)
        
#         for subdir in subdirs:
#             subdir_path = os.path.join(dirs,subdir)
#             if os.path.basename(subdir_path) == "__pycache__":
#                 shutil.rmtree(subdir_path)


import os
import shutil

# Get the current working directory (your Django project root)
current_dir = os.getcwd()

for root, subdirs, files in os.walk(current_dir):
    # Skip system/virtual environment directories
    if any(skip in root for skip in ['venv', 'env', 'site-packages', 'dist-packages']):
        continue

    # Target only 'migrations' folders
    if os.path.basename(root) == 'migrations':
        print(f"Cleaning: {root}")
        
        # Delete migration files except __init__.py
        for file in files:
            if file != '__init__.py' and file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Deleting file: {file_path}")
                os.remove(file_path)

        # Remove __pycache__ directories inside migrations
        for subdir in subdirs:
            if subdir == '__pycache__':
                cache_path = os.path.join(root, subdir)
                print(f"Removing cache: {cache_path}")
                shutil.rmtree(cache_path)