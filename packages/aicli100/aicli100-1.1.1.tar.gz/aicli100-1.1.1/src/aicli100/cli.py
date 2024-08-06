import configparser
import os
import time
import curses
from aicli100.setup import check_ollama_installation
import sys
from aicli100.ai import (
    set_model_command,
    list_ais_command,
    handle_request_ai,
    get_model_name,
)

CONFIG_FILE = "~/.aicli_config.ini"
screen = None
buffer = []
scroll_position = 0
max_y, max_x = 0, 0
user_input = ""
current_y = 0
current_x = 4


def help_text_command():
    global current_y, current_x, screen
    add_line("Commands:")
    add_line("/? or /help to show this help")
    add_line("/exit to exit")
    add_line("/clear to clear the screen")
    add_line("/keys-check show check api keys")
    add_line("/key-set open_ai <api_key> to set openai api key")
    add_line("/key-set anthropic <api_key> to set anthropic api key")
    add_line("/set-model <model> to set the model")
    add_line("/models to list the models")
    current_y += 9


def clear_screen_command():
    global buffer, scroll_position, current_y, current_x, screen
    buffer = []
    screen.clear()
    scroll_position = 0
    show_header()


def check_api_keys_command():
    import os

    global current_y, current_x, screen
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_FILE))

    if config.get("API_KEYS", "OPEN_AI_API_KEY") == "":
        add_line("Not set OPENAI")
        current_y += 1
    elif config.get("API_KEYS", "OPEN_AI_API_KEY") != "":
        add_line("OPENAI_API_KEY ✅")
        current_y += 1

    if config.get("API_KEYS", "anthropic_api_key") == "":
        add_line("Not set ANTHROPIC")
        current_y += 1
    elif config.get("API_KEYS", "anthropic_api_key") != "":
        add_line("anthropic_api_key ✅")
        current_y += 1

    refresh_screen()


def keys_set_command(user_input):
    import os

    global current_y, current_x, screen
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_FILE))

    if "API_KEYS" not in config:
        config.add_section("API_KEYS")

    user_input_splited = user_input.split(" ")
    if user_input_splited[1] == "open_ai" and len(user_input_splited) == 3:
        add_line(f"OpenAI API Key set to: {user_input_splited[2]} ✅")
        config.set("API_KEYS", "open_ai_api_key", user_input_splited[2])
        config_file = os.path.join(os.path.expanduser("~"), ".aicli_config.ini")
        with open(config_file, "w") as configfile:
            config.write(configfile)
        current_y += 1
        refresh_screen()


def handle_command(user_input):
    global current_y, current_x, screen
    if user_input == "/?" or user_input == "/help":
        user_input = ""
        help_text_command()

    elif user_input == "/exit":
        sys.exit()

    elif user_input == "/clear":
        user_input = ""
        clear_screen_command()

    elif user_input == "/keys-check":
        user_input = ""
        check_api_keys_command()

    elif user_input.startswith("/key-set"):
        keys_set_command(user_input)
        user_input = ""

    elif user_input.startswith("/set-model"):
        output = set_model_command(user_input)
        if output is not None:
            add_line(output)
        user_input = ""

    elif user_input == "/models":
        output = list_ais_command()
        if output is not None:
            add_line(output)
        user_input = ""

    else:
        add_line("Command not found type /? for help")
        current_y += 1
        refresh_screen()


def check_cfg(stdscr) -> None:
    """Check if the config file exists, if not, create it and set the first_use to 1"""
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_FILE))
    if config.getboolean("USER_CFG", "ollama_installed"):
        return

    if config.getboolean("USER_CFG", "FIRST_USE"):
        stdscr.addstr(1, 0, ">>> First use detected...")
        stdscr.refresh()
        time.sleep(1)
        stdscr.addstr(2, 0, ">>> Checking ollama installation...")
        stdscr.refresh()
        time.sleep(1)
        installed = check_ollama_installation(stdscr)
        if installed:
            config.set("USER_CFG", "FIRST_USE", "0")
            config.set("USER_CFG", "ollama_installed", "1")
            with open(os.path.expanduser(CONFIG_FILE), "w") as configfile:
                config.write(configfile)


def start(stdscr):
    global max_y, max_x
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()

    check_cfg(stdscr)


def show_header():
    global current_y, current_x, screen
    add_line(
        r"""
 ________  ___          ________  ___       ___     
|\   __  \|\  \        |\   ____\|\  \     |\  \    
\ \  \|\  \ \  \       \ \  \___|\ \  \    \ \  \   
 \ \   __  \ \  \       \ \  \    \ \  \    \ \  \  
  \ \  \ \  \ \  \       \ \  \____\ \  \____\ \  \ 
   \ \__\ \__\ \__\       \ \_______\ \_______\ \__\
    \|__|\|__|\|__|        \|_______|\|_______|\|__|
"""
    )
    add_line("/? or /help for help")
    add_line(f"Current model: {get_model_name()}")


def initialize_screen(stdscr):
    global current_y, current_x, screen, max_y, max_x, user_input
    start(stdscr)
    screen = stdscr
    curses.curs_set(0)
    screen.clear()
    show_header()
    refresh_screen()


def add_line(text):
    global buffer, scroll_position, max_y, current_y
    lines = text.split("\n")
    for line in lines:
        trimmed_line = line.rstrip()
        if trimmed_line:
            buffer.append(trimmed_line)
        else:
            buffer.append("")
    if len(buffer) > max_y - 1:
        scroll_position = len(buffer) - (max_y - 1)
    refresh_screen()


def refresh_screen():
    global screen, buffer, scroll_position, max_y, max_x, user_input, current_y, current_x
    screen.clear()
    display_range = min(max_y - 2, len(buffer) - scroll_position)
    for i in range(display_range):
        try:
            screen.addstr(i, 0, buffer[i + scroll_position][: max_x - 1])
        except curses.error:
            pass  # Ignora erros de escrita fora da tela

    prompt = ">>> "
    input_display = user_input[: max_x - len(prompt) - 1]
    try:
        screen.addstr(max_y - 1, 0, prompt + input_display)
    except curses.error:
        pass  # Ignora erros de escrita fora da tela

    current_y = max_y - 1
    current_x = len(prompt) + len(input_display)
    try:
        screen.move(current_y, current_x)
    except curses.error:
        raise Exception(f"Error moving cursor to position {current_y}, {current_x}")
    screen.refresh()


def handle_scroll(direction):
    global scroll_position, buffer, max_y
    if direction > 0 and scroll_position > 0:
        scroll_position = max(0, scroll_position - 1)
    elif direction < 0 and scroll_position < len(buffer) - (max_y - 2):
        scroll_position = min(len(buffer) - (max_y - 2), scroll_position + 1)
    refresh_screen()


def add_input_line():
    global current_y, current_x, screen
    add_line(">>>")
    current_x = 4


def add_response_from_ai(chunk: str):
    global current_y, current_x, screen, max_y, max_x, buffer, scroll_position, current_line_size
    if current_line_size + len(chunk) < max_x - 1:
        if chunk.endswith("\n"):
            current_line_size = 0
            buffer.append("")
        else:
            current_line_size += len(chunk)
            buffer[-1] += chunk
    else:
        current_line_size = 0
        buffer.append(chunk)
    refresh_screen()


def input_bar():
    global current_y, current_x, buffer, scroll_position, max_y, max_x, user_input, screen, current_line_size
    user_input = ""
    curses.curs_set(1)
    refresh_screen()
    while True:
        # Captura a entrada do usuário
        while True:
            try:
                key = screen.getch()
            except KeyboardInterrupt:
                sys.exit()
            if key == ord("\n"):  # Enter pressionado
                current_y += 1  # Desce uma linha
                if user_input.startswith("/"):
                    handle_command(user_input)
                else:
                    current_x = 1  # Seta inicio de resposta
                    current_line_size = 0
                    for chunk in handle_request_ai(user_input):
                        add_response_from_ai(chunk)
                current_y = max_y - 1
                current_x = 4
                break  # Sai apenas do loop interno

            elif key == curses.KEY_BACKSPACE or key == 127:  # Backspace
                if current_x > 4:
                    user_input = user_input[:-1]
                    current_x -= 1
                    screen.delch(current_y, current_x)

            # HANDLE SCROLL
            elif key == curses.KEY_UP:
                handle_scroll(1)
            elif key == curses.KEY_DOWN:
                handle_scroll(-1)

            elif 32 <= key <= 126:  # Caracteres imprimíveis
                if current_x < max_x - 1:
                    user_input += chr(key)
                    screen.addch(current_y, current_x, key)
                    current_x += 1
                else:
                    # Move o prompt para a linha de cima
                    current_y -= 1
                    if current_y < max_y - 1:
                        screen.insertln()
                    if current_y == max_y - 2:
                        screen.addstr(current_y, 0, ">>> " + user_input)
                        current_y = max_y - 1
                    user_input += chr(key)
                    current_x = 0  # Reinicia a posição X após o prompt

        refresh_screen()
        if user_input != "":
            break

    return user_input
