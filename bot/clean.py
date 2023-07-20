import os
import shutil
 
 
def purge_cache(path):
    for file_name in os.listdir(path):
        abs_path = os.path.join(path, file_name)
        if file_name == "__pycache__":
            print(abs_path)
            shutil.rmtree(abs_path)
        elif os.path.isdir(abs_path):
            purge_cache(abs_path)
 
 
if __name__ == "__main__":
    path_list = os.path.dirname(
        os.path.abspath(__file__)
    ).split(os.sep)
    root_dir = os.sep.join(path_list[0:-2:])
    purge_cache(root_dir)
 