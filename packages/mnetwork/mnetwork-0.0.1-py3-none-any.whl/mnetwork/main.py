import subprocess
from pathlib import Path

from click import command, option
from rich.console import Console
from rich.table import Table


@command()
@option('--all', is_flag=True, help='See all processes.')
@option('--include-ports', "-i", default='', help='Comma-separated list of ports to include.')
@option('--exclude-ports', "-x", default='', help='Comma-separated list of ports to exclude.')
@option('--page', is_flag=True, help='Page the output.')
def cli(all, include_ports, exclude_ports, page) -> None:
    include_ports = set(include_ports.split(',')) if include_ports else set()
    exclude_ports = set(exclude_ports.split(',')) if exclude_ports else set()

    output = subprocess.check_output(["lsof", "-i", "-P", "-n"], text=True)
    lines = output.splitlines()[1:]  # Skip the header line

    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("PID", style="dim cyan")
    table.add_column("Process Name", style="bold green")
    table.add_column("Port", style="bold yellow")
    table.add_column("Path")
    table.add_column("Command Line", style="blue")

    data = {}

    for line in lines:
        parts = line.split()
        if len(parts) > 8 and ':' in parts[8]:
            pid = parts[1]
            process_name = parts[0]
            port = parts[8].split(':')[-1]
            if (include_ports and port not in include_ports) or (exclude_ports and port in exclude_ports):
                    continue
            path = subprocess.check_output(["readlink", f"/proc/{pid}/exe"], text=True).strip()
            with Path(f"/proc/{pid}/cmdline").open() as f:
                cmdline = f.read().replace('\x00', ' ')
            key = (port, process_name) if not all else (port, process_name, pid)
            
            data[key] = [(pid, path, cmdline)]

    for (port, process_name), processes in data.items():
        for pid, path, cmdline in processes:
            table.add_row(pid, process_name, port, f"[link=file://{path}]{path}[/link]", cmdline)

    console = Console()
    if page:
        with console.pager(styles=True):
            console.print(table)
    else:
        console.print(table)

if __name__ == '__main__':
    cli()