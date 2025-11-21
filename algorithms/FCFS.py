from typing import List, Dict, Tuple

def fcfs(processes: List[Dict]) -> Tuple[List[Dict], List[Tuple[str, int, int]]]:

    # Input Validations
    if not isinstance(processes, list):#if processes are not given as a list of dictionaries
        raise TypeError("Processes must be provided as a list of dictionaries.")

    if not processes:#if list of processes is empty it will return empty lists also
        return [], []

    required_keys = {"pid", "arrival", "burst"}
    for p in processes:
        
        if not required_keys.issubset(p.keys()):#if any of input field like (pid, arrival,burst etc) is not in list this will raise Error
            raise KeyError(f"Process {p} is missing required keys: {required_keys}")

        if p["arrival"] < 0 or p["burst"] <= 0:#this checks that arrival is not negative and burst is not negative also not equal to 0
            raise ValueError("Arrival must be >= 0 and Burst Time must be > 0.")

    # FCFS main logic sorting the processes according to its arrival time
    # using lambda function as a key for sorted funtion, it gets arrival from every dictionary and helps in sorting
    processes = sorted(processes, key=lambda x: x["arrival"])

    current_time = 0
    gantt_chart = []

    # Main FCFS loop
    for proc in processes:
        arrival = proc["arrival"]
        burst = proc["burst"]

        # This checks if the CPU is free before the process arrives.
        # If the current time is before the arrival time, we will wait until the process shows up.
        # So, we move current time up to when this process arrives.
        if current_time < arrival:
            current_time = arrival

        # Recording start time
        proc["start"] = current_time

        # Executing process fully (non-preemptive)
        current_time += burst

        # Recording finish time
        proc["finish"] = current_time

        # Metrics Calculations
        proc["turnaround"] = proc["finish"] - proc["arrival"] #total time taken from arrival to completion
        proc["waiting"] = proc["turnaround"] - proc["burst"] #time process spent in ready queue
        proc["response"] = proc["start"] - proc["arrival"] #time when process first gets the cpu 

        # Append to Gantt chart
        gantt_chart.append((proc["pid"], proc["start"], proc["finish"]))

    return processes, gantt_chart



if _name_ == "_main_":
    # Input Requirements: Number of processes, Process ID, Arrival Time, Burst Time
    sample_processes = [#sample input for testing 
        {"pid": "P1", "arrival": 0, "burst": 5},
        {"pid": "P2", "arrival": 2, "burst": 3},
        {"pid": "P3", "arrival": 4, "burst": 1},
    ]

    print("\n" + "="*90)#printing "=" 90 times
    print(" " * 28 + "FCFS SCHEDULING SIMULATOR")
    print("="*90)
    
    print("\nINPUT PROCESSES:")
    print("-" * 90)
    print(f"{'PID':<5} {'Arrival Time':<15} {'Burst Time':<15}")#making table format :< -> left assigned, any number like :<8 means columns is 8 unit wide
    print("-" * 90)
    for p in sample_processes:
        print(f"{p['pid']:<8} {p['arrival']:<15} {p['burst']:<15}")
    print("-" * 90)

    # Calling Algorithm
    results, chart = fcfs(sample_processes)#results will get results of processes and chart will get gantt chart

    # Final Output
    print("\n" + "="*90)
    print(" " * 28 + "FCFS SCHEDULING RESULTS")
    print("="*90 + "\n")

    # 1. Process Execution Order (Gantt Chart or Timeline)
    print("1. PROCESS EXECUTION ORDER (GANTT CHART):")
    print("-" * 90)
    
    if chart:
        # Execution order text
        execution_order = " → ".join([pid for pid, _, _ in chart])
        print(f"Execution Order: {execution_order}\n")
        
        # Gantt Chart Timeline
        timeline = "|"
        labels = "0"
        for pid, start, end in chart:
            duration = end - start
            timeline += f" {pid:^8} |"
            labels += f"{start:>10}{end:>10}"
        
        print("Gantt Chart:")
        print(timeline)
        print(labels)
        
        # Visual Timeline
        print("\nVisual Timeline:")
        for pid, start, end in chart:
            duration = end - start
            bar = "█" * max(1, duration)
            print(f"  {pid}: {' ' * start}{bar} ({start} → {end})")
    else:
        print("No processes to execute.")
    
    # 2. Waiting Time, Turnaround Time, Response Time
    print("\n2. PROCESS METRICS:")
    print("-" * 90)
    print(f"{'PID':<8} {'Waiting Time':<15} {'Turnaround Time':<18} {'Response Time':<15}")
    print("-" * 90)
    
    for p in results:
        print(f"{p['pid']:<12} {p['waiting']:<15} {p['turnaround']:<18} {p['response']:<15}")
    print("-" * 90)
    
    # 3. Average Waiting Time and Average Turnaround Time
    if results:
        avg_waiting = sum(p['waiting'] for p in results) / len(results)
        avg_turnaround = sum(p['turnaround'] for p in results) / len(results)
        
        print("\n3. AVERAGE METRICS:")
        print("-" * 90)
        print(f"Average Waiting Time:    {avg_waiting:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround:.2f}")
        print("-" * 90)
    
    print("\n" + "="*90 + "\n")