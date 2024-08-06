# aicli100

AICLI100 is a command line interface for using AI.

## Features

- **Install and Check Ollama**: Automatically installs and checks the Ollama AI tool on Linux systems.
- **API Key Management**: Easily set and check API keys for OpenAI and Anthropic.
- **Model Management**: List available AI models and set the desired model for AI requests.
- **Command Line Interface**: Interact with the AI directly from the terminal using simple commands.

## Installation
### Using git
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/aicli.git
   cd aicli
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Build the project:
   ```sh
   python -m build
   ```

### Using pip

1. Install the package:
   ```sh
   pip install aicli100
   ```
2. Run the app:
   ```sh
   aicli100
   ```

## Usage

1. Run the CLI application:
   ```sh
   python src/main.py
   ```

2. Use the following commands within the CLI:
   - `/help` or `/?`: Show help text.
   - `/exit`: Exit the application.
   - `/clear`: Clear the screen.
   - `/keys-check`: Check the status of API keys.
   - `/key-set open_ai <api_key>`: Set the OpenAI API key.
   - `/key-set anthropic <api_key>`: Set the Anthropic API key.
   - `/set-model <model>`: Set the AI model.
   - `/models`: List available AI models.

## Configuration

The configuration file is located at `~/.aicli_config.ini`. It stores API keys and user settings.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Author

Roberto Fernandino - [romfernandino@gmail.com](mailto:romfernandino@gmail.com)

## Acknowledgements

- [Ollama](https://ollama.com)
- [OpenAI](https://openai.com)
- [Anthropic](https://www.anthropic.com)