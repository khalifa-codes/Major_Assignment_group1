"""
Algorithms Package for CPU Scheduling Simulator
------------------------------------------------
This package contains all CPU scheduling algorithm implementations:

- FCFS: First Come First Serve (non-preemptive)
- SJF: Shortest Job First (non-preemptive)
- Round Robin: Preemptive with time quantum
- Priority Scheduling: Non-preemptive or preemptive
- SRTF: Shortest Remaining Time First (preemptive SJF)

"""

from .FCFS import fcfs
from .SJF import sjf
from .RR import round_robin
from .PS import priority_scheduling
from .SRTF import srtf

__all__ = [
    "fcfs",
    "sjf",
    "round_robin",
    "priority_scheduling",
    "srtf"
]
