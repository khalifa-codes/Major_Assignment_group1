"""
Main Window for CPU Scheduling Simulator GUI
--------------------------------------------
This module provides the main menu window with navigation buttons.
"""

import tkinter as tk
from tkinter import ttk, font
from .scheduler_ui import SchedulerUI, DeadlockUI


class MainWindow:
    """Main menu window with algorithm selection buttons."""
    
    def _init_(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2e")
        
        # Configure style
        self.setup_styles()
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_font = font.Font(family="Arial", size=32, weight="bold")
        title_label = tk.Label(
            self.main_frame,
            text="CPU Scheduling Simulator",
            font=title_font,
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        title_label.pack(pady=(20, 40))
        
        # Subtitle
        subtitle_font = font.Font(family="Arial", size=14)
        subtitle_label = tk.Label(
            self.main_frame,
            text="Select an algorithm to simulate",
            font=subtitle_font,
            bg="#1e1e2e",
            fg="#bac2de"
        )
        subtitle_label.pack(pady=(0, 50))
        
        # Buttons container
        buttons_frame = tk.Frame(self.main_frame, bg="#1e1e2e")
        buttons_frame.pack(expand=True)
        
        # Button configurations
        button_configs = [
            {
                "text": "FCFS\n(First Come First Serve)",
                "command": lambda: self.open_scheduler("FCFS"),
                "color": "#89b4fa"
            },
            {
                "text": "SJF\n(Shortest Job First)",
                "command": lambda: self.open_scheduler("SJF"),
                "color": "#a6e3a1"
            },
            {
                "text": "RR\n(Round Robin)",
                "command": lambda: self.open_scheduler("RR"),
                "color": "#f9e2af"
            },
            {
                "text": "DL\n(Deadlock Prevention)",
                "command": self.open_deadlock,
                "color": "#f38ba8"
            }
        ]
        
        # Create buttons in a 2x2 grid
        for i, config in enumerate(button_configs):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                buttons_frame,
                text=config["text"],
                font=font.Font(family="Arial", size=16, weight="bold"),
                bg=config["color"],
                fg="#1e1e2e",
                activebackground=config["color"],
                activeforeground="#1e1e2e",
                relief=tk.FLAT,
                cursor="hand2",
                padx=30,
                pady=25,
                command=config["command"],
                borderwidth=0,
                highlightthickness=0
            )
            btn.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=config["color"]: self.on_enter(e, b, c))
            btn.bind("<Leave>", lambda e, b=btn, c=config["color"]: self.on_leave(e, b, c))
        
        # Configure grid weights
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_rowconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(1, weight=1)
        
        # Footer
        footer_label = tk.Label(
            self.main_frame,
            text="© CPU Scheduling Simulator 2024",
            font=font.Font(family="Arial", size=10),
            bg="#1e1e2e",
            fg="#6c7086"
        )
        footer_label.pack(side=tk.BOTTOM, pady=20)
    
    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=10)
    
    def on_enter(self, event, button, color):
        """Button hover enter effect."""
        button.configure(bg=self.lighten_color(color))
    
    def on_leave(self, event, button, color):
        """Button hover leave effect."""
        button.configure(bg=color)
    
    def lighten_color(self, color):
        """Lighten a hex color."""
        # Simple lightening by increasing RGB values
        color_map = {
            "#89b4fa": "#a5c9ff",
            "#a6e3a1": "#b8f0b3",
            "#f9e2af": "#ffebc4",
            "#f38ba8": "#ffa0bc"
        }
        return color_map.get(color, color)
    
    def open_scheduler(self, algorithm):
        """Open scheduler UI for the selected algorithm."""
        # Clear main window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create scheduler UI
        scheduler = SchedulerUI(self.root, algorithm, self.show_main_menu)
        scheduler.pack(fill=tk.BOTH, expand=True)
    
    def open_deadlock(self):
        """Open deadlock prevention UI."""
        # Clear main window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create deadlock UI
        deadlock = DeadlockUI(self.root, self.show_main_menu)
        deadlock.pack(fill=tk.BOTH, expand=True)
    
    def show_main_menu(self):
        """Return to main menu."""
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Recreate main window
        self._init_(self.root)


def main():
    """Entry point for GUI application."""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if _name_ == "_main_":
    main()