import toml
from cryptography.fernet import Fernet
import base64
import os
import logging
from typing import Union, Optional

logger = logging.getLogger(__name__)


class TOMLCryptError(Exception):
    """Custom exception for TOML Crypt errors"""

    pass


def generate_key() -> str:
    """Generate a new encryption key"""
    logger.info("Generating new encryption key")
    return base64.urlsafe_b64encode(Fernet.generate_key()).decode()


def save_key(key: str, filename: str) -> None:
    """Save the encryption key to a file"""
    try:
        with open(filename, "w") as key_file:
            key_file.write(key)
        logger.info(f"Key saved to file: {filename}")
    except IOError as e:
        logger.error(f"Failed to save key to file: {filename}")
        raise TOMLCryptError(f"Failed to save key: {str(e)}")


def load_key(filename: str) -> str:
    """Load the encryption key from a file"""
    try:
        with open(filename, "r") as key_file:
            key = key_file.read().strip()
        logger.info(f"Key loaded from file: {filename}")
        return key
    except IOError as e:
        logger.error(f"Failed to load key from file: {filename}")
        raise TOMLCryptError(f"Failed to load key: {str(e)}")


def get_key_from_env(env_var_name: str) -> str:
    """Get the encryption key from an environment variable"""
    key = os.environ.get(env_var_name)
    if key:
        logger.info(f"Key loaded from environment variable: {env_var_name}")
        return key
    else:
        logger.warning(f"Key not found in environment variable: {env_var_name}")
        return None


def get_key(
    key: Optional[str] = None,
    key_file: Optional[str] = None,
    env_var_name: Optional[str] = None,
) -> str:
    """
    Get the encryption key from either a provided key, a key file, or an environment variable.
    Priority: provided key > key file > environment variable
    """
    if key is not None:
        logger.info("Using provided key")
        return key
    elif key_file is not None:
        return load_key(key_file)
    elif env_var_name is not None:
        return get_key_from_env(env_var_name)
    else:
        raise TOMLCryptError("No encryption key provided")


def encrypt_toml(
    input_file: str,
    output_file: str,
    key: Union[str, None] = None,
    key_file: Optional[str] = None,
) -> None:
    """Encrypt a TOML file"""
    try:
        encryption_key = get_key(key, key_file)

        with open(input_file, "r") as file:
            toml_data = toml.load(file)

        toml_string = toml.dumps(toml_data)

        f = Fernet(base64.urlsafe_b64decode(encryption_key))
        encrypted_data = f.encrypt(toml_string.encode())

        with open(output_file, "wb") as file:
            file.write(encrypted_data)

        logger.info(f"Encrypted {input_file} to {output_file}")
    except Exception as e:
        logger.error(f"Failed to encrypt {input_file}: {str(e)}")
        raise TOMLCryptError(f"Encryption failed: {str(e)}")


def decrypt_toml(
    input_file: str,
    output_file: str,
    key: Union[str, None] = None,
    key_file: Optional[str] = None,
) -> None:
    """Decrypt a TOML file"""
    try:
        decryption_key = get_key(key, key_file)

        with open(input_file, "rb") as file:
            encrypted_data = file.read()

        f = Fernet(base64.urlsafe_b64decode(decryption_key))
        decrypted_data = f.decrypt(encrypted_data)

        toml_data = toml.loads(decrypted_data.decode())

        with open(output_file, "w") as file:
            toml.dump(toml_data, file)

        logger.info(f"Decrypted {input_file} to {output_file}")
    except Exception as e:
        logger.error(f"Failed to decrypt {input_file}: {str(e)}")
        raise TOMLCryptError(f"Decryption failed: {str(e)}")
