import requests
import os
import re

class FetchConfigFromServerException(Exception):
    def __init__(self, error, message="Failed to fetch property source from turtle-config-server"):
        self.message = message
        self.error = error
        super().__init__(f"{self.message}: {error}")

class UnresolvedPlaceholdersError(Exception):
    def __init__(self, unresolved_keys, message="Failed to resolve placeholders: Keys with unresolved placeholders"):
        self.message = message
        self.unresolved_keys = unresolved_keys
        super().__init__(f"{self.message}: {unresolved_keys}")

class ConfigServerPythonClient:

    def __init__(self, config_server_url, service_name, profiles, commit_id, env_namespace, path_to_env_var_file=None):
        """
        Initialize the ConfigServerPythonClient instance with configuration parameters.

        Args:
            config_server_url (str): The URL of the configuration server.
            service_name (str): The name of the service whose configuration is to be fetched.
            profiles (list): List of profiles to consider when fetching configuration.
            commit_id (str): Optional commit ID to fetch a specific version of configuration.
        """
        self.config_server_url = config_server_url
        self.service_name = service_name
        self.profiles = profiles
        self.commit_id = commit_id
        self.filtered_config_properties = {}
        self.total_config_properties = []
        self.unique_config_properties = {}
        self.resolved_config_properties = {}
        self.path_to_env_var_file = path_to_env_var_file
        self.env_namespace = env_namespace
        self.unresolved_keys = {}


    def _extract_required_properties(self):
        """
        Extract required properties based on the service name and update filtered_config_properties.
        """
        # Create a keyword based on the service name to match required configurations
        keyword = f'configurations/{self.service_name}'
        # Loop through each configuration source
        for config in self.total_config_properties:
            # Check if the keyword is present in the configuration source name
            if keyword in config["name"]:
                # Update filtered_config_properties with properties not already present
                self.filtered_config_properties.update({k: v for k, v in config["source"].items() if k not in self.filtered_config_properties})
        # Check if filtered_config_properties is still empty after the update
        if not self.filtered_config_properties:
            raise ValueError(f"No properties were found for the specified service: {self.service_name}")

    def _recursively_resolve_required_placeholders(self):
        """
        Recursively resolve placeholders within configuration values.
        """
        try:
            def _resolve_single_value_placeholders(value):
                # find placeholders using regex
                placeholders = re.findall(r"\${(.*?)}", str(value))
                for placeholder in placeholders:
                    # If the placeholder exists in unique_config_properties, replace it
                    if placeholder in self.unique_config_properties:
                        value = value.replace(f"${{{placeholder}}}", str(_resolve_single_value_placeholders(self.unique_config_properties[placeholder])))
                return value

            # Loop through unique_config_properties to resolve placeholders
            for key, value in self.filtered_config_properties.items():
                # If the value contains placeholders, resolve them using the helper function
                if "${" in str(value) and "}" in str(value):
                    self.resolved_config_properties[key] = _resolve_single_value_placeholders(value)
                else:
                    self.resolved_config_properties[key] = value
        except Exception as e:
            raise Exception(f"Failed to Recursively Resolve Required Placeholders: {e}")

    def _fetch_config_from_server(self):
        """
        Fetch configuration data from the configuration server using HTTP GET request.
        """
        # Create a comma-separated string of profiles
        profiles_string = ','.join(self.profiles)
        # Construct the API URL based on the provided parameters
        if self.commit_id.strip():
            config_server_api_url = f"{self.config_server_url}/{self.service_name}/{profiles_string}/{self.commit_id}"
        else:
            config_server_api_url = f"{self.config_server_url}/{self.service_name}/{profiles_string}"
        try:
            # Send an HTTP GET request to the configuration server API
            response = requests.get(config_server_api_url)
            # Parse the JSON response and extract the 'propertySources' field
            self.total_config_properties = response.json()['propertySources']
        except Exception as e:
            raise FetchConfigFromServerException(e)

    def __deduplicate_config_properties(self):
        """
        Deduplicate and merge configuration properties into unique_config_properties.
        """
        # Loop through each configuration source in total_config_properties
        for config in self.total_config_properties:
            # Loop through each key in the 'source' dictionary of the current config
            for key in config['source']:
                # Check if the key is not already present in unique_config_properties
                if key not in self.unique_config_properties:
                    # If not present, add the key-value pair to unique_config_properties
                    self.unique_config_properties[key] = config['source'][key]

    def _apply_namespace_to_config(self):
        """
        Add 'ENV_NAMESPACE' key with the value from the environment variable to configurations.
        """
        self.unique_config_properties['ENV_NAMESPACE'] = self.env_namespace

    def _fetch_and_merge_config(self):
        """
        Fetch, deduplicate, and apply namespace to configuration data.
        """
        self._fetch_config_from_server()
        self.__deduplicate_config_properties()
        self._apply_namespace_to_config()

    def _resolve_required_placeholders(self):
        """
        Resolve placeholders within configuration properties.
        """
        self._extract_required_properties()
        self._recursively_resolve_required_placeholders()
        self._check_unresolved_keys()


    def _check_unresolved_keys(self):
        # Find keys with unresolved placeholders
        self.unresolved_keys = [key for key, value in self.resolved_config_properties.items() if re.search(r"\${(.*?)}", str(value))]
        # Print keys with unresolved placeholders
        if self.unresolved_keys:
            print("Unresolved keys found: Moving ahead to writing resolved keys to env.")
            for key in self.unresolved_keys:
                del self.resolved_config_properties[key]
            # Raise custom exception if there are unresolved keys
            # raise UnresolvedPlaceholdersError(self.unresolved_keys)

    def _set_env_variables(self):
        """
        Set environment variables with resolved configuration properties.
        """
        for key, value in self.resolved_config_properties.items():
            os.environ[key] = str(value)
        print("Environment variables are set successfully")

    def _export_env_variables_to_file(self):
        """
        Export environment variables to a shell script file.
        """
        if self.path_to_env_var_file is None:
            raise ValueError("path_to_env_var_file is not specified. Please provide a valid file path.")
        # Create a string with export statements for each environment variable
        env_vars = ""
        for key, value in self.resolved_config_properties.items():
            env_vars += f'export {key}="{value}"\n'

        # Write the export statements to a shell script file
        with open(self.path_to_env_var_file, 'w') as file:
            file.write(env_vars)
        print("Environment variables are written successfully to shell.sh")

    def _get_env_variables(self):
        """
        Fetch and process configuration, resolving placeholders as necessary.
        """
        # Fetch and merge configuration data, and then resolve placeholders
        self._fetch_and_merge_config()
        self._resolve_required_placeholders()

    def write_configs_to_env(self):
        """
        Fetch configuration properties and set them as environment variables for the Python client.

        This function performs the following steps:
        1. Fetches and processes configuration data.
        2. Resolves placeholders within configuration properties.
        3. Sets environment variables with the resolved configuration properties.

        Raises:
            Exception: If any step in the process fails.
        """
        try:
            print("Write Config to Env: Started")
            # Get environment variables and set them for the Python client
            self._get_env_variables()
            self._set_env_variables()
            print("Write Config to Env: Finished Successfully")
            if self.unresolved_keys:
                raise UnresolvedPlaceholdersError(self.unresolved_keys)
        except UnresolvedPlaceholdersError as e:
            raise e
        except Exception as e:
            print(f"Write Config to Env: Failed: {e}")
            raise e

    def write_configs_to_file(self):
        """
        Fetch configuration properties and export them to a shell script file for the Play client.

        This function performs the following steps:
        1. Fetches and processes configuration data.
        2. Resolves placeholders within configuration properties.
        3. Exports environment variables to a shell script file for the Play client.

        Raises:
            Exception: If any step in the process fails.
        """
        try:
            print("Write Config to File: Started")
            # Get environment variables and export them to a file for the Play client
            self._get_env_variables()
            self._export_env_variables_to_file()
            print("Write Config to File: Finished Successfully")
            if self.unresolved_keys:
                raise UnresolvedPlaceholdersError(self.unresolved_keys)
        except UnresolvedPlaceholdersError as e:
            raise e
        except Exception as e:
            print(f"Write Config to File: Failed: {e}")
            raise e
