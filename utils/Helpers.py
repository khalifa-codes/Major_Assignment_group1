from typing import List, Dict

def average_waiting_time(processes: List[Dict]) -> float:#calculates average waiting time of processes for all three algorithms, it's acting like helper for gantt.
    if not processes:
        return 0.0
    total_waiting = sum(p['waiting'] for p in processes)
    return total_waiting / len(processes)


def average_turnaround_time(processes: List[Dict]) -> float:
    if not processes:
        return 0.0
    total_turnaround = sum(p['turnaround'] for p in processes)
    return total_turnaround / len(processes)


def sort_processes_by_arrival(processes: List[Dict]) -> List[Dict]:
     return sorted(processes, key=lambda x: x['arrival'])


def sort_processes_by_burst(processes: List[Dict]) -> List[Dict]:
    return sorted(processes, key=lambda x: x['burst'])



if _name_ == "_main_":
    sample_processes = [
        {"pid": "P1", "arrival": 0, "burst": 5, "waiting": 0, "turnaround": 5},
        {"pid": "P2", "arrival": 2, "burst": 3, "waiting": 3, "turnaround": 6},
        {"pid": "P3", "arrival": 4, "burst": 1, "waiting": 1, "turnaround": 2},
    ]

    print("\nSample Processes:")
    for p in sample_processes:
        print(p)

    print("\nAverage Waiting Time:", average_waiting_time(sample_processes))
    print("Average Turnaround Time:", average_turnaround_time(sample_processes))

    print("\nSorted by Arrival:")
    for p in sort_processes_by_arrival(sample_processes):
        print(p)

    print("\nSorted by Burst:")
    for p in sort_processes_by_burst(sample_processes):
        print(p)