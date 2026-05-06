"""
Secure Proxy Client with End-to-End Encryption

Connects to proxy server and sends encrypted messages
"""

import socket
from .encryption import SecureEncryption


class ProxyClient:
    """
    Client that connects to proxy and sends encrypted messages
    
    Attributes:
        proxy_host (str): Proxy host
        proxy_port (int): Proxy port
        crypto (SecureEncryption): Encryption manager
    """
    
    def __init__(self, 
                 shared_key: bytes,
                 proxy_host: str = "127.0.0.1",
                 proxy_port: int = 9999):
        """
        Initialize proxy client
        
        Args:
            shared_key (bytes): Shared AES-256 key
            proxy_host (str): Proxy host
            proxy_port (int): Proxy port
        """
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.crypto = SecureEncryption(shared_key)
        
        print(f"""
        ╔═══════════════════════════════════════╗
        ║   🔒 Secure Client                   ║
        ║   Connecting to {self.proxy_host}:{self.proxy_port}   
        ╚═══════════════════════════════════════╝
        """)
    
    def send_message(self, message: str) -> str:
        """
        Send an encrypted message to proxy
        
        Args:
            message (str): Message to send
            
        Returns:
            str: Decrypted response from server
            
        Raises:
            ConnectionError: If unable to connect to proxy
        """
        client_socket = None
        try:
            # Connect to proxy
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.proxy_host, self.proxy_port))
            print(f"[✓] Connected to proxy {self.proxy_host}:{self.proxy_port}")
            
            # Encrypt message
            encrypted_message = self.crypto.encrypt(message)
            print(f"[🔐] Message encrypted ({len(encrypted_message)} chars)")
            print(f"[📝] Original message: {message}")
            
            # Send encrypted message
            client_socket.send(encrypted_message.encode('utf-8'))
            print(f"[→] Encrypted message sent to proxy")
            
            # Receive encrypted response
            encrypted_response = client_socket.recv(4096).decode('utf-8')
            print(f"[←] Encrypted response received ({len(encrypted_response)} chars)")
            
            # Decrypt response
            response = self.crypto.decrypt(encrypted_response)
            print(f"[🔓] Decrypted response: {response}")
            
            return response
        
        except socket.error as e:
            raise ConnectionError(f"Error connecting to proxy: {e}")
        except Exception as e:
            raise Exception(f"Error processing message: {e}")
        finally:
            if client_socket:
                client_socket.close()
                print(f"[X] Connection with proxy closed\n")
