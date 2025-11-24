
from typing import List, Dict, Tuple
from collections import deque
import copy

def round_robin(processes: List[Dict], quantum: int) -> Tuple[List[Dict], List[Tuple[str, int, int]]]:
    #Input Validations

    if not isinstance(processes, list):#if process not in list form raising error
        raise TypeError("Processes must be provided as a list of dictionaries.")

    if not processes:#if there is no process
        return [], []

    if not isinstance(quantum, int) or quantum <= 0:
        raise ValueError("Quantum must be a positive integer.")

    required = {"pid", "arrival", "burst"}

    for p in processes:#for checking the keys and its values must be greater than 0 or equal to 0
        if not required.issubset(p.keys()):
            raise KeyError(f"Process {p} is missing required keys: {required}")
        if p["arrival"] < 0 or p["burst"] <= 0:
            raise ValueError("Arrival must be >= 0 and Burst Time must be > 0.")
        # Optional priority validation
        if "priority" in p and p["priority"] < 0:
            raise ValueError("Priority must be >= 0.")

    # Preparing Data for processing
    processes = copy.deepcopy(processes)
    gantt_chart = []
    current_time = 0

    for p in processes:
        p["remaining"] = p["burst"]
        p["start"] = None
        p["finish"] = None
        p["response"] = None

    # Sort by arrival time
    processes.sort(key=lambda x: x["arrival"])

    ready_queue = deque()
    remaining_processes = processes.copy()
    completed = []

    # Round Ribin Mamin Loop
    while remaining_processes:

        # Add newly arrived processes
        for p in remaining_processes:
            if p["arrival"] <= current_time and p not in ready_queue:#checks if arrival time of process is smaller than current time and also process not in ready queue then add it to ready queue
                ready_queue.append(p)

        #if there is no process in ready queue move to the next process with minimum arrival time and add it to the ready_queue
        if not ready_queue:
            next_proc = min(remaining_processes, key=lambda x: x["arrival"])
            current_time = next_proc["arrival"]
            ready_queue.append(next_proc)

        # Take first ready process from ready queue
        proc = ready_queue.popleft()
        q = quantum  # quantum time

        # Response time, first time a proess getting CPU
        if proc["start"] is None:
            proc["start"] = current_time
            proc["response"] = proc["start"] - proc["arrival"]


        # This line determines how much CPU time to allocate to the current process in this round.
        # It assigns to exec_time the smaller value between the process's quantum (q) and its remaining burst time.
        # This ensures that the process is either run for the full quantum, or—if it has less CPU time left than that—only until it finishes.
        exec_time = min(q, proc["remaining"])
        # Set when this burst starts and ends
        start_t = current_time
        end_t = current_time + exec_time
        current_time += exec_time #the clock is updated to show how much total CPU time has passed after executing this part.
        proc["remaining"] -= exec_time  # Decrease time left for this process

        # Add Entries in gannt chart
        gantt_chart.append((proc["pid"], start_t, end_t))

        # If process is finished
        if proc["remaining"] == 0:
            proc["finish"] = current_time
            proc["turnaround"] = proc["finish"] - proc["arrival"]
            proc["waiting"] = proc["turnaround"] - proc["burst"]
            completed.append(proc)#adding completed process into the complete lists
            remaining_processes.remove(proc)#removing the finished process from the remaining_processes

        else:
            # if there is new arrival so add it into the ready queue
            for p in remaining_processes:
                if p["arrival"] > start_t and p["arrival"] <= end_t and p not in ready_queue:
                    ready_queue.append(p)

            # Add back to end of queue
            ready_queue.append(proc)#process having burst time so it will added to the end of queue for again chance of 

    return completed, gantt_chart



# --------------------------- OUTPUT STYLE ---------------------------
if __name__ == "__main__":

    sample_processes = [
        {"pid": "P1", "arrival": 0, "burst": 7, "priority": 2},
        {"pid": "P2", "arrival": 2, "burst": 4, "priority": 1},
        {"pid": "P3", "arrival": 4, "burst": 2, "priority": 3},
    ]
    quantum = 2

    print("\n" + "="*80)
    print(" " * 25 + "ROUND ROBIN SCHEDULING SIMULATOR")
    print("="*80)
    
    print("\nINPUT PROCESSES:")
    print("-"*80)
    print(f"{'P_NO:':<8}{'PID':<8}{'Arrival':<12}{'Burst':<10}{'Priority':<12}{'Quantum':<10}")
    print("-"*80)
    p_n = 0
    for p in sample_processes:
        p_n +=1
        priority = p.get("priority", "N/A")
        print(f"{p_n:<8}{p['pid']:<8}{p['arrival']:<12}{p['burst']:<10}{priority:<12}{quantum:<10}")
    print("-"*80)

    results, chart = round_robin(sample_processes, quantum)

    # Gantt Chart
    print("\nGANTT CHART:")
    exec_order = " → ".join([pid for pid, _, _ in chart])
    print(f"Execution Order: {exec_order}\n")

    timeline = "|"
    times = "0"
    for pid, s, e in chart:
        timeline += f" {pid:^8} |"
        times += f"{'':>8}{e:>3}"
    print(timeline)
    print(times)

    # Metrics
    print("\nPROCESS METRICS:")
    print("-"*80)
    print(f"{'PID':<8}{'Arrival':<10}{'Burst':<8}{'Start':<8}{'Finish':<8}"
          f"{'Waiting':<10}{'Turnaround':<12}{'Response':<10}")
    print("-"*80)

    for p in results:
        p_n += 1
        print(f"{p_n:<8}{p['pid']:<8}{p['arrival']:<10}{p['burst']:<8}{p['start']:<8}{p['finish']:<8}"
              f"{p['waiting']:<10}{p['turnaround']:<12}{p['response']:<10}")

    print("-"*80)

    if results:
        avg_waiting = sum(p["waiting"] for p in results) / len(results)
        avg_turnaround = sum(p["turnaround"] for p in results) / len(results)
    else:
        avg_waiting = 0
        avg_turnaround = 0

    print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print("="*80 + "\n")