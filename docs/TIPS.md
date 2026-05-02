# 💡 Installation & Setup Tips

Best practices for a clean Windows 11 installation — before running any optimizer scripts.

---

## 🔌 Install Windows Without Internet (Most Important Tip)

When Windows 11 setup asks you to connect to Wi-Fi or Ethernet — **don't**.

**Why it matters:**
- Connecting during setup forces you to sign in with a **Microsoft account** (no local account option on Home edition)
- Windows downloads and installs **additional bloatware** tied to your Microsoft account
- It enables **activity syncing**, advertising ID, and Cortana from the first boot

**How to bypass on Windows 11:**

**Method 1 — No cable:** Simply don't plug in the network cable / don't connect to Wi-Fi during setup.

**Method 2 — If Wi-Fi/Ethernet is auto-detected:**
```
On the "Let's connect you to a network" screen:
  Press Shift + F10  →  opens a command prompt
  Type: OOBE\BYPASSNRO
  Press Enter  →  the PC reboots and offers "I don't have internet"
```

**Method 3 — On newer builds (24H2+):**
```
On the network screen:
  Press Shift + F10
  Type: start ms-cxh:localonly
  Press Enter
```

> After setup is complete, you can connect to the internet normally and run these scripts.

---

## 🏠 Create a Local Account

During offline setup, Windows will let you create a local account.  
Keep your username **short, no spaces, no accents** — it becomes your `C:\Users\username` folder.

---

## 🔄 Defer Windows Updates (First Boot)

Before connecting to the internet for the first time:

1. Go to **Settings → Windows Update → Advanced Options**
2. Set **"Pause updates"** for 1-5 weeks
3. Then connect and let **only drivers** install first
4. Run these optimizer scripts
5. Then un-pause updates

This prevents Windows from installing unwanted "recommended" apps during the first update cycle.

---

## 🧹 Skip / Deny Everything During OOBE

On the post-install "Let's customize your experience" screens, always choose:

| Screen | Recommended choice |
|--------|-------------------|
| Diagnostic data | **Required only** (minimum) |
| Inking & typing | **No** |
| Tailored experiences | **No** |
| Find my device | **No** (unless needed) |
| Location | **No** |
| Advertising ID | **No** |

---

## 🖥️ Driver Installation Order

After your first boot, install drivers in this order to avoid conflicts:

1. **Chipset** (AMD or Intel — from manufacturer's site, not Windows Update)
2. **GPU** (NVIDIA/AMD/Intel — from their official site, not GeForce Experience)
3. **Audio** (Realtek, etc.)
4. **Network** (if needed)
5. Everything else

> **Avoid GeForce Experience / AMD Software "full install"** — they add significant background processes.  
> Install the **bare GPU driver only** using the "Custom → Clean install" option.

---

## 🛡️ Windows Defender Recommendations

- Keep Windows Defender **enabled** — it's lightweight and effective on a clean install
- Disable **"Send samples automatically"** in Defender settings
- The telemetry scripts in this repo do NOT touch Defender

---

## 📦 Recommended First Apps (Post-Install)

| Category | Recommendation | Why |
|----------|---------------|-----|
| Browser | [Firefox](https://firefox.com) / [Brave](https://brave.com) | Less telemetry than Edge |
| Package manager | [winget](https://learn.microsoft.com/en-us/windows/package-manager/) | Built-in, no install needed |
| GPU drivers | Direct from [nvidia.com](https://nvidia.com) / [amd.com](https://amd.com) | Skip the bloated launchers |
| 7-Zip | `winget install 7zip.7zip` | Free, no ads |
| VLC | `winget install VideoLAN.VLC` | Replaces Movies & TV |

---

## ⚡ Quick winget Install (after running this repo's scripts)

```powershell
# Run in PowerShell as Administrator
winget install 7zip.7zip VideoLAN.VLC Mozilla.Firefox --accept-source-agreements --accept-package-agreements
```
