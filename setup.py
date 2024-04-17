# Setup build file for compile .py to .exe
from cx_Freeze import setup, Executable


build_exe_options = {
    "packages": ["PIL", "mediapipe", "cv2"],
    "include_files": ["drawing_app/", "ressources/", "menu_fct.py"],
}

setup(
    name = "DrawItium",
    version = "0.1",
    description = "Application allowing you to draw with your fingers using AI recognition.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("menu.py", base="Win32GUI", icon="./ressources/drawitium_logo.ico")]
)

# Run "python setup.py build" to have the .exe for the app