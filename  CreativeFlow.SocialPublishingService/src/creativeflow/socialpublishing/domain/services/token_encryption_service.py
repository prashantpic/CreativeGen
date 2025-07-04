"""
Interface for encrypting and decrypting sensitive tokens.
"""
from abc import ABC, abstractmethod


class ITokenEncryptionService(ABC):
    """
    Defines the contract for encrypting and decrypting OAuth tokens.
    This decouples the domain from specific encryption algorithms.
    """

    @abstractmethod
    def encrypt_token(self, token: str) -> bytes:
        """
        Encrypts a plaintext token.

        Args:
            token: The plaintext token string.

        Returns:
            The encrypted token as bytes.
        """
        raise NotImplementedError

    @abstractmethod
    def decrypt_token(self, encrypted_token: bytes) -> str:
        """
        Decrypts an encrypted token.

        Args:
            encrypted_token: The encrypted token as bytes.

        Returns:
            The decrypted plaintext token string.
        """
        raise NotImplementedError