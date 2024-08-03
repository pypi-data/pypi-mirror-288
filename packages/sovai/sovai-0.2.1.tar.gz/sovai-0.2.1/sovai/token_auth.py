from sovai.api_config import ApiConfig, save_key


def token_auth(token: str):
    ApiConfig.token = token
    ApiConfig.token_type = "Bearer"
    save_key()
