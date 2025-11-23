"""
Gantt Chart Module for CPU Scheduling Simulator
------------------------------------------------
This module provides functions to generate and print Gantt charts
for any CPU scheduling algorithm.

Functions:
    - print_gantt_chart: Display a text-based Gantt chart for CLI.
    - get_execution_order: Get execution order string from chart.
"""

from typing import List, Tuple, Optional


def get_execution_order(chart: List[Tuple[str, int, int]]) -> str:
    """
    Get execution order string from Gantt chart data.

    :param chart: List of tuples (PID, start_time, finish_time)
    :return: Execution order string like "P1 → P2 → P3"
    """
    if not chart:
        return ""
    return " → ".join([pid for pid, _, _ in chart])


def print_gantt_chart(
    chart: List[Tuple[str, int, int]],
    show_execution_order: bool = True,
    show_start_times: bool = False,
    show_visual: bool = True,
    header: Optional[str] = None
) -> None:
    """
    Print a simple ASCII-style Gantt chart based on the provided chart data.

    :param chart: List of tuples (PID, start_time, finish_time)
                  Example: [("P1", 0, 5), ("P2", 5, 8), ...]
    :param show_execution_order: If True, display execution order text (default: True)
    :param show_start_times: If True, show start times in labels (default: False)
    :param show_visual: If True, display visual block representation (default: True)
    :param header: Optional custom header text (default: None)
    """
    if not chart:
        print("No processes to display.")
        return

    # ---------- Execution Order Text ----------
    if show_execution_order:
        execution_order = get_execution_order(chart)
        if execution_order:
            print(f"Execution Order: {execution_order}\n")

    # ---------- Create timeline bars ----------
    timeline = "|"
    if show_start_times:
        # Format with both start and finish times (like FCFS)
        time_labels = "0"
        for pid, start, end in chart:
            timeline += f" {pid:^8} |"
            time_labels += f"{start:>10}{end:>10}"
    else:
        # Format with only finish times (like SJF/RR)
        time_labels = "0"
        for pid, start, end in chart:
            timeline += f" {pid:^8} |"
            time_labels += f"{'':>8}{end:>3}"

    # Print header if provided, otherwise use default
    if header:
        print(header)
    else:
        print("Gantt Chart Timeline:")
    
    print(timeline)
    print(time_labels)

    # ---------- Visual block representation ----------
    if show_visual:
        print("\nVisual Timeline:")
        for pid, start, end in chart:
            duration = end - start
            # Use a block character for visual representation
            bar = "█" * max(1, duration)
            print(f"  {pid}: {' ' * start}{bar} ({start} → {end})")


# -----------------------
# Example usage (CLI test)
# -----------------------
if __name__ == "__main__":
    sample_chart = [
        ("P1", 0, 5),
        ("P2", 5, 8),
        ("P3", 8, 12),
        ("P4", 12, 15)
    ]

    print("="*80)
    print("Example 1: Full Gantt Chart (Default)")
    print("="*80)
    print_gantt_chart(sample_chart)
    
    print("\n" + "="*80)
    print("Example 2: FCFS-style (with start times, custom header)")
    print("="*80)
    print_gantt_chart(
        sample_chart,
        show_execution_order=True,
        show_start_times=True,
        show_visual=True,
        header="Gantt Chart:"
    )
    
    print("\n" + "="*80)
    print("Example 3: SJF/RR-style (execution order + timeline bars, no visual blocks)")
    print("="*80)
    print_gantt_chart(
        sample_chart,
        show_execution_order=True,
        show_start_times=False,
        show_visual=False
    )
    
    print("\n" + "="*80)
    print("Example 4: Execution Order Only")
    print("="*80)
    order = get_execution_order(sample_chart)
    print(f"Execution Order: {order}")