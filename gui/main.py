import sys
import os
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    # Ensure the app runs as Administrator to prevent script permission issues and ugly popups
    if not is_admin():
        # Relaunch the script with admin rights
        # sys.argv provides the arguments passed to the original script
        script_path = os.path.abspath(sys.argv[0])
        # If frozen (PyInstaller), sys.executable is the .exe itself
        executable = sys.executable if getattr(sys, 'frozen', False) else sys.executable
        args = f'"{script_path}"' if not getattr(sys, 'frozen', False) else ""
        
        ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, args, None, 1)
        sys.exit()

    # Add gui to sys.path so we can import core and ui easily
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ui.app import WinOptimizerApp

    app = WinOptimizerApp()
    app.mainloop()
