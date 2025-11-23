"""
Bonus: Deadlock Prevention Package
---------------------------------
Contains deadlock prevention algorithms like Banker's Algorithm.
"""

from .Deadlock_prevention import bankers_algorithm
from .Bankers_data import total_resources, allocation, max_need, process_ids, resource_names


__all__ = ["bankers_algorithm"]
