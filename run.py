import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import time
import psutil

class ScriptRunnerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Script Runner")
        self.script_path = tk.StringVar()
        self.process_pid = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Выберите скрипт .py:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.script_path, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.master, text="Обзор", command=self.browse_script).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(self.master, text="Запустить", command=self.run_script).grid(row=1, column=0, columnspan=3, pady=10)

        # Запуск потока для мониторинга скрипта
        self.monitor_thread = threading.Thread(target=self.monitor_script)
        self.monitor_thread.daemon = True  # Поток будет завершен, когда основная программа закроется
        self.monitor_thread.start()

    def browse_script(self):
        script_path = filedialog.askopenfilename(filetypes=[("Python Scripts", "*.py")])
        if script_path:
            self.script_path.set(script_path)

    def run_script(self):
        script_path = self.script_path.get()
        if script_path:
            process = subprocess.Popen(["python", script_path], cwd=os.path.dirname(script_path))
            self.process_pid = process.pid
        else:
            messagebox.showinfo("Ошибка", "Выберите скрипт перед запуском!")

    def monitor_script(self):
        while True:
            script_path = self.script_path.get()
            if script_path:
                if self.process_pid:
                    try:
                        process = psutil.Process(self.process_pid)
                        script_running = any("python" in cmdline for cmdline in process.cmdline())
                    except psutil.NoSuchProcess:
                        script_running = False

                    if not script_running:
                        self.run_script()

                time.sleep(10)

if __name__ == "__run__":
    root = tk.Tk()
    app = ScriptRunnerApp(root)
    root.mainloop()