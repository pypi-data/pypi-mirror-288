import os
import sys
from config_server_python_library import ConfigServerPythonClient

def main(config_server_url, application_name, profiles, commit_id, env_namespace, path_to_env_var_file):
    # Create a string to store all env variables
    client = ConfigServerPythonClient(config_server_url, application_name, profiles, commit_id, env_namespace, path_to_env_var_file)
    client.write_configs_to_file()

if __name__ == "__main__":

    if len(sys.argv) != 4:
        raise ValueError("Usage: python config_server_play_client.py <application_name> <profiles> <path_to_env_var_file>")

    config_server_url = os.environ.get("CONFIG_SERVER_URL")
    application_name = sys.argv[1]
    profiles = sys.argv[2].strip('[]').replace("'", "").split(', ')
    commit_id = os.environ.get("COMMIT_ID")
    env_namespace = os.environ.get("ENV_NAMESPACE")
    path_to_env_var_file = sys.argv[3]

    main(config_server_url, application_name, profiles, commit_id, env_namespace, path_to_env_var_file)