import subprocess
import os
import sys
import platform
import datetime


def get_log_path():
    """Returns the path for the history log file."""
    base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()
    return os.path.join(base_dir, "WinOptimizer_history.log")


def write_log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"
    print(log_line.strip())
    try:
        with open(get_log_path(), "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        print(f"Failed to write log: {e}")


def _get_scripts_dir():
    """Returns the path to the scripts directory whether frozen or in dev mode."""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, "scripts")
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))


def run_script(script_name):
    """
    Runs a batch script from the scripts folder.
    Returns True if successful, False otherwise.
    """
    write_log(f"INFO: Iniciando -> {script_name}")
    script_path = os.path.join(_get_scripts_dir(), script_name)

    if not os.path.exists(script_path):
        write_log(f"ERROR: Script não encontrado: {script_path}")
        return False

    try:
        creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

        process = subprocess.Popen(
            f'"{script_path}"',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=creation_flags
        )
        stdout, stderr = process.communicate(timeout=120)

        if process.returncode == 0:
            write_log(f"SUCCESS: {script_name} executado com sucesso.")
            return True
        else:
            write_log(f"WARNING: {script_name} retornou código {process.returncode}.")
            return False

    except subprocess.TimeoutExpired:
        process.kill()
        write_log(f"ERROR: Timeout ao executar {script_name}.")
        return False
    except Exception as e:
        write_log(f"ERROR: Falha crítica ao executar {script_name}. Erro: {e}")
        return False


def run_cmd(command):
    """
    Runs a shell command (e.g. winget) in a visible console window.
    """
    write_log(f"INFO: Executando comando -> {command}")
    try:
        creation_flags = subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        process = subprocess.Popen(command, shell=True, creationflags=creation_flags)
        process.wait()

        if process.returncode == 0:
            write_log("SUCCESS: Comando executado com sucesso.")
            return True
        else:
            write_log(f"WARNING: Comando retornou código {process.returncode}.")
            return False
    except Exception as e:
        write_log(f"ERROR: Falha ao executar comando. Erro: {e}")
        return False


def get_hardware_info():
    """
    Collects rich hardware info using PowerShell.
    Reads GPU VRAM from the Windows registry to bypass the 4GB cap in Win32_VideoController.
    Returns a dict with keys: os, cpu, gpu, ram, disks, motherboard.
    """
    results = {}

    def run_ps(cmd, timeout=15):
        try:
            out = subprocess.check_output(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stderr=subprocess.DEVNULL,
                timeout=timeout
            ).decode("utf-8", errors="ignore").strip()
            lines = [l.strip() for l in out.splitlines() if l.strip()]
            return lines if lines else []
        except:
            return []

    # ── OS (reads from registry — same source as Settings > About) ────
    os_lines = run_ps(
        "$r = Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion'; "
        "$build = $r.CurrentBuildNumber; "
        "$ubr   = $r.UBR; "
        "$ver   = if ($r.DisplayVersion) { $r.DisplayVersion } else { $r.ReleaseId }; "
        "$name  = $r.ProductName; "
        "# Build >= 22000 means Windows 11 even if ProductName says Windows 10 "
        "if ([int]$build -ge 22000 -and $name -like '*10*') { $name = $name -replace 'Windows 10','Windows 11' }; "
        "\"$name  v$ver  (Build $build.$ubr)\""
    )
    results["os"] = os_lines[0] if os_lines else f"{platform.system()} {platform.release()}"

    # ── CPU ──────────────────────────────────────────────────────────
    cpu_lines = run_ps(
        "$c = Get-CimInstance Win32_Processor | Select-Object -First 1;"
        "\"$($c.Name.Trim())\" + \"  |  $($c.NumberOfCores) Cores / $($c.NumberOfLogicalProcessors) Threads\" + "
        "\"  |  $([math]::Round($c.MaxClockSpeed/1000,2)) GHz\""
    )
    results["cpu"] = cpu_lines[0] if cpu_lines else "N/A"

    # ── GPU (VRAM from registry — bypasses 4GB cap) ──────────────────
    # Win32_VideoController.AdapterRAM overflows at 4GB (32-bit field).
    # The registry key HardwareInformation.qwMemorySize holds the true 64-bit value.
    gpu_script = r"""
$gpus = Get-CimInstance Win32_VideoController | Where-Object { $_.AdapterCompatibility -ne 'Microsoft' }
$regBase = 'HKLM:\SYSTEM\ControlSet001\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}'
$results = @()
foreach ($gpu in $gpus) {
    $name = $gpu.Name.Trim()
    $vramGb = 'N/A'
    # Try registry for accurate VRAM
    Get-ChildItem $regBase -ErrorAction SilentlyContinue | ForEach-Object {
        $desc = (Get-ItemProperty $_.PSPath -ErrorAction SilentlyContinue).'DriverDesc'
        if ($desc -and $name -like "*$desc*") {
            $raw = (Get-ItemProperty $_.PSPath -ErrorAction SilentlyContinue).'HardwareInformation.qwMemorySize'
            if ($raw) { $vramGb = [math]::Round($raw/1GB,1) }
        }
    }
    if ($vramGb -eq 'N/A') { $vramGb = [math]::Round($gpu.AdapterRAM/1GB,1) }
    $results += "$name  |  $vramGb GB VRAM"
}
$results
"""
    gpu_lines = run_ps(gpu_script, timeout=20)
    results["gpu"] = "\n".join(gpu_lines) if gpu_lines else "N/A"

    # ── RAM ──────────────────────────────────────────────────────────
    ram_script = r"""
$sticks = Get-CimInstance Win32_PhysicalMemory
$total   = [math]::Round(($sticks | Measure-Object Capacity -Sum).Sum/1GB,1)
$speed   = ($sticks | Select-Object -First 1).Speed
$slots   = $sticks.Count
$typeNum = ($sticks | Select-Object -First 1).MemoryType
$type    = switch($typeNum){ 24{'DDR3'} 26{'DDR4'} 34{'DDR5'} default{"DDR($typeNum)"} }
"$total GB  $type @ $speed MHz  ($slots stick(s))"
"""
    ram_lines = run_ps(ram_script)
    results["ram"] = ram_lines[0] if ram_lines else "N/A"

    # ── DISKS (all drives, one per line) ─────────────────────────────
    disk_script = r"""
$disks = Get-PhysicalDisk | Sort-Object DeviceId
foreach ($d in $disks) {
    $sizeGb = [math]::Round($d.Size/1GB)
    $type = $d.MediaType
    if ($type -eq 'Unspecified') { $type = 'Unknown' }
    $bus  = $d.BusType
    "$($d.FriendlyName)  |  $sizeGb GB  |  $type  ($bus)"
}
"""
    disk_lines = run_ps(disk_script)
    results["disks"] = disk_lines  # list of strings, one per disk

    # ── MOTHERBOARD ──────────────────────────────────────────────────
    mb_lines = run_ps(
        "$b = Get-CimInstance Win32_BaseBoard | Select-Object -First 1; "
        "\"$($b.Manufacturer.Trim()) $($b.Product.Trim())\""
    )
    results["motherboard"] = mb_lines[0] if mb_lines else "N/A"

    return results

