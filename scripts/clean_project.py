import shutil
import os

def clean_project():
    # Remover cache Python
    cache_dirs = ["__pycache__"]
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name in cache_dirs:
                shutil.rmtree(os.path.join(root, dir_name))
    print("Cache e arquivos temporarios removidos!")

if __name__ == "__main__":
    clean_project()
