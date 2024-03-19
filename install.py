import os
import subprocess
import shutil

# Ustawienia
venv_folder = "venv"
requirements_file = "requirements.txt"

# Tworzenie środowiska wirtualnego
print("Tworzenie środowiska wirtualnego...")
subprocess.run(["python", "-m", "venv", venv_folder])

# Aktywacja środowiska wirtualnego
activate_path = os.path.join(venv_folder, "Scripts", "activate")
print(f"Aktywowanie środowiska wirtualnego: {activate_path}")
subprocess.run([activate_path], shell=True)

current_folder = os.path.abspath(os.path.dirname(__file__))

# Instalacja zależności z pliku requirements.txt
requirements_path = os.path.join(current_folder, requirements_file)
print(f"Instalacja zależności z pliku {requirements_file}")
subprocess.run(["pip", "install", "-r", requirements_path])

with open('config.json', 'r', encoding='utf-8') as json_file:
    file_content = json_file.read()
file_content = file_content.replace('path-to-project', current_folder)

with open('ML_NALF_Flask.json', 'w', encoding='utf-8') as json_file:
    json_file.write(file_content)

print("Instalacja zakończona.")
