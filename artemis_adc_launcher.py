import sys
import venv
from os import getcwd, path
from subprocess import run
from time import time

# welcome print statements
print("Welcome to Team Cartographer's 2023 NASA ADC Application")
print("GitHub: https://github.com/abhi-arya1/cartographerADC23")


# Create a new virtual environment, given that there isn't one already.
venv_folder = path.join(getcwd(), "subprocess_venv")
if not path.exists(venv_folder):

    start = time()

    print("Creating virtual environment")
    venv.create("subprocess_venv", with_pip=True)

    print("Installing dependencies...")

    # Add pip installation names here for any new package.
    packages = ["Pillow", "numpy", "ursina", "PySimpleGUI", "orjson", "seaborn"]
    for package in packages:
        run([sys.executable, "-m", "pip", "install", package], check=True)
        print(f"Installed package: {package}")

    print(f"Venv creation completed in {round(time()-start, 2)}s")


print("\nRunning application")

# runs site_manager.py
program_path = getcwd() + "/site_manager.py"
program = run([sys.executable, program_path])

print("\nDeactivating")
