"""
AES-256 Encryption Module with HMAC for Authentication

Implements end-to-end symmetric encryption using:
- AES-256-CBC for encryption
- HMAC-SHA256 for message authentication
- Random IV for each message
"""

import os
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode


class SecureEncryption:
    """
    AES-256 Encryption Manager with HMAC Authentication
    
    Attributes:
        key (bytes): AES-256 key (32 bytes)
        hmac_key (bytes): Key for HMAC (derived from main key)
    """
    
    def __init__(self, shared_key: bytes):
        """
        Initialize encryption manager
        
        Args:
            shared_key (bytes): Shared key (minimum 32 bytes for AES-256)
            
        Raises:
            ValueError: If key is too short
        """
        if len(shared_key) < 32:
            raise ValueError("Key must be at least 32 bytes for AES-256")
        
        # Use only first 32 bytes
        self.key = shared_key[:32]
        
        # Derive HMAC key using main key
        self.hmac_key = hashlib.sha256(self.key + b"hmac").digest()
        
        print(f"[✓] AES-256 Encryption initialized successfully")
    
    def encrypt(self, message: str) -> str:
        """
        Encrypts a message with AES-256-CBC
        
        Process:
        1. Generate random IV (16 bytes)
        2. Encrypt message with AES-256-CBC
        3. Calculate HMAC for authentication
        4. Return: IV + HMAC + Ciphertext (base64)
        
        Args:
            message (str): Plaintext message
            
        Returns:
            str: Encrypted message in base64 (IV + HMAC + cipher)
        """
        # Convert message to bytes
        plaintext = message.encode('utf-8')
        
        # Generate random IV (16 bytes)
        iv = os.urandom(16)
        
        # Create AES-256-CBC cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Apply PKCS7 padding (AES works with 16-byte blocks)
        padded_plaintext = self._pkcs7_pad(plaintext)
        
        # Encrypt
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        
        # Calculate HMAC for integrity verification
        hmac_obj = hmac.new(
            self.hmac_key,
            iv + ciphertext,
            hashlib.sha256
        )
        hmac_digest = hmac_obj.digest()
        
        # Combine: IV + HMAC + Ciphertext and encode in base64
        encrypted_data = iv + hmac_digest + ciphertext
        encoded = b64encode(encrypted_data).decode('utf-8')
        
        return encoded
    
    def decrypt(self, encrypted_message: str) -> str:
        """
        Decrypts an AES-256-CBC message
        
        Process:
        1. Decode from base64
        2. Extract IV (first 16 bytes)
        3. Extract HMAC (next 32 bytes)
        4. Extract Ciphertext (rest)
        5. Verify HMAC
        6. Decrypt with AES-256-CBC
        7. Remove padding
        
        Args:
            encrypted_message (str): Encrypted message in base64
            
        Returns:
            str: Decrypted message
            
        Raises:
            ValueError: If HMAC doesn't match (data altered)
        """
        try:
            # Decode from base64
            encrypted_data = b64decode(encrypted_message.encode('utf-8'))
            
            # Extract components
            iv = encrypted_data[:16]
            hmac_digest = encrypted_data[16:48]  # SHA256 = 32 bytes
            ciphertext = encrypted_data[48:]
            
            # Verify HMAC (security against tampering)
            hmac_obj = hmac.new(
                self.hmac_key,
                iv + ciphertext,
                hashlib.sha256
            )
            
            # Secure comparison against timing attacks
            if not hmac.compare_digest(hmac_obj.digest(), hmac_digest):
                raise ValueError("❌ Invalid HMAC! Data may have been altered.")
            
            # Create cipher for decryption
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            
            # Decrypt
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Remove padding
            plaintext = self._pkcs7_unpad(padded_plaintext)
            
            return plaintext.decode('utf-8')
        
        except Exception as e:
            raise ValueError(f"Error decrypting: {str(e)}")
    
    @staticmethod
    def _pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
        """
        Applies PKCS7 padding to data
        
        PKCS7: fill with N bytes of value N
        Ex: 14-byte data → 2 bytes of value 0x02
        
        Args:
            data (bytes): Data to be padded
            block_size (int): Block size (default AES = 16)
            
        Returns:
            bytes: Data with padding applied
        """
        pad_length = block_size - (len(data) % block_size)
        padding = bytes([pad_length] * pad_length)
        return data + padding
    
    @staticmethod
    def _pkcs7_unpad(data: bytes) -> bytes:
        """
        Remove PKCS7 padding from data
        
        Args:
            data (bytes): Data with padding
            
        Returns:
            bytes: Data without padding
            
        Raises:
            ValueError: If padding is invalid
        """
        pad_length = data[-1]
        
        if pad_length > 16 or pad_length == 0:
            raise ValueError("Invalid padding")
        
        # Verify all padding bytes have the same value
        for byte in data[-pad_length:]:
            if byte != pad_length:
                raise ValueError("Corrupted padding")
        
        return data[:-pad_length]
    
    @staticmethod
    def generate_key(length: int = 32) -> bytes:
        """
        Generates a secure random key
        
        Args:
            length (int): Key size in bytes (default: 32 for AES-256)
            
        Returns:
            bytes: Random key
        """
        return os.urandom(length)
