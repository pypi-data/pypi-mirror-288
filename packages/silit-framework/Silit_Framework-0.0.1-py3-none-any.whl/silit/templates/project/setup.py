from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but some modules need help.
build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter"],
}

# Base option
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this for GUI applications

setup(
    name="MyFramework",
    version="0.1",
    description="My Desktop Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("silit.py", base=base)],
)
