import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#load file
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")])
    if not file_path:
        return

    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        df = pd.read_json(file_path)
    else:
        messagebox.showerror("Lỗi", "Định dạng tệp không hợp lệ!")
        return

    global processes
    processes = df.to_dict(orient="records")
    update_table()


def update_table():
    for row in tree.get_children():
        tree.delete(row)

    for p in processes:
        tree.insert("", "end", values=(p["ID"], p["Burst Time"],p["Arrival Time"], p["Priority"]))


def run_fcfs():
    global processes
    processes.sort(key=lambda x: x["Arrival Time"])
    time = 0
    results = []
    gantt_chart = []

    for p in processes:
        if time < p["Arrival Time"]:
            time = p["Arrival Time"]
        waiting_time = time - p["Arrival Time"]
        turnaround_time = waiting_time + p["Burst Time"]
        results.append((p["ID"], waiting_time, turnaround_time))
        gantt_chart.append((p["ID"], time, time + p["Burst Time"]))
        time += p["Burst Time"]

    display_results(results)
    plot_gantt_chart(gantt_chart)


def run_sjf_preemptive():
    global processes
    processes = sorted(processes, key=lambda x: (x["Arrival Time"], x["Burst Time"]))
    remaining_time = {p["ID"]: p["Burst Time"] for p in processes}
    time = 0
    completed = 0
    results = []
    gantt_chart = []

    while completed < len(processes):
        available_processes = [p for p in processes if p["Arrival Time"] <= time and remaining_time[p["ID"]] > 0]
        if available_processes:
            shortest = min(available_processes, key=lambda x: remaining_time[x["ID"]])
            remaining_time[shortest["ID"]] -= 1
            gantt_chart.append((shortest["ID"], time, time + 1))
            if remaining_time[shortest["ID"]] == 0:
                completion_time = time + 1
                turnaround_time = completion_time - shortest["Arrival Time"]
                waiting_time = turnaround_time - shortest["Burst Time"]
                results.append((shortest["ID"], waiting_time, turnaround_time))
                completed += 1
        time += 1

    display_results(results)
    plot_gantt_chart(gantt_chart)


def run_sjf_non_preemptive():
    global processes
    processes.sort(key=lambda x: (x["Burst Time"], x["Arrival Time"]))
    time = 0
    results = []
    gantt_chart = []

    for p in processes:
        if time < p["Arrival Time"]:
            time = p["Arrival Time"]
        waiting_time = time - p["Arrival Time"]
        turnaround_time = waiting_time + p["Burst Time"]
        results.append((p["ID"], waiting_time, turnaround_time))
        gantt_chart.append((p["ID"], time, time + p["Burst Time"]))
        time += p["Burst Time"]

    display_results(results)
    plot_gantt_chart(gantt_chart)


def run_priority_scheduling():
    global processes
    processes.sort(key=lambda x: (-x["Priority"], x["Arrival Time"]))  # Sắp xếp theo độ ưu tiên (cao hơn chạy trước)
    time = 0
    results = []
    gantt_chart = []

    for p in processes:
        if time < p["Arrival Time"]:
            time = p["Arrival Time"]
        waiting_time = time - p["Arrival Time"]
        turnaround_time = waiting_time + p["Burst Time"]
        results.append((p["ID"], waiting_time, turnaround_time))
        gantt_chart.append((p["ID"], time, time + p["Burst Time"]))
        time += p["Burst Time"]

    display_results(results)
    plot_gantt_chart(gantt_chart)


def run_round_robin():
    global processes
    quantum = simpledialog.askinteger("Nhập Quantum Time", "Nhập giá trị quantum:")
    if not quantum:
        return

    queue = []
    time = 0
    results = {}
    gantt_chart = []

    for p in processes:
        results[p["ID"]] = {"waiting_time": 0, "turnaround_time": 0, "remaining_time": p["Burst Time"],
                            "arrival_time": p["Arrival Time"]}

    processes.sort(key=lambda x: x["Arrival Time"])
    queue.append(processes[0]["ID"])

    while queue:
        process_id = queue.pop(0)
        p = next(p for p in processes if p["ID"] == process_id)

        exec_time = min(quantum, results[process_id]["remaining_time"])
        gantt_chart.append((process_id, time, time + exec_time))
        time += exec_time
        results[process_id]["remaining_time"] -= exec_time

        for p in processes:
            if p["Arrival Time"] <= time and p["ID"] not in queue and results[p["ID"]]["remaining_time"] > 0:
                queue.append(p["ID"])

        if results[process_id]["remaining_time"] > 0:
            queue.append(process_id)
        else:
            results[process_id]["turnaround_time"] = time - results[process_id]["arrival_time"]
            results[process_id]["waiting_time"] = results[process_id]["turnaround_time"] - p["Burst Time"]

    final_results = [(p["ID"], results[p["ID"]]["waiting_time"], results[p["ID"]]["turnaround_time"]) for p in
                     processes]
    display_results(final_results)
    plot_gantt_chart(gantt_chart)


def display_results(results):
    for row in result_tree.get_children():
        result_tree.delete(row)

    for res in results:
        result_tree.insert("", "end", values=res)


def plot_gantt_chart(gantt_chart):
    unique_processes = list(set(task[0] for task in gantt_chart))
    color_map = {proc: plt.cm.tab10(i / len(unique_processes)) for i, proc in enumerate(unique_processes)}
    fig, ax = plt.subplots(figsize=(8, 4))

    for task in gantt_chart:
        ax.broken_barh([(task[1], task[2] - task[1])], (10, 9), facecolors=color_map[task[0]], edgecolors='black',
                       linewidth=1.5)
        ax.text(task[1] + (task[2] - task[1]) / 2, 15, f"{task[0]}", ha='center', va='center', color='black',
                fontsize=10, fontweight='bold')

    for task in gantt_chart:
        ax.text(task[2], 5, str(task[2]), ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_xticks(range(gantt_chart[0][1], gantt_chart[-1][2] + 1))
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title("Gantt Chart")

    for widget in gantt_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=gantt_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


root = tk.Tk()
root.title("CPU Scheduling Simulator")

processes = []

frame_input = ttk.LabelFrame(root, text="Nhập dữ liệu")
frame_input.pack(padx=10, pady=10, fill="x")

ttk.Label(frame_input, text="Tập tin dữ liệu:").grid(row=0, column=0, padx=5, pady=5)
file_entry = ttk.Entry(frame_input, width=40)
file_entry.grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame_input, text="Chọn tệp", command=load_file).grid(row=0, column=2, padx=5, pady=5)

frame_buttons = ttk.Frame(frame_input)
frame_buttons.grid(row=1, column=0, columnspan=3, pady=5)

ttk.Button(frame_buttons, text="FCFS", command=run_fcfs).pack(side=tk.LEFT, padx=10, expand=True)
ttk.Button(frame_buttons, text="SJF (Preemptive)", command=run_sjf_preemptive).pack(side=tk.LEFT, padx=10, expand=True)
ttk.Button(frame_buttons, text="SJF (Non-Preemptive)", command=run_sjf_non_preemptive).pack(side=tk.LEFT, padx=10, expand=True)
ttk.Button(frame_buttons, text="Priority Scheduling", command=run_priority_scheduling).pack(side=tk.LEFT, padx=10, expand=True)
ttk.Button(frame_buttons, text="Round Robin", command=run_round_robin).pack(side=tk.LEFT, padx=10, expand=True)

frame_table = ttk.LabelFrame(root, text="Danh sách tiến trình")
frame_table.pack(padx=10, pady=10, fill="both", expand=True)


columns = ("ID", "Burst Time", "Arrival Time", "Priority")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill="both", expand=True)

frame_result = ttk.LabelFrame(root, text="Kết quả")
frame_result.pack(padx=10, pady=10, fill="both", expand=True)

columns_result = ("ID", "Waiting Time", "Turnaround Time")
result_tree = ttk.Treeview(frame_result, columns=columns_result, show="headings")
for col in columns_result:
    result_tree.heading(col, text=col)
    result_tree.column(col, width=100)
result_tree.pack(fill="both", expand=True)

gantt_frame = ttk.LabelFrame(root, text="Biểu đồ Gantt")
gantt_frame.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()
