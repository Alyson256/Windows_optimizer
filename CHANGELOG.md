# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] — 2026-05-05

### Added
- `12_system_cleanup.bat` — New script to safely clear DNS cache, user/system temp folders, Windows Update cache, and Recycle Bin
- `docs/pt-BR.md` — Full Portuguese translation mirroring the English README
- `docs/RISKS_pt-BR.md` — Full Portuguese translation of the risks documentation
- `docs/TIPS_pt-BR.md` — Full Portuguese translation of the installation tips

### Changed
- `docs/RISKS.md` — Updated to include risk analysis for `11_remove_bloatware` and `12_system_cleanup`
- `README.md` — Added `12_system_cleanup.bat` to the scripts table and file tree
- `00_run_all.bat` — Included the new system cleanup step at the end of the sequence

---

## [1.0.0] — 2026-05-02

### Added
- `00_run_all.bat` — Master launcher with auto-elevation and per-step confirmation
- `01_restore_point.bat` — System restore point creation via PowerShell
- `02_services_manual.bat` — 16 non-essential services set to Manual start
- `03_disable_recall.bat` — Windows Recall disable via Group Policy keys
- `04_disable_telemetry.bat` — Telemetry level 0, DiagTrack disabled, CEIP tasks disabled
- `05_power_plan.bat` — High Performance plan + Fast Startup disable
- `06_visual_tweaks.bat` — Animation/transparency disable, ClearType preserved
- `07_network_tweaks.bat` — Nagle off, TCP tuning, DNS cache, network throttling
- `08_privacy_tweaks.bat` — Advertising ID, location, activity history, Cortana
- `09_startup_cleanup.bat` — Read-only startup registry audit
- `10_undo_all.bat` — Full revert of all changes to Windows defaults
- `tools/check_status.bat` — Read-only diagnostic status audit
- `_lib/` — Shared utilities: colors, logger, admin check
- `docs/RISKS.md` — Technical risk documentation per script
- `docs/pt-BR.md` — Portuguese documentation
