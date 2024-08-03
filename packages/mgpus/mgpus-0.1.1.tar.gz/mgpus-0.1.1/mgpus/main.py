import click
import psutil
import pynvml
from rich.console import Console
from rich.table import Table


@click.command()
def cli():
    # Initialize NVML
    pynvml.nvmlInit()

    # Get the number of GPUs
    device_count = pynvml.nvmlDeviceGetCount()

    gpu_data = {f"GPU {i}": [] for i in range(device_count)}
    gpu_total_memory = {f"GPU {i}": pynvml.nvmlDeviceGetMemoryInfo(pynvml.nvmlDeviceGetHandleByIndex(i)).total / 1024 / 1024 / 1024 for i in range(device_count)}

    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)

        # Get processes running on the GPU
        processes = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)

        for process in processes:
            try:
                process_info = psutil.Process(process.pid)
                process_name = process_info.cmdline()
                process_name = ' '.join(process_name) if process_name else "Unknown"
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                process_name = "Unknown"
            
            memory_usage_gb = process.usedGpuMemory / 1024 / 1024 / 1024
            gpu_data[f"GPU {i}"].append(f"{process_name} (PID {process.pid}), {memory_usage_gb:.2f} GB")

    # Find the maximum number of processes in any GPU column for consistent table formatting
    max_rows = max(len(v) for v in gpu_data.values())

    for k in gpu_data:
        gpu_data[k].extend([""] * (max_rows - len(gpu_data[k])))

    print_gpu_processes_table(gpu_data, gpu_total_memory)
    return gpu_data, gpu_total_memory

def print_gpu_processes_table(gpu_data, gpu_total_memory) -> None:
    console = Console()
    num_gpus = len(gpu_data)
    columns_per_row = 4

    for i in range(0, num_gpus, columns_per_row):
        table = Table(show_header=True, header_style="bold magenta")
        subset_gpu_data = {k: gpu_data[k] for k in list(gpu_data.keys())[i:i+columns_per_row]}
        
        columns = list(subset_gpu_data.keys())
        for column in columns:
            table.add_column(column)

        rows = list(zip(*subset_gpu_data.values(), strict=False))
        for row in rows:
            table.add_row(*row)

        total_row = [f"{sum(float(proc.split()[-2]) for proc in col if proc):.0f}/{gpu_total_memory[k]:.0f} GB" for k, col in subset_gpu_data.items()]
        table.add_row(*total_row, style="bold yellow")

        console.print(table)


if __name__ == "__main__":
    gpu_data, gpu_total_memory = cli()
    print_gpu_processes_table(gpu_data, gpu_total_memory)