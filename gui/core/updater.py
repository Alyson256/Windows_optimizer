import requests
import threading
import os
import sys
import tempfile
import subprocess

GITHUB_REPO = "Alyson256/Windows_optimization"
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
RELEASES_URL = f"https://github.com/{GITHUB_REPO}/releases/latest"


def check_for_updates(current_version, callback):
    """
    Checks GitHub API for the latest release in a separate thread.
    callback(has_update, latest_version, url, asset_url) will be called on the main thread.
    asset_url is the direct download link for the .exe asset if available.
    """
    def run_check():
        try:
            response = requests.get(API_URL, timeout=8)

            if response.status_code == 404:
                # No releases exist yet on GitHub - treat as up to date
                callback(False, current_version, None, None)
                return

            if response.status_code != 200:
                callback(None, None, None, None)
                return

            data = response.json()
            raw_tag = data.get("tag_name", "0.0.0")
            
            # Robust version extraction: find first sequence of digits and dots
            # Handles tags like: v2.0, V2.0Upgrade, release-2.1, 2.0.0
            import re
            version_match = re.search(r'(\d+[\.\d]*)', raw_tag)
            latest_version = version_match.group(1) if version_match else "0.0.0"
            curr_v = current_version.strip().lstrip("vV")


            def parse_version(v):
                try:
                    return [int(x) for x in v.split('.') if x.isdigit()]
                except:
                    return [0]

            # Find the .exe asset in the release
            asset_url = None
            assets = data.get("assets", [])
            for asset in assets:
                name = asset.get("name", "").lower()
                if name.endswith(".exe"):
                    asset_url = asset.get("browser_download_url")
                    break

            if parse_version(latest_version) > parse_version(curr_v):
                callback(True, latest_version, RELEASES_URL, asset_url)
            else:
                callback(False, latest_version, None, None)

        except Exception as e:
            print(f"Error checking updates: {e}")
            callback(None, None, None, None)

    thread = threading.Thread(target=run_check, daemon=True)
    thread.start()


def download_and_replace(asset_url, progress_callback, done_callback):
    """
    Downloads the new .exe from GitHub asset URL.
    Uses a helper launcher script to replace the running .exe after we exit.
    progress_callback(percent: int) is called during download.
    done_callback(success: bool, tmp_path: str) is called when done.
    """
    def run_download():
        try:
            response = requests.get(asset_url, stream=True, timeout=30)
            total = int(response.headers.get("content-length", 0))
            downloaded = 0

            # Save to a temp file next to the current executable
            suffix = ".exe" if sys.platform == "win32" else ""
            tmp_path = os.path.join(tempfile.gettempdir(), f"WinOptimizer_update{suffix}")

            with open(tmp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            pct = int((downloaded / total) * 100)
                            progress_callback(pct)

            done_callback(True, tmp_path)
        except Exception as e:
            print(f"Download error: {e}")
            done_callback(False, "")

    threading.Thread(target=run_download, daemon=True).start()


def apply_update(new_exe_path):
    """
    Creates a tiny batch script to replace the current .exe after we exit,
    then relaunches the new version.
    Only works when compiled (frozen). Falls back to opening releases page in dev mode.
    """
    if not getattr(sys, 'frozen', False):
        # In dev mode, just open the releases page
        import webbrowser
        webbrowser.open_new_tab(RELEASES_URL)
        return

    current_exe = sys.executable
    updater_bat = os.path.join(tempfile.gettempdir(), "win_optimizer_updater.bat")

    bat_content = f"""@echo off
ping -n 3 127.0.0.1 >nul
copy /Y "{new_exe_path}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
"""
    with open(updater_bat, "w") as f:
        f.write(bat_content)

    # Launch the updater script and exit
    subprocess.Popen(["cmd.exe", "/c", updater_bat], close_fds=True)
    sys.exit(0)
