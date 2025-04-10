import tkinter as tk
from tkinter import ttk
import subprocess
import os

class ScriptLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Launcher")
        self.root.geometry("400x300")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = ttk.Label(main_frame, text="Select a script to run:", font=('Helvetica', 12, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create buttons for each script
        scripts = [
            ("Reviews Determiner", "ReviewDeter.py"),
            ("Target Review", "TargetReview.py"),
            ("Hotels Scraper", "hotels_scraper_gui.py")
        ]
        
        for button_text, script_name in scripts:
            btn = ttk.Button(
                main_frame, 
                text=button_text,
                command=lambda s=script_name: self.run_script(s)
            )
            btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Exit button
        exit_btn = ttk.Button(main_frame, text="Exit", command=root.destroy)
        exit_btn.pack(pady=(20, 0), padx=20, fill=tk.X)

    def run_script(self, script_name):
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        try:
            subprocess.Popen(['python', script_path])
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to run {script_name}: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScriptLauncher(root)
    root.mainloop()
