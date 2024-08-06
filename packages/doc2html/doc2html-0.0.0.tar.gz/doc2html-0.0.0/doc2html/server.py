from time import sleep
import socket
import subprocess

from . import config as cfg


def is_unoserver_running(
        interface: str = cfg.TRANSFORM_HOST,
        port: int = cfg.UNOSERVER_PORT, timeout: int = 20) -> bool:
    """Check if the server is already running by trying to establish a socket connection."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((interface, int(port)))
            return True
        except (ConnectionRefusedError, socket.timeout):
            return False


def sync_start_uno_server(interface=cfg.TRANSFORM_HOST, port=cfg.UNOSERVER_PORT, executable_path=None) -> bool:
    """Synchronously starts unoserver"""
    if is_unoserver_running(interface=interface, port=port):
        cfg.logger.info("Unoserver is already running.")
        return True

    # Construct the command to start the unoserver using the specified Python interpreter.
    cmd = [cfg.UNO_PYTHON, "-m", "unoserver.server", "--interface", interface, "--port", str(port)]

    if executable_path:
        cmd.extend(["--executable", executable_path])

    try:
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        # Optionally, wait for a few seconds to allow the server to start.
        # This step can be adjusted or removed based on your needs.
        sleep(15)

        # Optionally, check the first few lines of output (useful for debugging).
        # output, _ = process.communicate(timeout=10)  # This line captures output for the given timeout.

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex((cfg.TRANSFORM_HOST, cfg.UNOSERVER_PORT))

        port_in_use = result == 0

        # if "some expected output" in output.decode('utf-8'):
        #     cfg.logger.info("Started unoserver successfully.")
        #     return True
        # else:
        #     cfg.logger.warning("Unexpected output from unoserver. You might want to check this.")
        #     return False

        if port_in_use:
            cfg.logger.info("Started unoserver successfully.")
            return True
        else:
            cfg.logger.warning("Unexpected output from unoserver. You might want to check this.")
            return False

    except Exception as err:
        cfg.logger.error(f"Failed to start unoserver. Error: {str(err)}")
        raise Exception(f"Failed to start unoserver. Error: {str(err)}")


async def start_unoserver(interface=cfg.TRANSFORM_HOST, port=cfg.UNOSERVER_PORT, executable_path=None) -> bool:
    """Asynchronously starts unoserver"""
    return sync_start_uno_server(interface=interface, port=port, executable_path=executable_path)


async def handle_start_unoserver() -> None:
    """Initialization of Unoserver with exception management"""
    try:
        is_active = await start_unoserver()
    except Exception as err:
        error_message = str(err)
        if "timed out after 10 seconds" in error_message:
            raise Exception("Server initialization ongoing. Please try again later.") from None
        else:
            raise Exception(f"An unexpected error occurred: {error_message}") from None

    if not is_active:
        raise Exception("Unoserver failed to start")


def allocate_unoserver_environment() -> None:
    """Run the script for Unoserver environment allocation"""
    rc = subprocess.call("./doc2html/allocate_unoserver.sh")
    if rc == 0:
        cfg.logger.info("Environment allocation finished.")
    else:
        cfg.logger.error("Something went wrong while allocating Unoserver environment.")
