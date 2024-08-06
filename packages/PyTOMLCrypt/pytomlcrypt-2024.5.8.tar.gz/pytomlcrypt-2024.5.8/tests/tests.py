import pytest
import tempfile
import os
import sys

sys.path.append("./")
from PyTOMLCrypt import (
    generate_key,
    save_key,
    load_key,
    get_key_from_env,
    get_key,
    encrypt_toml,
    decrypt_toml,
    TOMLCryptError,
)


@pytest.fixture
def key():
    return generate_key()


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture
def key_file(temp_dir, key):
    filename = os.path.join(temp_dir, "secret.key")
    save_key(key, filename)
    return filename


def test_key_generation(key):
    assert isinstance(key, str)


def test_key_save_load(key, key_file):
    loaded_key = load_key(key_file)
    assert key == loaded_key


def test_key_from_env(key, monkeypatch):
    monkeypatch.setenv("TOML_CRYPT_KEY", key)
    assert get_key_from_env("TOML_CRYPT_KEY") == key


def test_get_key(key, key_file, monkeypatch):
    # Test with provided key
    assert get_key(key=key) == key

    # Test with key file
    assert get_key(key_file=key_file) == key

    # Test with environment variable
    monkeypatch.setenv("TOML_CRYPT_KEY", key)
    assert get_key(env_var_name="TOML_CRYPT_KEY") == key

    # Test with no key available
    monkeypatch.delenv("TOML_CRYPT_KEY", raising=False)
    with pytest.raises(TOMLCryptError):
        get_key()


def test_encrypt_decrypt(key, temp_dir):
    input_data = """
[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00
    """

    input_file = os.path.join(temp_dir, "input.toml")
    with open(input_file, "w") as f:
        f.write(input_data)

    encrypted_file = os.path.join(temp_dir, "encrypted.bin")
    decrypted_file = os.path.join(temp_dir, "decrypted.toml")

    # Test encryption and decryption with provided key
    encrypt_toml(input_file, encrypted_file, key=key)
    decrypt_toml(encrypted_file, decrypted_file, key=key)

    with open(decrypted_file, "r") as f:
        decrypted_data = f.read()

    assert input_data.strip() == decrypted_data.strip()


def test_encrypt_decrypt_with_key_file(key, temp_dir, key_file):
    input_data = """
[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00
    """

    input_file = os.path.join(temp_dir, "input.toml")
    with open(input_file, "w") as f:
        f.write(input_data)

    encrypted_file = os.path.join(temp_dir, "encrypted.bin")
    decrypted_file = os.path.join(temp_dir, "decrypted.toml")

    # Test encryption and decryption with key file
    encrypt_toml(input_file, encrypted_file, key_file=key_file)
    decrypt_toml(encrypted_file, decrypted_file, key_file=key_file)

    with open(decrypted_file, "r") as f:
        decrypted_data = f.read()

    assert input_data.strip() == decrypted_data.strip()


def test_encryption_error(key, temp_dir):
    non_existent_file = os.path.join(temp_dir, "non_existent.toml")
    output_file = os.path.join(temp_dir, "output.bin")

    with pytest.raises(TOMLCryptError):
        encrypt_toml(non_existent_file, output_file, key=key)


def test_decryption_error(key, temp_dir):
    invalid_file = os.path.join(temp_dir, "invalid.bin")
    with open(invalid_file, "wb") as f:
        f.write(b"invalid data")

    output_file = os.path.join(temp_dir, "output.toml")

    with pytest.raises(TOMLCryptError):
        decrypt_toml(invalid_file, output_file, key=key)
