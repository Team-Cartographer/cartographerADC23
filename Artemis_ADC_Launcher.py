import sys
import venv
from os import getcwd, path
from subprocess import run
from time import time

start_time = time()
print("Welcome to Team Cartographer's 2023 NASA ADC Application")
print("GitHub: https://github.com/abhi-arya1/cartographerADC23")

# Create a new virtual environment, given that there isn't one already.
venv_folder = path.join(getcwd(), 'subprocess_venv')
if not path.exists(venv_folder):

    print("Setup Initializing...")
    venv.create('subprocess_venv', with_pip=True)

    print("Installing Necessary Packages...")

    # Activate the virtual environment
    activate_script = path.join(venv_folder, 'Scripts', 'activate.bat')
    run(f'cmd /c "{activate_script}"', shell=True, check=True)

    # Install the required libraries
    run([sys.executable, '-m', 'pip', 'install', 'Pillow'], check=True)
    print("Installed package: Pillow")
    run([sys.executable, '-m', 'pip', 'install', 'numpy'], check=True)
    print("Installed package: numpy")
    run([sys.executable, '-m', 'pip', 'install', 'ursina'], check=True)
    print("Installed package: ursina")
    run([sys.executable, '-m', 'pip', 'install', 'PySimpleGUI'], check=True)
    print("Installed package: PySimpleGUI")
    run([sys.executable, '-m', 'pip', 'install', 'tqdm'], check=True)
    print("Installed package: tqdm")
    run([sys.executable, '-m', 'pip', 'install', 'msgspec'], check=True)
    print("Installed package: msgspec")
    run([sys.executable, '-m', 'pip', 'install', 'seaborn'], check=True)
    print("Installed package: seaborn")


code_path = getcwd()
# Checks Existence before running App Setup.
if not path.exists(code_path + "/Data/Images/AStar_Path.png"):
    print('Running Setup')

    print("Running FileManager First-Time Setup")
    # runs FileManager.py
    folder_creator_path = code_path + "/FileManager.py"
    folder_creator_program = run([sys.executable, folder_creator_path])
    print("FileManager Setup Success")

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

    print("Running A* Pathfinding")
    # runs A_Star.py (Without quad trees)
    a_star_path = code_path + "/A_Star.py"
    a_star_program = run([sys.executable, a_star_path])
    print("A* Pathfinding Success")

    end_time = time()

    print(f'Setup Completed in {round((end_time - start_time)/60, 2)}min')


print("Running Display")
# runs Display.py
display_path = code_path + '/Display.py'
display_program = run([sys.executable, display_path])
print('Ended Program')


run('deactivate', shell=True, check=True)
