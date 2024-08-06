import requests
import json
import configparser
import os
from openai import OpenAI

CONFIG_FILE = "~/.aicli_config.ini"
config = configparser.ConfigParser()
config.read(os.path.expanduser(CONFIG_FILE))


def stream_request_ollama(prompt: str, model: str) -> str:
    """
    Realiza uma requisição para o servidor Ollama e gera uma resposta em streaming.

    Esta função envia uma solicitação POST para o servidor Ollama local,
    utilizando o modelo e o prompt especificados. A resposta é retornada
    em formato de stream, permitindo o processamento de grandes respostas
    de forma eficiente.

    Args:
        prompt (str): O texto de entrada para o modelo de IA.
        model (str): O nome do modelo Ollama a ser utilizado.

    Yields:
        str: Fragmentos da resposta gerada pelo modelo, retornados
             à medida que são recebidos do servidor.

    Raises:
        requests.RequestException: Se ocorrer um erro na comunicação com o servidor.
        json.JSONDecodeError: Se a resposta do servidor não for um JSON válido.

    Note:
        Esta função assume que o servidor Ollama está rodando localmente
        na porta 11434. Certifique-se de que o servidor esteja ativo e
        acessível antes de chamar esta função.
    """
    response = requests.post(
        f"http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt},
        stream=True,
    )
    for line in response.iter_lines():
        if line:
            json_response = json.loads(line.decode("utf-8"))
            if "response" in json_response:
                chunk = json_response["response"]
                yield chunk


def get_models_list() -> list:
    import requests

    models_list = []
    if config.getboolean("USER_CFG", "ollama_installed"):
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            data = response.json()
            for model in data.get("models", []):
                models_list.append({"name": model["name"], "origin": "ollama"})

    if config.get("API_KEYS", "open_ai_api_key") != "":
        open_ai_client = OpenAI(api_key=config.get("API_KEYS", "open_ai_api_key"))
        data = open_ai_client.models.list()
        for model in data.data:
            models_list.append({"name": model.id, "origin": "openai"})
    
    if config.get("API_KEYS", "anthropic_api_key") != "":
        models_list.append({"name": "claude-3-opus-20240229", "origin": "anthropic"})
        models_list.append({"name": "claude-3-haiku-20240307", "origin": "anthropic"})
        models_list.append({"name": "claude-3-sonnet-20240229", "origin": "anthropic"})
        models_list.append(
            {"name": "claude-3-5-sonnet-20240620", "origin": "anthropic"}
        )
    return models_list


def list_ais_command():
    model_list = get_models_list()
    models_string = ""
    for model in model_list:
        if model["name"] == config.get("USER_CFG", "model"):
            models_string += f"{model['name']} - {model['origin']} (CURRENT)\n"
        else:
            models_string += f"{model['name']} - {model['origin']}\n"
    return f"Available models:\n{models_string}"


def set_model_command(user_input):
    user_input_splited = user_input.split(" ")
    model_list = get_models_list()
    model_list_names = [model["name"] for model in model_list]
    if len(user_input_splited) == 1:
        return "Error: Command incomplete. Use '/set-model <model>' to define the AI model."

    if user_input_splited[1] == "":
        return "Please, provide a model name"

    if user_input_splited[1] not in model_list_names:
        models_string = ""
        for model in model_list:
            if model["name"] == config.get("USER_CFG", "model"):
                models_string += f"{model['name']} - {model['origin']} (CURRENT)\n"
            else:
                models_string += f"{model['name']} - {model['origin']}\n"
        return f"ERROR: MODEL NOT FOUND\n\nAvailable models:\n{models_string}"

    config["USER_CFG"]["model"] = user_input_splited[1]

    config_file = os.path.expanduser(CONFIG_FILE)
    with open(config_file, "w") as configfile:
        config.write(configfile)

    return f"Model definied as {user_input_splited[1]}"


def stream_request_open_ai(prompt: str) -> str:
    client = OpenAI(api_key=config.get("API_KEYS", "open_ai_api_key"))
    response = client.chat.completions.create(
        model=config.get("USER_CFG", "model"),
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def handle_request_ai(prompt:str) -> str:
    model = config.get("USER_CFG", "model")
    models_list = get_models_list()
    for model in models_list:
        if model["name"] == config.get("USER_CFG", "model"):
            if model["origin"] == "openai":
                return stream_request_open_ai(prompt)
            elif model["origin"] == "ollama":
                return stream_request_ollama(prompt, model["name"])


def get_model_name() -> str:
    return config.get("USER_CFG", "model")