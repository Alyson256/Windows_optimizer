import customtkinter as ctk
import webbrowser
import os
import platform
import threading
import subprocess
import tkinter.messagebox as messagebox
from core.i18n import I18n
from core.runner import run_script, run_cmd, get_log_path, get_hardware_info
from core.updater import check_for_updates, download_and_replace, apply_update

CURRENT_VERSION = "2.0"

# Set default appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ToolTip:
    def __init__(self, widget, text_callback):
        self.widget = widget
        self.text_callback = text_callback
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window:
            return
        text = self.text_callback()
        if not text:
            return
            
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        tw.attributes("-topmost", True)
        
        label = ctk.CTkLabel(tw, text=text, justify="left", fg_color=("gray80", "gray20"), corner_radius=6, padx=10, pady=5)
        label.pack()

    def hide_tooltip(self, event=None):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()

class WinOptimizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.i18n = I18n(lang="pt")
        
        self.title(self.i18n.get("app_title"))
        self.geometry("750x800")
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Try to load icon if it exists
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except:
                pass
        
        self.toggles = {}
        self.app_toggles = {}
        self.info_labels = {}
        self.latest_update_url = None
        self.latest_asset_url = None  # Direct .exe download URL from GitHub assets
        
        self.build_header()
        self.build_tabs()
        self.build_footer()
        
        self.update_texts()
        self.auto_check_updates()

    def build_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=30, pady=(25, 15), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text=self.i18n.get("app_title"), font=ctk.CTkFont(size=26, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="w")
        
        self.lang_var = ctk.StringVar(value="Português")
        self.lang_menu = ctk.CTkOptionMenu(self.header_frame, values=["Português", "English"], 
                                           command=self.change_language, variable=self.lang_var, width=110)
        self.lang_menu.grid(row=0, column=1, padx=(0, 10))
        
        self.theme_var = ctk.StringVar(value=self.i18n.get("system"))
        self.theme_menu = ctk.CTkOptionMenu(self.header_frame, values=["Claro", "Escuro", "Sistema"], 
                                            command=self.change_theme, variable=self.theme_var, width=100)
        self.theme_menu.grid(row=0, column=2)
        
        # Update Row
        self.update_btn = ctk.CTkButton(self.header_frame, text=self.i18n.get("check_updates"), 
                                        command=self.manual_check_updates, width=120, fg_color="transparent", border_width=1, text_color=("gray10", "gray90"))
        self.update_btn.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        self.history_btn = ctk.CTkButton(self.header_frame, text=self.i18n.get("view_history"), 
                                        command=self.open_history, width=120, fg_color="transparent", border_width=1, text_color=("gray10", "gray90"))
        self.history_btn.grid(row=1, column=2, sticky="e", pady=(15, 0))

    def build_tabs(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=30, pady=5, sticky="nsew")
        
        self.tab_names = ["tab_presets", "tab_performance", "tab_privacy", "tab_network", "tab_cleanup", "tab_apps", "tab_hardware"]
        self.tabs = {}
        
        for t in self.tab_names:
            self.tabs[t] = self.tabview.add(t)
            self.tabs[t].grid_columnconfigure(0, weight=1)
            
        self.build_presets_tab()
        
        self.script_categories = {
            "tab_performance": ["02_services_manual", "05_power_plan", "06_visual_tweaks"],
            "tab_privacy": ["03_disable_recall", "04_disable_telemetry", "08_privacy_tweaks"],
            "tab_network": ["07_network_tweaks"],
            "tab_cleanup": ["11_remove_bloatware", "12_system_cleanup"]
        }
        
        for tab_key, scripts in self.script_categories.items():
            self.build_script_list(self.tabs[tab_key], scripts)
            
        self.build_apps_tab()
        self.build_hardware_tab()

    def build_presets_tab(self):
        tab = self.tabs["tab_presets"]
        
        # Welcome Section
        self.welcome_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.welcome_frame.grid(row=0, column=0, padx=20, pady=(20, 25), sticky="ew")
        
        self.welcome_title = ctk.CTkLabel(self.welcome_frame, text="", font=ctk.CTkFont(size=22, weight="bold"), text_color=("blue", "cyan"))
        self.welcome_title.pack(anchor="w", pady=(0, 10))
        
        self.welcome_desc = ctk.CTkLabel(self.welcome_frame, text="", justify="left", wraplength=600, font=ctk.CTkFont(size=14))
        self.welcome_desc.pack(anchor="w")
        
        # Recommended Preset Card
        self.rec_frame = ctk.CTkFrame(tab, fg_color=("gray90", "gray15"), corner_radius=10)
        self.rec_frame.grid(row=1, column=0, padx=20, pady=15, sticky="ew")
        self.rec_frame.grid_columnconfigure(0, weight=1)
        
        self.rec_title = ctk.CTkLabel(self.rec_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.rec_title.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        
        self.rec_desc = ctk.CTkLabel(self.rec_frame, text="", justify="left", wraplength=450)
        self.rec_desc.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")
        
        self.rec_btn = ctk.CTkButton(self.rec_frame, text="Run", command=self.run_preset_recommended, width=120, height=36)
        self.rec_btn.grid(row=0, column=1, rowspan=2, padx=20)
        
        # Cleanup Preset Card
        self.clean_frame = ctk.CTkFrame(tab, fg_color=("gray90", "gray15"), corner_radius=10)
        self.clean_frame.grid(row=2, column=0, padx=20, pady=15, sticky="ew")
        self.clean_frame.grid_columnconfigure(0, weight=1)
        
        self.clean_title = ctk.CTkLabel(self.clean_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.clean_title.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        
        self.clean_desc = ctk.CTkLabel(self.clean_frame, text="", justify="left", wraplength=450)
        self.clean_desc.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")
        
        self.clean_btn = ctk.CTkButton(self.clean_frame, text="Run", command=self.run_preset_cleanup, width=120, height=36, fg_color="#D97706", hover_color="#B45309")
        self.clean_btn.grid(row=0, column=1, rowspan=2, padx=20)

    def build_script_list(self, parent_tab, scripts):
        for i, script_key in enumerate(scripts):
            row_frame = ctk.CTkFrame(parent_tab, fg_color="transparent")
            row_frame.grid(row=i, column=0, pady=10, padx=10, sticky="ew")
            row_frame.grid_columnconfigure(0, weight=1)
            
            switch_var = ctk.StringVar(value="off")
            switch = ctk.CTkSwitch(row_frame, text="", variable=switch_var, onvalue="on", offvalue="off", font=ctk.CTkFont(size=14))
            switch.grid(row=0, column=0, sticky="w")
            
            self.toggles[f"{script_key}.bat"] = (switch, switch_var, script_key)
            
            info_label = ctk.CTkLabel(row_frame, text="[ ? ]", text_color=("blue", "cyan"), cursor="hand2")
            info_label.grid(row=0, column=1, padx=10, sticky="e")
            self.info_labels[script_key] = info_label
            
            ToolTip(info_label, lambda k=script_key: self.i18n.get(f"scripts.{k}.desc", ""))
            
    def build_apps_tab(self):
        tab = self.tabs["tab_apps"]
        
        self.apps_to_install = [
            "Google.Chrome", "Brave.Brave", "Mozilla.Firefox", 
            "7zip.7zip", "VideoLAN.VLC", "Notepad++.Notepad++"
        ]
        
        for i, app_id in enumerate(self.apps_to_install):
            row_frame = ctk.CTkFrame(tab, fg_color="transparent")
            row_frame.grid(row=i, column=0, pady=10, padx=20, sticky="ew")
            row_frame.grid_columnconfigure(0, weight=1)
            
            check_var = ctk.StringVar(value="off")
            checkbox = ctk.CTkCheckBox(row_frame, text="", variable=check_var, onvalue="on", offvalue="off", font=ctk.CTkFont(size=14))
            checkbox.grid(row=0, column=0, sticky="w")
            
            self.app_toggles[app_id] = (checkbox, check_var)
            
        self.install_apps_btn = ctk.CTkButton(tab, text="Instalar", command=self.run_install_apps, height=40, width=200)
        self.install_apps_btn.grid(row=len(self.apps_to_install), column=0, pady=30)

    def build_hardware_tab(self):
        tab = self.tabs["tab_hardware"]
        
        # Scrollable frame so it works even with many disks
        self.hw_scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self.hw_scroll.pack(padx=10, pady=10, fill="both", expand=True)
        self.hw_scroll.grid_columnconfigure(1, weight=1)
        
        # Static rows that are always present
        self.hw_static_keys = ["hw_os", "hw_cpu", "hw_gpu", "hw_ram", "hw_motherboard"]
        self.hw_labels = {}
        
        for i, key in enumerate(self.hw_static_keys):
            lbl_title = ctk.CTkLabel(self.hw_scroll, text=self.i18n.get(key),
                                     font=ctk.CTkFont(size=13, weight="bold"), anchor="e")
            lbl_title.grid(row=i*2, column=0, padx=(10, 15), pady=(12, 2), sticky="e")
            
            lbl_val = ctk.CTkLabel(self.hw_scroll, text=self.i18n.get("hw_loading"),
                                   font=ctk.CTkFont(size=13), anchor="w", justify="left", wraplength=440)
            lbl_val.grid(row=i*2, column=1, padx=(0, 10), pady=(12, 2), sticky="ew")
            
            sep = ctk.CTkFrame(self.hw_scroll, height=1, fg_color=("gray75", "gray30"))
            sep.grid(row=i*2+1, column=0, columnspan=2, sticky="ew", padx=10)
            
            self.hw_labels[key] = lbl_val
        
        # Placeholder row for disks (will be built dynamically)
        self.hw_disk_start_row = len(self.hw_static_keys) * 2
        self.hw_disk_title = ctk.CTkLabel(self.hw_scroll, text=self.i18n.get("hw_disk"),
                                           font=ctk.CTkFont(size=13, weight="bold"), anchor="ne")
        self.hw_disk_title.grid(row=self.hw_disk_start_row, column=0, padx=(10, 15), pady=(12, 2), sticky="ne")
        self.hw_disk_values_frame = ctk.CTkFrame(self.hw_scroll, fg_color="transparent")
        self.hw_disk_values_frame.grid(row=self.hw_disk_start_row, column=1, padx=(0, 10), pady=(12, 2), sticky="ew")
        self.hw_disk_loading = ctk.CTkLabel(self.hw_disk_values_frame, text=self.i18n.get("hw_loading"),
                                             font=ctk.CTkFont(size=13), anchor="w")
        self.hw_disk_loading.pack(anchor="w")
        
        # Run fetch in background so UI doesn't freeze
        threading.Thread(target=self._fetch_hardware_background, daemon=True).start()

    def _fetch_hardware_background(self):
        info = get_hardware_info()
        self.after(0, lambda: self._apply_hardware_ui(info))

    def _apply_hardware_ui(self, info):
        # Update static rows
        mapping = {
            "hw_os":          info.get("os", "N/A"),
            "hw_cpu":         info.get("cpu", "N/A"),
            "hw_gpu":         info.get("gpu", "N/A"),
            "hw_ram":         info.get("ram", "N/A"),
            "hw_motherboard": info.get("motherboard", "N/A"),
        }
        for key, val in mapping.items():
            if key in self.hw_labels:
                self.hw_labels[key].configure(text=val)
        
        # Update disk rows dynamically
        for widget in self.hw_disk_values_frame.winfo_children():
            widget.destroy()
        
        disks = info.get("disks", [])
        if disks:
            for i, disk_str in enumerate(disks):
                # Icon based on type
                icon = "💿" if "SSD" in disk_str or "NVMe" in disk_str else "🖴"
                lbl = ctk.CTkLabel(self.hw_disk_values_frame,
                                   text=f"{icon} {disk_str}",
                                   font=ctk.CTkFont(size=13), anchor="w")
                lbl.pack(anchor="w", pady=(0, 4))
        else:
            ctk.CTkLabel(self.hw_disk_values_frame, text="N/A",
                         font=ctk.CTkFont(size=13)).pack(anchor="w")


    def build_footer(self):
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, padx=30, pady=(15, 30), sticky="ew")
        self.footer_frame.grid_columnconfigure(0, weight=1)
        
        # Grouped buttons on the left
        btn_group = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        btn_group.grid(row=0, column=0, sticky="w")
        
        self.run_btn = ctk.CTkButton(btn_group, text="Otimizar", command=self.run_selected_toggles, height=40, width=160)
        self.run_btn.pack(side="left", padx=(0, 10))
        
        self.undo_btn = ctk.CTkButton(btn_group, text="Desfazer", command=self.undo_all, fg_color="transparent", border_width=2, text_color=("black", "white"), height=40, width=120)
        self.undo_btn.pack(side="left")
        
        self.dev_label = ctk.CTkLabel(self.footer_frame, text="Desenvolvido por Alyson256", text_color=("blue", "cyan"), cursor="hand2", font=ctk.CTkFont(size=13))
        self.dev_label.grid(row=0, column=2, sticky="e")
        self.dev_label.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://github.com/Alyson256"))

    def update_texts(self):
        self.title(self.i18n.get("app_title"))
        self.title_label.configure(text=self.i18n.get("app_title"))
        
        self.welcome_title.configure(text=self.i18n.get("welcome_title"))
        self.welcome_desc.configure(text=self.i18n.get("welcome_desc"))
        
        self.lang_menu.configure(values=["Português", "English"])
        
        theme_vals = [self.i18n.get("light"), self.i18n.get("dark"), self.i18n.get("system")]
        self.theme_menu.configure(values=theme_vals)
        
        for tab_key in self.tab_names:
            translated_name = self.i18n.get(tab_key)
            try:
                self.tabview._segmented_button._buttons_dict[tab_key].configure(text=translated_name)
            except:
                pass
        
        self.rec_title.configure(text=self.i18n.get("preset_recommended"))
        self.rec_desc.configure(text=self.i18n.get("preset_recommended_desc"))
        self.rec_btn.configure(text="Run")
        
        self.clean_title.configure(text=self.i18n.get("preset_cleanup"))
        self.clean_desc.configure(text=self.i18n.get("preset_cleanup_desc"))
        self.clean_btn.configure(text="Run")

        for script_file, (switch, _, script_key) in self.toggles.items():
            name = self.i18n.get(f"scripts.{script_key}.name", script_key)
            switch.configure(text=name)
            
        for app_id, (checkbox, _) in self.app_toggles.items():
            name = self.i18n.get(f"apps.{app_id}", app_id)
            checkbox.configure(text=name)
            
        if hasattr(self, 'hw_labels'):
            for key in self.hw_labels:
                pass  # title labels are static; we only re-translate the disk title separately
        if hasattr(self, 'hw_disk_title'):
            self.hw_disk_title.configure(text=self.i18n.get("hw_disk"))
            
        self.run_btn.configure(text=self.i18n.get("run_selected"))
        self.undo_btn.configure(text=self.i18n.get("undo_all"))
        self.install_apps_btn.configure(text=self.i18n.get("install_selected"))
        self.dev_label.configure(text=f"{self.i18n.get('developed_by')}Alyson256")
        
        if not self.latest_update_url:
            self.update_btn.configure(text=self.i18n.get("check_updates"))
            
        self.history_btn.configure(text=self.i18n.get("view_history"))

    def change_language(self, choice):
        lang_code = "pt" if choice == "Português" else "en"
        self.i18n.load_language(lang_code)
        self.update_texts()

    def change_theme(self, choice):
        if choice == self.i18n.get("light"):
            ctk.set_appearance_mode("Light")
        elif choice == self.i18n.get("dark"):
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("System")

    def confirm_action(self, msg_key):
        title = self.i18n.get("confirm_title")
        msg = self.i18n.get(msg_key)
        return messagebox.askyesno(title, msg)

    def run_preset_recommended(self):
        if not self.confirm_action("confirm_preset"): return
        print("Running Recommended Preset...")
        run_script("02_services_manual.bat")
        run_script("04_disable_telemetry.bat")
        run_script("06_visual_tweaks.bat")
        run_script("08_privacy_tweaks.bat")
        print("Preset Done!")

    def run_preset_cleanup(self):
        if not self.confirm_action("confirm_preset"): return
        print("Running Cleanup Preset...")
        run_script("12_system_cleanup.bat")
        print("Cleanup Done!")

    def run_selected_toggles(self):
        if not self.confirm_action("confirm_run"): return
        for script_file, (_, var, _) in self.toggles.items():
            if var.get() == "on":
                print(f"Running {script_file}...")
                run_script(script_file)
        print("Done!")

    def run_install_apps(self):
        if not self.confirm_action("confirm_apps"): return
        to_install = []
        for app_id, (_, var) in self.app_toggles.items():
            if var.get() == "on":
                to_install.append(app_id)
                
        if not to_install: return
        
        apps_str = " ".join(to_install)
        # We launch winget in a visible command prompt so the user sees progress bars
        cmd = f'start cmd /c "winget install {apps_str} --accept-source-agreements --accept-package-agreements && pause"'
        run_cmd(cmd)

    def undo_all(self):
        if not self.confirm_action("confirm_undo"): return
        print("Running 10_undo_all.bat...")
        run_script("10_undo_all.bat")
        print("Undo complete!")
        
    def open_history(self):
        log_path = get_log_path()
        if os.path.exists(log_path):
            os.startfile(log_path)
        else:
            messagebox.showinfo("Histórico", "O arquivo de log ainda não existe. Nenhuma ação foi registrada.")

    def auto_check_updates(self):
        self.update_btn.configure(state="disabled", text=self.i18n.get("checking"))
        check_for_updates(CURRENT_VERSION, self._on_update_checked)
        
    def manual_check_updates(self):
        """Called when user clicks the update button."""
        if self.latest_asset_url:
            # Asset available: start download flow
            self._start_download()
        elif self.latest_update_url:
            # No direct asset, open releases page in browser as fallback
            webbrowser.open_new_tab(self.latest_update_url)
        else:
            # Re-check
            self.auto_check_updates()
            
    def _on_update_checked(self, has_update, latest_version, url, asset_url):
        self.after(0, lambda: self._apply_update_ui(has_update, latest_version, url, asset_url))
        
    def _apply_update_ui(self, has_update, latest_version, url, asset_url):
        self.update_btn.configure(state="normal")
        if has_update is True:
            self.latest_update_url = url
            self.latest_asset_url = asset_url
            version_text = self.i18n.get("update_available").replace("{v}", f"v{latest_version}")
            if asset_url:
                # Show download button
                btn_text = f"{version_text}  —  {self.i18n.get('update_download')}"
            else:
                btn_text = version_text
            self.update_btn.configure(text=btn_text, fg_color="#10B981", text_color="white", border_width=0)
        elif has_update is False:
            self.update_btn.configure(text=self.i18n.get("up_to_date"), fg_color="transparent")
        else:
            self.update_btn.configure(text=self.i18n.get("update_error"), fg_color="transparent")
            
    def _start_download(self):
        """Starts downloading the update in background and shows progress."""
        self.update_btn.configure(state="disabled", fg_color="#2563EB", text=self.i18n.get("update_downloading").replace("{pct}", "0"))
        
        def on_progress(pct):
            self.after(0, lambda p=pct: self.update_btn.configure(
                text=self.i18n.get("update_downloading").replace("{pct}", str(p))
            ))
            
        def on_done(success, tmp_path):
            self.after(0, lambda: self._on_download_done(success, tmp_path))
            
        download_and_replace(self.latest_asset_url, on_progress, on_done)
        
    def _on_download_done(self, success, tmp_path):
        if not success:
            self.update_btn.configure(state="normal", text=self.i18n.get("update_error"), fg_color="transparent")
            return
        
        # Ask user to apply and restart
        confirmed = messagebox.askyesno(
            self.i18n.get("update_restart_title"),
            self.i18n.get("update_restart_msg")
        )
        if confirmed:
            apply_update(tmp_path)
        else:
            self.update_btn.configure(state="normal", text=self.i18n.get("update_download"), fg_color="#10B981")
