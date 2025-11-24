"""
Scheduler UI for CPU Scheduling Simulator
-----------------------------------------
This module provides the UI for scheduling algorithms (FCFS, SJF, RR)
and deadlock prevention (Banker's Algorithm).
"""

import tkinter as tk
from tkinter import ttk, messagebox, font, scrolledtext
from typing import List, Dict, Tuple
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms import fcfs, sjf, round_robin
from utils import average_waiting_time, average_turnaround_time
from advance_features import bankers_algorithm
from advance_features import total_resources, allocation, max_need, process_ids, resource_names


class SchedulerUI(tk.Frame):
    """UI for CPU scheduling algorithms."""
    
    # Color palette for processes
    PROCESS_COLORS = [
        "#89b4fa", "#a6e3a1", "#f9e2af", "#f38ba8", "#cba6f7",
        "#fab387", "#94e2d5", "#f5c2e7", "#b4befe", "#74c7ec"
    ]
    
    def __init__(self, root, algorithm: str, back_callback):
        super().__init__(root)
        self.root = root
        self.algorithm = algorithm
        self.back_callback = back_callback
        self.processes = []
        self.results = None
        self.gantt_chart = None
        self.time_quantum = None
        
        self.configure(bg="#1e1e2e")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI components."""
        # Header with back button
        header_frame = tk.Frame(self, bg="#1e1e2e")
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Title
        title_font = font.Font(family="Arial", size=24, weight="bold")
        title_text = {
            "FCFS": "First Come First Serve (FCFS)",
            "SJF": "Shortest Job First (SJF)",
            "RR": "Round Robin (RR)"
        }.get(self.algorithm, self.algorithm)
        
        title_label = tk.Label(
            header_frame,
            text=title_text,
            font=title_font,
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        title_label.pack(side=tk.LEFT)
        
        # Back button
        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=font.Font(family="Arial", size=12, weight="bold"),
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            activeforeground="#cdd6f4",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.back_callback,
            borderwidth=0
        )
        back_btn.pack(side=tk.RIGHT)
        
        # Main content area with scrolling
        canvas = tk.Canvas(self, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Bind mousewheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        self.content_frame = scrollable_frame
        
        # Show input form
        self.show_input_form()
    
    def show_input_form(self):
        """Show form to input number of processes."""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Input frame
        input_frame = tk.Frame(self.content_frame, bg="#313244", relief=tk.RAISED, bd=2)
        input_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            input_frame,
            text="Enter Number of Processes",
            font=font.Font(family="Arial", size=16, weight="bold"),
            bg="#313244",
            fg="#cdd6f4"
        )
        title_label.pack(pady=20)
        
        # Input field
        input_container = tk.Frame(input_frame, bg="#313244")
        input_container.pack(pady=20)
        
        tk.Label(
            input_container,
            text="Number of Processes:",
            font=font.Font(family="Arial", size=12),
            bg="#313244",
            fg="#bac2de"
        ).pack(side=tk.LEFT, padx=10)
        
        self.num_processes_var = tk.StringVar(value="3")
        num_entry = tk.Entry(
            input_container,
            textvariable=self.num_processes_var,
            font=font.Font(family="Arial", size=12),
            width=10,
            bg="#45475a",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief=tk.FLAT,
            bd=5
        )
        num_entry.pack(side=tk.LEFT, padx=10)
        
        # Generate button
        generate_btn = tk.Button(
            input_frame,
            text="Generate Table",
            font=font.Font(family="Arial", size=12, weight="bold"),
            bg="#89b4fa",
            fg="#1e1e2e",
            activebackground="#a5c9ff",
            activeforeground="#1e1e2e",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.generate_table,
            borderwidth=0
        )
        generate_btn.pack(pady=20)
    
    def generate_table(self):
        """Generate input table for processes."""
        try:
            num_processes = int(self.num_processes_var.get())
            if num_processes <= 0:
                messagebox.showerror("Error", "Number of processes must be positive!")
                return
            if num_processes > 20:
                messagebox.showerror("Error", "Maximum 20 processes allowed!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Table frame
        table_frame = tk.Frame(self.content_frame, bg="#313244", relief=tk.RAISED, bd=2)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            table_frame,
            text="Enter Process Details",
            font=font.Font(family="Arial", size=16, weight="bold"),
            bg="#313244",
            fg="#cdd6f4"
        )
        title_label.pack(pady=20)
        
        # Time quantum for RR
        if self.algorithm == "RR":
            quantum_frame = tk.Frame(table_frame, bg="#313244")
            quantum_frame.pack(pady=10)
            
            tk.Label(
                quantum_frame,
                text="Time Quantum:",
                font=font.Font(family="Arial", size=12),
                bg="#313244",
                fg="#bac2de"
            ).pack(side=tk.LEFT, padx=10)
            
            self.quantum_var = tk.StringVar(value="2")
            quantum_entry = tk.Entry(
                quantum_frame,
                textvariable=self.quantum_var,
                font=font.Font(family="Arial", size=12),
                width=10,
                bg="#45475a",
                fg="#cdd6f4",
                insertbackground="#cdd6f4",
                relief=tk.FLAT,
                bd=5
            )
            quantum_entry.pack(side=tk.LEFT, padx=10)
        
        # Create table
        table_container = tk.Frame(table_frame, bg="#313244")
        table_container.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Headers
        headers = ["PID", "Arrival Time", "Burst Time"]
        if self.algorithm in ["FCFS", "SJF"]:
            headers.append("Priority (Optional)")
        
        header_frame = tk.Frame(table_container, bg="#45475a")
        header_frame.pack(fill=tk.X)
        
        for i, header in enumerate(headers):
            label = tk.Label(
                header_frame,
                text=header,
                font=font.Font(family="Arial", size=11, weight="bold"),
                bg="#45475a",
                fg="#cdd6f4",
                padx=15,
                pady=10
            )
            label.grid(row=0, column=i, sticky="ew", padx=1)
        
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=1)
        if len(headers) > 3:
            header_frame.grid_columnconfigure(3, weight=1)
        
        # Entry fields
        self.entries = []
        for i in range(num_processes):
            row_frame = tk.Frame(table_container, bg="#313244")
            row_frame.pack(fill=tk.X, pady=2)
            
            row_entries = []
            
            # PID
            pid_var = tk.StringVar(value=f"P{i+1}")
            pid_entry = tk.Entry(
                row_frame,
                textvariable=pid_var,
                font=font.Font(family="Arial", size=11),
                bg="#45475a",
                fg="#cdd6f4",
                insertbackground="#cdd6f4",
                relief=tk.FLAT,
                bd=5
            )
            pid_entry.grid(row=0, column=0, sticky="ew", padx=1, pady=1)
            row_entries.append(pid_var)
            
            # Arrival
            arrival_var = tk.StringVar(value="0")
            arrival_entry = tk.Entry(
                row_frame,
                textvariable=arrival_var,
                font=font.Font(family="Arial", size=11),
                bg="#45475a",
                fg="#cdd6f4",
                insertbackground="#cdd6f4",
                relief=tk.FLAT,
                bd=5
            )
            arrival_entry.grid(row=0, column=1, sticky="ew", padx=1, pady=1)
            row_entries.append(arrival_var)
            
            # Burst
            burst_var = tk.StringVar(value="1")
            burst_entry = tk.Entry(
                row_frame,
                textvariable=burst_var,
                font=font.Font(family="Arial", size=11),
                bg="#45475a",
                fg="#cdd6f4",
                insertbackground="#cdd6f4",
                relief=tk.FLAT,
                bd=5
            )
            burst_entry.grid(row=0, column=2, sticky="ew", padx=1, pady=1)
            row_entries.append(burst_var)
            
            # Priority (optional)
            if self.algorithm in ["FCFS", "SJF"]:
                priority_var = tk.StringVar(value="0")
                priority_entry = tk.Entry(
                    row_frame,
                    textvariable=priority_var,
                    font=font.Font(family="Arial", size=11),
                    bg="#45475a",
                    fg="#cdd6f4",
                    insertbackground="#cdd6f4",
                    relief=tk.FLAT,
                    bd=5
                )
                priority_entry.grid(row=0, column=3, sticky="ew", padx=1, pady=1)
                row_entries.append(priority_var)
            
            row_frame.grid_columnconfigure(0, weight=1)
            row_frame.grid_columnconfigure(1, weight=1)
            row_frame.grid_columnconfigure(2, weight=1)
            if len(headers) > 3:
                row_frame.grid_columnconfigure(3, weight=1)
            
            self.entries.append(row_entries)
        
        # Run button
        run_btn = tk.Button(
            table_frame,
            text=f"RUN {self.algorithm}",
            font=font.Font(family="Arial", size=14, weight="bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            activebackground="#b8f0b3",
            activeforeground="#1e1e2e",
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=15,
            command=self.run_algorithm,
            borderwidth=0
        )
        run_btn.pack(pady=20)
    
    def run_algorithm(self):
        """Run the selected algorithm."""
        # Collect process data
        processes = []
        try:
            for row_entries in self.entries:
                pid = row_entries[0].get().strip().upper()
                if not pid:
                    messagebox.showerror("Error", "PID cannot be empty!")
                    return
                
                arrival = int(row_entries[1].get())
                burst = int(row_entries[2].get())
                
                if arrival < 0:
                    messagebox.showerror("Error", "Arrival time must be >= 0!")
                    return
                if burst <= 0:
                    messagebox.showerror("Error", "Burst time must be > 0!")
                    return
                
                process = {
                    "pid": pid,
                    "arrival": arrival,
                    "burst": burst
                }
                
                if len(row_entries) > 3:
                    priority_str = row_entries[3].get().strip()
                    if priority_str:
                        process["priority"] = int(priority_str)
                    else:
                        process["priority"] = 0
                
                processes.append(process)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
            return
        
        # Get time quantum for RR
        if self.algorithm == "RR":
            try:
                self.time_quantum = int(self.quantum_var.get())
                if self.time_quantum <= 0:
                    messagebox.showerror("Error", "Time quantum must be positive!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid time quantum!")
                return
        
        # Run algorithm
        try:
            if self.algorithm == "FCFS":
                self.results, self.gantt_chart = fcfs(processes)
            elif self.algorithm == "SJF":
                self.results, self.gantt_chart = sjf(processes)
            elif self.algorithm == "RR":
                self.results, self.gantt_chart = round_robin(processes, self.time_quantum)
            
            # Display results
            self.display_results()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def display_results(self):
        """Display algorithm results with Gantt chart and metrics."""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Results container
        results_frame = tk.Frame(self.content_frame, bg="#1e1e2e")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            results_frame,
            text=f"{self.algorithm} Results",
            font=font.Font(family="Arial", size=20, weight="bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        title_label.pack(pady=20)
        
        # Gantt Chart Section
        gantt_frame = tk.Frame(results_frame, bg="#313244", relief=tk.RAISED, bd=2)
        gantt_frame.pack(fill=tk.X, padx=20, pady=10)
        
        gantt_title = tk.Label(
            gantt_frame,
            text="Gantt Chart",
            font=font.Font(family="Arial", size=16, weight="bold"),
            bg="#313244",
            fg="#cdd6f4"
        )
        gantt_title.pack(pady=15)
        
        # Execution order
        execution_order = " → ".join([pid for pid, _, _ in self.gantt_chart])
        order_label = tk.Label(
            gantt_frame,
            text=f"Execution Order: {execution_order}",
            font=font.Font(family="Arial", size=12),
            bg="#313244",
            fg="#bac2de"
        )
        order_label.pack(pady=10)
        
        # Visual Gantt Chart
        chart_canvas = tk.Canvas(
            gantt_frame,
            bg="#45475a",
            height=150,
            highlightthickness=0
        )
        chart_canvas.pack(fill=tk.X, padx=20, pady=20)
        
        self.draw_gantt_chart(chart_canvas)
        
        # Timeline
        timeline_frame = tk.Frame(gantt_frame, bg="#313244")
        timeline_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.draw_timeline(timeline_frame)
        
        # Metrics Section
        metrics_frame = tk.Frame(results_frame, bg="#313244", relief=tk.RAISED, bd=2)
        metrics_frame.pack(fill=tk.X, padx=20, pady=10)
        
        metrics_title = tk.Label(
            metrics_frame,
            text="Process Metrics",
            font=font.Font(family="Arial", size=16, weight="bold"),
            bg="#313244",
            fg="#cdd6f4"
        )
        metrics_title.pack(pady=15)
        
        # Metrics table
        metrics_table = tk.Frame(metrics_frame, bg="#313244")
        metrics_table.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Headers
        headers = ["PID", "Waiting Time", "Turnaround Time", "Response Time"]
        header_row = tk.Frame(metrics_table, bg="#45475a")
        header_row.pack(fill=tk.X)
        
        for header in headers:
            label = tk.Label(
                header_row,
                text=header,
                font=font.Font(family="Arial", size=11, weight="bold"),
                bg="#45475a",
                fg="#cdd6f4",
                padx=15,
                pady=10
            )
            label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Data rows
        for i, proc in enumerate(self.results):
            row_color = "#313244" if i % 2 == 0 else "#3a3d52"
            row = tk.Frame(metrics_table, bg=row_color)
            row.pack(fill=tk.X)
            
            pid_color = self.PROCESS_COLORS[i % len(self.PROCESS_COLORS)]
            
            tk.Label(
                row,
                text=proc["pid"],
                font=font.Font(family="Arial", size=11, weight="bold"),
                bg=row_color,
                fg=pid_color,
                padx=15,
                pady=8
            ).pack(side=tk.LEFT, expand=True, fill=tk.X)
            
            tk.Label(
                row,
                text=str(proc["waiting"]),
                font=font.Font(family="Arial", size=11),
                bg=row_color,
                fg="#cdd6f4",
                padx=15,
                pady=8
            ).pack(side=tk.LEFT, expand=True, fill=tk.X)
            
            tk.Label(
                row,
                text=str(proc["turnaround"]),
                font=font.Font(family="Arial", size=11),
                bg=row_color,
                fg="#cdd6f4",
                padx=15,
                pady=8
            ).pack(side=tk.LEFT, expand=True, fill=tk.X)
            
            tk.Label(
                row,
                text=str(proc["response"]),
                font=font.Font(family="Arial", size=11),
                bg=row_color,
                fg="#cdd6f4",
                padx=15,
                pady=8
            ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Average metrics
        avg_wt = average_waiting_time(self.results)
        avg_tat = average_turnaround_time(self.results)
        
        avg_frame = tk.Frame(metrics_frame, bg="#45475a")
        avg_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            avg_frame,
            text=f"Average Waiting Time: {avg_wt:.2f}",
            font=font.Font(family="Arial", size=12, weight="bold"),
            bg="#45475a",
            fg="#a6e3a1",
            padx=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            avg_frame,
            text=f"Average Turnaround Time: {avg_tat:.2f}",
            font=font.Font(family="Arial", size=12, weight="bold"),
            bg="#45475a",
            fg="#a6e3a1",
            padx=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True)
        
        # Back button
        back_btn = tk.Button(
            results_frame,
            text="← Back to Input",
            font=font.Font(family="Arial", size=12, weight="bold"),
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            activeforeground="#cdd6f4",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.show_input_form,
            borderwidth=0
        )
        back_btn.pack(pady=20)
    
    def draw_gantt_chart(self, canvas):
        """Draw colorful Gantt chart on canvas."""
        if not self.gantt_chart:
            return
        
        # Calculate dimensions
        max_time = max(end for _, _, end in self.gantt_chart)
        # Get parent width or use default
        parent_width = self.content_frame.winfo_width() or 800
        canvas_width = max(800, parent_width - 80)  # Account for padding
        canvas_height = 120
        canvas.config(width=canvas_width, height=canvas_height)
        
        # Scale factor
        scale = (canvas_width - 100) / max(1, max_time)
        bar_height = 60
        y_start = 30
        
        # Draw bars
        x_offset = 50
        process_color_map = {}
        color_index = 0
        
        for pid, start, end in self.gantt_chart:
            if pid not in process_color_map:
                process_color_map[pid] = self.PROCESS_COLORS[color_index % len(self.PROCESS_COLORS)]
                color_index += 1
            
            x1 = x_offset + start * scale
            x2 = x_offset + end * scale
            width = x2 - x1
            
            # Draw bar
            canvas.create_rectangle(
                x1, y_start,
                x2, y_start + bar_height,
                fill=process_color_map[pid],
                outline="#1e1e2e",
                width=2
            )
            
            # Draw PID text
            if width > 30:
                canvas.create_text(
                    (x1 + x2) / 2,
                    y_start + bar_height / 2,
                    text=pid,
                    font=font.Font(family="Arial", size=10, weight="bold"),
                    fill="#1e1e2e"
                )
            
        # Collect unique time points
        time_points = set()
        for pid, start, end in self.gantt_chart:
            time_points.add(start)
            time_points.add(end)
        time_points = sorted(time_points)
        
        # Draw time labels
        for time_point in time_points:
            x_pos = x_offset + time_point * scale
            canvas.create_text(
                x_pos, y_start - 10,
                text=str(time_point),
                font=font.Font(family="Arial", size=9),
                fill="#bac2de",
                anchor="s"
            )
        
        # Draw axis line
        canvas.create_line(
            x_offset, y_start + bar_height + 5,
            x_offset + max_time * scale, y_start + bar_height + 5,
            fill="#bac2de",
            width=2
        )
    
    def draw_timeline(self, parent):
        """Draw timeline visualization matching CLI output format - each process on its own line."""
        if not self.gantt_chart:
            return
        
        timeline_label = tk.Label(
            parent,
            text="Timeline:",
            font=font.Font(family="Arial", size=12, weight="bold"),
            bg="#313244",
            fg="#cdd6f4"
        )
        timeline_label.pack(anchor=tk.W, pady=10)
        
        max_time = max(end for _, _, end in self.gantt_chart)
        # Get parent width or use default
        parent_width = self.content_frame.winfo_width() or 800
        canvas_width = max(800, parent_width - 80)  # Account for padding
        scale = (canvas_width - 100) / max(1, max_time)
        bar_height = 30
        line_spacing = 40
        x_offset = 50
        
        # Calculate canvas height based on number of processes
        num_processes = len(self.gantt_chart)
        canvas_height = num_processes * line_spacing + 50
        
        timeline_canvas = tk.Canvas(
            parent,
            bg="#45475a",
            height=canvas_height,
            highlightthickness=0
        )
        timeline_canvas.pack(fill=tk.X, pady=10)
        
        # Collect all unique time points (start and end of each segment)
        time_points = set([0])  # Always include 0
        for pid, start, end in self.gantt_chart:
            time_points.add(start)
            time_points.add(end)
        time_points = sorted(time_points)
        
        process_color_map = {}
        color_index = 0
        
        # Draw each process on its own line
        for i, (pid, start, end) in enumerate(self.gantt_chart):
            if pid not in process_color_map:
                process_color_map[pid] = self.PROCESS_COLORS[color_index % len(self.PROCESS_COLORS)]
                color_index += 1
            
            y_pos = 20 + i * line_spacing
            
            # Draw process label
            timeline_canvas.create_text(
                x_offset - 5, y_pos + bar_height / 2,
                text=f"{pid}:",
                font=font.Font(family="Arial", size=10, weight="bold"),
                fill="#cdd6f4",
                anchor="e"
            )
            
            # Draw bar starting at the start position (which aligns with previous process end)
            x1 = x_offset + start * scale
            x2 = x_offset + end * scale
            
            timeline_canvas.create_rectangle(
                x1, y_pos,
                x2, y_pos + bar_height,
                fill=process_color_map[pid],
                outline="#1e1e2e",
                width=1
            )
            
            # Draw time labels for this process
            timeline_canvas.create_text(
                x1, y_pos + bar_height + 12,
                text=str(start),
                font=font.Font(family="Arial", size=8),
                fill="#bac2de",
                anchor="n"
            )
            timeline_canvas.create_text(
                x2, y_pos + bar_height + 12,
                text=str(end),
                font=font.Font(family="Arial", size=8),
                fill="#bac2de",
                anchor="n"
            )
            
            # Draw connecting line from previous end to current start (if not first process)
            if i > 0:
                prev_end = self.gantt_chart[i-1][2]
                if prev_end == start:
                    # Draw a vertical line connecting them
                    prev_y = 20 + (i-1) * line_spacing + bar_height
                    timeline_canvas.create_line(
                        x_offset + prev_end * scale, prev_y,
                        x_offset + start * scale, y_pos,
                        fill="#6c7086",
                        width=1,
                        dash=(3, 3)
                    )
        
        # Draw bottom time axis with all time points
        axis_y = 20 + num_processes * line_spacing + 5
        timeline_canvas.create_line(
            x_offset, axis_y,
            x_offset + max_time * scale, axis_y,
            fill="#bac2de",
            width=2
        )
        
        # Draw time labels on axis
        for time_point in time_points:
            x_pos = x_offset + time_point * scale
            timeline_canvas.create_text(
                x_pos, axis_y + 10,
                text=str(time_point),
                font=font.Font(family="Arial", size=9),
                fill="#bac2de",
                anchor="n"
            )
            # Draw tick mark
            timeline_canvas.create_line(
                x_pos, axis_y,
                x_pos, axis_y + 5,
                fill="#bac2de",
                width=1
            )
        
        timeline_canvas.config(width=canvas_width)


class DeadlockUI(tk.Frame):
    """UI for Deadlock Prevention (Banker's Algorithm)."""
    
    def __init__(self, root, back_callback):
        super().__init__(root)
        self.root = root
        self.back_callback = back_callback
        
        self.configure(bg="#1e1e2e")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI components."""
        # Header with back button
        header_frame = tk.Frame(self, bg="#1e1e2e")
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Title
        title_font = font.Font(family="Arial", size=24, weight="bold")
        title_label = tk.Label(
            header_frame,
            text="Deadlock Prevention (Banker's Algorithm)",
            font=title_font,
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        title_label.pack(side=tk.LEFT)
        
        # Back button
        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=font.Font(family="Arial", size=12, weight="bold"),
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            activeforeground="#cdd6f4",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.back_callback,
            borderwidth=0
        )
        back_btn.pack(side=tk.RIGHT)
        
        # Main content area with scrolling
        canvas = tk.Canvas(self, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Bind mousewheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        self.content_frame = scrollable_frame
        
        # Run algorithm and display results
        self.run_bankers_algorithm()
    
    def run_bankers_algorithm(self):
        """Run Banker's algorithm and get data for visual display."""
        try:
            # Calculate values
            num_resources = len(resource_names)
            allocated_sum = [sum(x[i] for x in allocation) for i in range(num_resources)]
            available = [total_resources[i] - allocated_sum[i] for i in range(num_resources)]
            
            need = [
                [max_need[i][j] - allocation[i][j] for j in range(num_resources)]
                for i in range(len(allocation))
            ]
            
            finished = [False] * len(process_ids)
            safe_sequence = []
            execution_steps = []
            
            # Run algorithm and capture steps
            while len(safe_sequence) < len(process_ids):
                executed_in_cycle = False
                
                for i in range(len(process_ids)):
                    if not finished[i]:
                        if all(need[i][r] <= available[r] for r in range(num_resources)):
                            # Process can finish
                            step = {
                                'process': process_ids[i],
                                'allocation': allocation[i].copy(),
                                'available_before': available.copy(),
                                'available_after': [available[r] + allocation[i][r] for r in range(num_resources)]
                            }
                            execution_steps.append(step)
                            
                            available = step['available_after']
                            finished[i] = True
                            safe_sequence.append(process_ids[i])
                            executed_in_cycle = True
                            break
                
                if not executed_in_cycle:
                    # Unsafe state
                    self.display_results(
                        total_resources, allocation, max_need, need,
                        process_ids, resource_names, available,
                        execution_steps, safe_sequence, is_safe=False
                    )
                    return
            
            # Safe state
            self.display_results(
                total_resources, allocation, max_need, need,
                process_ids, resource_names, available,
                execution_steps, safe_sequence, is_safe=True
            )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def display_results(self, total_resources, allocation, max_need, need,
                       process_ids, resource_names, available,
                       execution_steps, safe_sequence, is_safe):
        """Display Banker's algorithm results with attractive visual formatting."""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Results container
        results_frame = tk.Frame(self.content_frame, bg="#1e1e2e")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            results_frame,
            text="Banker's Algorithm Visualization",
            font=font.Font(family="Arial", size=20, weight="bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        title_label.pack(pady=20)
        
        # Total Resources Section
        total_frame = tk.Frame(results_frame, bg="#313244", relief=tk.RAISED, bd=2)
        total_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            total_frame,
            text="Total System Resources",
            font=font.Font(family="Arial", size=14, weight="bold"),
            bg="#313244",
            fg="#89b4fa"
        ).pack(pady=15)
        
        resources_container = tk.Frame(total_frame, bg="#313244")
        resources_container.pack(pady=(0, 15))
        
        for i, res_name in enumerate(resource_names):
            res_frame = tk.Frame(resources_container, bg="#45475a", relief=tk.RAISED, bd=1)
            res_frame.pack(side=tk.LEFT, padx=10, pady=5)
            
            tk.Label(
                res_frame,
                text=res_name,
                font=font.Font(family="Arial", size=11),
                bg="#45475a",
                fg="#bac2de"
            ).pack(padx=15, pady=5)
            
            tk.Label(
                res_frame,
                text=str(total_resources[i]),
                font=font.Font(family="Arial", size=16, weight="bold"),
                bg="#45475a",
                fg="#89b4fa"
            ).pack(padx=15, pady=(0, 10))
        
        # Process Details Table
        process_frame = tk.Frame(results_frame, bg="#313244", relief=tk.RAISED, bd=2)
        process_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(
            process_frame,
            text="Process Details",
            font=font.Font(family="Arial", size=14, weight="bold"),
            bg="#313244",
            fg="#cdd6f4"
        ).pack(pady=15)
        
        # Table container with scrolling
        table_container = tk.Frame(process_frame, bg="#313244")
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Headers
        headers = ["PID", "Allocation", "Max Need", "Remaining Need", "Status"]
        header_row = tk.Frame(table_container, bg="#45475a")
        header_row.pack(fill=tk.X, pady=(0, 2))
        
        for header in headers:
            label = tk.Label(
                header_row,
                text=header,
                font=font.Font(family="Arial", size=11, weight="bold"),
                bg="#45475a",
                fg="#cdd6f4",
                padx=10,
                pady=10
            )
            label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Process rows
        process_colors = ["#89b4fa", "#a6e3a1", "#f9e2af", "#f38ba8", "#cba6f7"]
        for i, pid in enumerate(process_ids):
            row_color = "#313244" if i % 2 == 0 else "#3a3d52"
            row = tk.Frame(table_container, bg=row_color)
            row.pack(fill=tk.X, pady=1)
            
            # PID
            pid_color = process_colors[i % len(process_colors)]
            tk.Label(
                row,
                text=pid,
                font=font.Font(family="Arial", size=11, weight="bold"),
                bg=row_color,
                fg=pid_color,
                padx=10,
                pady=8
            ).pack(side=tk.LEFT, expand=True, fill=tk.X)
            
            # Allocation
            alloc_str = "(" + ", ".join(map(str, allocation[i])) + ")"
            tk.Label(
                row,
                text=alloc_str,
                font=font.Font(family="Arial", size=10),
                bg=row_color,
                fg="#bac2de",
                padx=10,
                pady=8
            ).pack(side=tk.LEFT, expand=True, fill=tk.X)
            
            # Max Need
            max_str = "(" + ", ".join(map(str, max_need[i])) + ")"
            tk.Label(
                row,
                text=max_str,
                font=font.Font(family="Arial", size=10),
                bg=row_color,
                fg="#bac2de",
                padx=10,
                pady=8
            ).pack(side=tk.LEFT, expand=True, fill=tk.X)
            
            # Remaining Need
            need_str = "(" + ", ".join(map(str, need[i])) + ")"
            tk.Label(
                row,
                text=need_str,
                font=font.Font(family="Arial", size=10),
                bg=row_color,
                fg="#f9e2af",
                padx=10,
                pady=8
            ).pack(side=tk.LEFT, expand=True, fill=tk.X)
            
            # Status
            status = "Completed" if pid in safe_sequence else "Pending"
            status_color = "#a6e3a1" if status == "Completed" else "#f38ba8"
            tk.Label(
                row,
                text=status,
                font=font.Font(family="Arial", size=10, weight="bold"),
                bg=row_color,
                fg=status_color,
                padx=10,
                pady=8
            ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Available Resources (Initial)
        available_frame = tk.Frame(results_frame, bg="#313244", relief=tk.RAISED, bd=2)
        available_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            available_frame,
            text="Available Resources (Initial)",
            font=font.Font(family="Arial", size=14, weight="bold"),
            bg="#313244",
            fg="#cdd6f4"
        ).pack(pady=15)
        
        avail_container = tk.Frame(available_frame, bg="#313244")
        avail_container.pack(pady=(0, 15))
        
        # Calculate initial available
        num_resources = len(resource_names)
        allocated_sum = [sum(x[i] for x in allocation) for i in range(num_resources)]
        initial_available = [total_resources[i] - allocated_sum[i] for i in range(num_resources)]
        
        for i, res_name in enumerate(resource_names):
            res_frame = tk.Frame(avail_container, bg="#45475a", relief=tk.RAISED, bd=1)
            res_frame.pack(side=tk.LEFT, padx=10, pady=5)
            
            tk.Label(
                res_frame,
                text=res_name,
                font=font.Font(family="Arial", size=11),
                bg="#45475a",
                fg="#bac2de"
            ).pack(padx=15, pady=5)
            
            tk.Label(
                res_frame,
                text=str(initial_available[i]),
                font=font.Font(family="Arial", size=16, weight="bold"),
                bg="#45475a",
                fg="#a6e3a1"
            ).pack(padx=15, pady=(0, 10))
        
        # Execution Steps
        if execution_steps:
            steps_frame = tk.Frame(results_frame, bg="#313244", relief=tk.RAISED, bd=2)
            steps_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            tk.Label(
                steps_frame,
                text="Execution Steps",
                font=font.Font(family="Arial", size=14, weight="bold"),
                bg="#313244",
                fg="#cdd6f4"
            ).pack(pady=15)
            
            steps_container = tk.Frame(steps_frame, bg="#313244")
            steps_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
            
            for step_num, step in enumerate(execution_steps, 1):
                step_row = tk.Frame(steps_container, bg="#45475a", relief=tk.RAISED, bd=1)
                step_row.pack(fill=tk.X, pady=5)
                
                # Step number and process
                step_header = tk.Frame(step_row, bg="#45475a")
                step_header.pack(fill=tk.X, padx=15, pady=10)
                
                tk.Label(
                    step_header,
                    text=f"Step {step_num}: Process {step['process']}",
                    font=font.Font(family="Arial", size=12, weight="bold"),
                    bg="#45475a",
                    fg="#89b4fa"
                ).pack(side=tk.LEFT)
                
                # Step details
                details_frame = tk.Frame(step_row, bg="#45475a")
                details_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
                
                tk.Label(
                    details_frame,
                    text=f"Releases: {tuple(step['allocation'])}",
                    font=font.Font(family="Arial", size=10),
                    bg="#45475a",
                    fg="#bac2de"
                ).pack(side=tk.LEFT, padx=10)
                
                avail_str = ", ".join([f"{resource_names[r]}={step['available_after'][r]}" for r in range(len(resource_names))])
                tk.Label(
                    details_frame,
                    text=f"New Available: {avail_str}",
                    font=font.Font(family="Arial", size=10, weight="bold"),
                    bg="#45475a",
                    fg="#a6e3a1"
                ).pack(side=tk.LEFT, padx=10)
        
        # Safe Sequence
        sequence_frame = tk.Frame(results_frame, bg="#313244", relief=tk.RAISED, bd=2)
        sequence_frame.pack(fill=tk.X, padx=20, pady=10)
        
        if is_safe:
            tk.Label(
                sequence_frame,
                text="Safe Sequence Found",
                font=font.Font(family="Arial", size=16, weight="bold"),
                bg="#313244",
                fg="#a6e3a1"
            ).pack(pady=15)
            
            sequence_str = " → ".join(safe_sequence)
            tk.Label(
                sequence_frame,
                text=sequence_str,
                font=font.Font(family="Arial", size=18, weight="bold"),
                bg="#313244",
                fg="#cdd6f4"
            ).pack(pady=(0, 15))
            
            tk.Label(
                sequence_frame,
                text="SYSTEM STATE: SAFE ✓",
                font=font.Font(family="Arial", size=14, weight="bold"),
                bg="#313244",
                fg="#a6e3a1"
            ).pack(pady=(0, 15))
        else:
            tk.Label(
                sequence_frame,
                text="SYSTEM STATE: UNSAFE ✗",
                font=font.Font(family="Arial", size=16, weight="bold"),
                bg="#313244",
                fg="#f38ba8"
            ).pack(pady=15)
            
            tk.Label(
                sequence_frame,
                text="No safe sequence exists",
                font=font.Font(family="Arial", size=12),
                bg="#313244",
                fg="#bac2de"
            ).pack(pady=(0, 15))
        
        # Run again button
        run_btn = tk.Button(
            results_frame,
            text="Run Again",
            font=font.Font(family="Arial", size=12, weight="bold"),
            bg="#f38ba8",
            fg="#1e1e2e",
            activebackground="#ffa0bc",
            activeforeground="#1e1e2e",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.run_bankers_algorithm,
            borderwidth=0
        )
        run_btn.pack(pady=20)