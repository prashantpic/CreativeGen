"""
Implementation of ITokenEncryptionService using AES-GCM.
"""
import base64
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from ....application.exceptions import TokenEncryptionError
from ....domain.services.token_encryption_service import ITokenEncryptionService


class AESGCMTokenEncryptionService(ITokenEncryptionService):
    """
    Provides AES-GCM encryption and decryption for sensitive tokens.
    Implements the ITokenEncryptionService interface.
    """
    _NONCE_SIZE = 12
    _TAG_SIZE = 16

    def __init__(self, aes_key_b64: str):
        """
        Initializes the encryption service.

        Args:
            aes_key_b64: A base64 encoded string representing the 32-byte AES key.

        Raises:
            ValueError: If the decoded key is not 32 bytes.
        """
        try:
            self.key = base64.b64decode(aes_key_b64)
            if len(self.key) != 32:
                raise ValueError("AES_KEY must be 32 bytes long.")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid AES_KEY configuration: {e}") from e

    def encrypt_token(self, token: str) -> bytes:
        """
        Encrypts a plaintext token using AES-GCM.

        Generates a unique nonce for each encryption, prepends it to the
        ciphertext, and appends the authentication tag.

        Args:
            token: The plaintext token string to encrypt.

        Returns:
            The encrypted data as bytes, in the format: nonce + ciphertext + tag.
        """
        aesgcm = AESGCM(self.key)
        nonce = os.urandom(self._NONCE_SIZE)
        plaintext_bytes = token.encode("utf-8")
        
        try:
            ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)
            # The ciphertext from cryptography lib already contains the auth tag.
            return nonce + ciphertext
        except Exception as e:
            # Broad exception to catch any potential issue during encryption
            raise TokenEncryptionError(f"Failed to encrypt token: {e}") from e

    def decrypt_token(self, encrypted_data: bytes) -> str:
        """
        Decrypts an encrypted token that was encrypted with AES-GCM.

        Args:
            encrypted_data: The encrypted bytes, expected to be in the format:
                            nonce + ciphertext + tag.

        Returns:
            The decrypted plaintext token string.

        Raises:
            TokenEncryptionError: If decryption fails due to tampering,
                                  incorrect key, or malformed data.
        """
        if len(encrypted_data) < self._NONCE_SIZE + self._TAG_SIZE:
             raise TokenEncryptionError("Invalid encrypted data format: too short.")

        aesgcm = AESGCM(self.key)
        nonce = encrypted_data[:self._NONCE_SIZE]
        ciphertext_with_tag = encrypted_data[self._NONCE_SIZE:]
        
        try:
            decrypted_bytes = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
            return decrypted_bytes.decode("utf-8")
        except InvalidTag:
            raise TokenEncryptionError(
                "Failed to decrypt token: Invalid authentication tag. "
                "Data may have been tampered with or the key is incorrect."
            )
        except Exception as e:
            raise TokenEncryptionError(f"An unexpected error occurred during decryption: {e}") from e