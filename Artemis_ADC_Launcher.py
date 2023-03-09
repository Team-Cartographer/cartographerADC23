import sys
import venv
from os import getcwd, path
from subprocess import run
from utils import show_info


# Create a new virtual environment
venv.create('venv', with_pip=True)

# Activate the virtual environment
venv_folder = path.join(getcwd(), 'venv')
activate_script = path.join(venv_folder, 'Scripts', 'activate.bat')
run(f'cmd /c "{activate_script}"', shell=True, check=True)

# Install the required libraries
run([sys.executable, '-m', 'pip', 'install', 'Pillow'], check=True)
print("Installed Pillow")
run([sys.executable, '-m', 'pip', 'install', 'python-dotenv'], check=True)
print("Installed dotenv")
run([sys.executable, '-m', 'pip', 'install', 'numpy'], check=True)
print("Installed numpy")
run([sys.executable, '-m', 'pip', 'install', 'ursina'], check=True)
print("Installed ursina")

code_path = getcwd()

# runs PathFetcher.exe
print("Running PathFetcher")
pathfetcher_path = code_path + "/PathFetcher/PathFetcher.exe"
pathfetcher_program = run(["cmd", "/c", pathfetcher_path], capture_output=True)
print("PathFetcher Success")

print("Running FolderCreator")
# runs FolderCreator.py
folder_creator_path = code_path + "/FolderCreator.py"
folder_creator_program = run([sys.executable, folder_creator_path])
print("FolderCreator Success")

print("Running DataProcessor")
# runs DataProcessor.py
data_processor_path = code_path + "/DataProcessor.py"
data_processor_program = run([sys.executable, data_processor_path])
print("DataProcessor Success")

print("Running Cartographer")
# runs Cartographer.py
cartographer_path = code_path + "/Cartographer.py"
cartographer_program = run([sys.executable, cartographer_path])
print("Cartographer Success")

print("Running A* (No QuadTree)")
# runs A_Star.py (Without quad trees)
a_star_path = code_path + "/A_Star.py"
a_star_program = run([sys.executable, a_star_path])
print("A* (no QuadTree) Success")

show_info('Installation Success', 'Please Run Display.py')

run('deactivate', shell=True, check=True)
