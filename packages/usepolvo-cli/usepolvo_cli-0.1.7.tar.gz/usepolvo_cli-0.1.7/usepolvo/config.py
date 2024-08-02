import configparser
import os

from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

CONFIG_FILE_PATH = os.path.expanduser("~/.usepolvo_cli_config")

config = configparser.ConfigParser()


def load_config():
    if os.path.exists(CONFIG_FILE_PATH):
        config.read(CONFIG_FILE_PATH)


def save_config(integration, api_key):
    load_config()
    if integration not in config:
        config[integration] = {}
    config[integration]["API_KEY"] = api_key
    with open(CONFIG_FILE_PATH, "w") as configfile:
        config.write(configfile)


def get_api_key(integration):
    load_config()
    env_var = f"{integration.upper()}_API_KEY"
    api_key = os.getenv(env_var)

    if api_key:
        # Save the API key to the config file
        save_config(integration, api_key)
        return api_key

    # If the API key is not in the environment variable, get it from the config file
    return config[integration].get("API_KEY", None) if integration in config else None
