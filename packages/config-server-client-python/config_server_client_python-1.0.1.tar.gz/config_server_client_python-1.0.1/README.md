#config-server-client-python

Streamline configuration management by fetching and updating configurations from a sping-cloud-config-server in Python.

#How to use config-serve-client-python package in django/flask framework.

Within the repository, we maintain clients for Python Framework. The Python client is responsible for retrieving configurations from the Spring Cloud Config Server and seamlessly integrating them as environment variables within the container.


#Python sping-cloud-config-server client

1} Add config-server-client-python package to requirements.txt
```
config-server-client-python==<version_no>
```
2} In manage.py import ConfigServerPythonClient as given below.
```
from src.config_server_python_library import ConfigServerPythonClient
```
3} Initiate ConfigServerPythonClient function in __main__. 
```
client = ConfigServerPythonClient(os.getenv('CONFIG_SERVER_URL'), <service-name>, <profile-list>, os.getenv('COMMIT_ID'), os.getenv('ENV_NAMESPACE'))
client.write_configs_to_env()
```


#How to push a new version of config-server-client-python to nexus:

1} Clone config-server-client-python repo.

```
git clone https://github.com/jayantreddy181198/config-server-client-python.git <destination_path>/config-server-client-python
```

2} Install twine and setuptools from pypi if not exists already.
```
pip install twine setuptools
```

3} Navigate to config-server-client-python repo.
```
cd <destination_path>/config-server-client-python
```

4} Make the required changes and update the version in setup.py

5} RUN below command to create sdist.
```
python setup.py sdist bdist_wheel
```

6} Upload package to nexus.
```
twine upload --repository pypi-release dist/*
```
