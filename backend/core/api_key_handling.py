# Encryption, storing and retrieval of api_key functions
import keyring


def set_api_key(api_key: str):
    SERVICE_NAME = "Friday_AI"
    ACCOUNT_NAME = "groq_api_key"
    return keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, api_key)


def get_api_key():
    SERVICE_NAME = "Friday_AI"
    ACCOUNT_NAME = "groq_api_key"
    return keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)


def clear_api_key():
    SERVICE_NAME = "Friday_AI"
    ACCOUNT_NAME = "groq_api_key"
    try:
        keyring.delete_password(SERVICE_NAME, ACCOUNT_NAME)
    except keyring.errors.PasswordDeleteError:
        raise