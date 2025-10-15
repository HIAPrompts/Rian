import os
import sys
import subprocess

# Definir o caminho do projeto
project_path = os.path.abspath(os.path.dirname(__file__))
src_path = os.path.join(project_path, 'src')

# Executar o main.py usando subprocess
if __name__ == "__main__":
    env = os.environ.copy()
    env['PYTHONPATH'] = src_path
    subprocess.run([sys.executable, os.path.join(src_path, 'main.py')], env=env)