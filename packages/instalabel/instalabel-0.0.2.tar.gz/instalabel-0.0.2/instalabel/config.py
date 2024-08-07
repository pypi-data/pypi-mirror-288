import instalabel.client

API_URL = "https://sua4nhu6ze.execute-api.us-east-1.amazonaws.com/prod"
DEFAULT_CONFIG_PATH_SUFFIX = "/.config/instalabel/config.json"
INSTALABEL_CLIENT_CONFIGURATION = instalabel.client.Configuration(host=API_URL)
