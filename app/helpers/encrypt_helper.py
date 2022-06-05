from typing import overload

from app.core.config import settings
from cryptography.fernet import Fernet


def str_to_bytes(value: str) -> bytes:
    return value.encode('utf-8')


def bytes_to_str(value: bytes) -> str:
    return value.decode('utf-8')


fernet = Fernet(settings.SECRET_KEY)


class EncryptHelper:
    @overload
    @staticmethod
    def encrypt(data: str) -> str: ...

    @overload
    @staticmethod
    def encrypt(data: bytes) -> bytes: ...

    @staticmethod
    def encrypt(data):
        if type(data) is str:
            byte_data = str_to_bytes(data)
            encrypted_byte_data = fernet.encrypt(byte_data)
            return bytes_to_str(encrypted_byte_data)

        if type(data) is bytes:
            return fernet.encrypt(data)

        raise TypeError(
            f'Only accepted `bytes` or `str` type. (passed: {type(data)})')

    @overload
    @staticmethod
    def decrypt(data: str) -> str: ...

    @overload
    @staticmethod
    def decrypt(data: bytes) -> bytes: ...

    @staticmethod
    def decrypt(data):
        if type(data) is str:
            byte_data = str_to_bytes(data)
            decrypted_byte_data = fernet.decrypt(byte_data)
            return bytes_to_str(decrypted_byte_data)

        if type(data) is bytes:
            return fernet.decrypt(data)

        raise TypeError(
            f'Only accepted `bytes` or `str` type. (passed: {type(data)})')
