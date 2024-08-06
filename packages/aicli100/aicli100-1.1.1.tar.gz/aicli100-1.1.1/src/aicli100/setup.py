import subprocess
import sys
import time
from aicli100.post_install import create_config

def install_ollama(stdscr):
    if sys.platform == "linux":
        stdscr.clear()
        command = "curl -fsSL https://ollama.com/install.sh | sh"

        # Iniciar o processo
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        max_y, max_x = stdscr.getmaxyx()
        current_y = 0

        # Ler a saída linha por linha
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break

            # Atualizar a tela com a nova linha
            if current_y < max_y:
                stdscr.addstr(current_y, 0, line[: max_x - 1])
                current_y += 1
            else:
                stdscr.move(0, 0)
                stdscr.deleteln()
                stdscr.move(max_y, 0)
                stdscr.insertln()
                stdscr.addstr(max_y, 0, line[: max_x - 1])

            stdscr.refresh()

        # Aguardar o processo terminar
        process.wait()

        if process.returncode == 0:
            stdscr.clear()
            stdscr.addstr(1, 0, ">>> Ollama installed ✅")
            stdscr.refresh()
            time.sleep(2)
            return True
        else:
            raise subprocess.CalledProcessError(process.returncode, command)
    else:
        stdscr.addstr(1, 0, "Your PC does not support this application.")
        stdscr.refresh()
        stdscr.getch()
        return False


def check_ollama_installation(stdscr):
    try:
        if (
            subprocess.run(
                ["ollama", "--version"], stdout=subprocess.DEVNULL, check=True
            ).returncode
            == 0
        ):
            stdscr.addstr(3, 0, ">>> Ollama is installed ✅")
            stdscr.refresh()
            time.sleep(2)
        return True
    except FileNotFoundError:
        stdscr.clear()
        stdscr.addstr(1, 0, ">>> Ollama is not installed")
        stdscr.addstr(2, 0, ">>> Do you want to install it (y/n)?")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord("y"):
            installed = install_ollama(stdscr)
            if installed:
                return True
            else:
                return False
        else:
            stdscr.addstr(3, 0, "Press any key to leave...")
            stdscr.refresh()
            stdscr.getch()
            return False


def create_config_file():
    create_config()
