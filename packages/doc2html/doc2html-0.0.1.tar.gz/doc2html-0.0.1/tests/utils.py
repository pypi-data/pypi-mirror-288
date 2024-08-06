import psutil


def find_and_kill_process_by_port(port: int):
    try:
        # Iterate over all running processes
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port:
                # Get the process ID (pid)
                pid = conn.pid
                if pid is not None:
                    process = psutil.Process(pid)
                    print(f"Killing process '{process.name()}' with PID {pid} running on port {port}...")
                    process.terminate()  # Send termination signal
                    return True

        print(f"No process found running on port {port}.")
        return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
