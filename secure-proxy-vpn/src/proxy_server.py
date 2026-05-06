"""
Proxy Server with End-to-End Encryption

Acts as intermediary between client and final server:
- Receives encrypted connection from client
- Decrypts the request
- Forwards to real server
- Receives response
- Encrypts and returns to client
"""

import socket
import threading
from .encryption import SecureEncryption


class ProxyServer:
    """
    Servidor proxy que criptografa/descriptografa comunicação
    
    Attributes:
        host (str): Endereço para escutar
        proxy_port (int): Porta do proxy
        target_host (str): Servidor alvo
        target_port (int): Porta do servidor alvo
        crypto (SecureEncryption): Gerenciador de criptografia
        socket (socket.socket): Socket servidor
    """
    
    def __init__(self, 
                 shared_key: bytes,
                 proxy_host: str = "127.0.0.1",
                 proxy_port: int = 9999,
                 target_host: str = "127.0.0.1",
                 target_port: int = 8888):
        """
        Inicializa o servidor proxy
        
        Args:
            shared_key (bytes): Chave compartilhada AES-256
            proxy_host (str): Host para escutar
            proxy_port (int): Porta do proxy
            target_host (str): Host do servidor alvo
            target_port (int): Porta do servidor alvo
        """
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.target_host = target_host
        self.target_port = target_port
        self.crypto = SecureEncryption(shared_key)
        self.server_socket = None
        self.running = False
        
        print(f"""
        ╔═══════════════════════════════════════╗
        ║   🔒 Servidor Proxy Seguro             ║
        ║   Escutando em {self.proxy_host}:{self.proxy_port}      
        ║   Encaminhando para {self.target_host}:{self.target_port}   ║
        ╚═══════════════════════════════════════╝
        """)
    
    def start(self):
        """Start proxy server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.proxy_host, self.proxy_port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"[✓] Proxy listening for connections on {self.proxy_host}:{self.proxy_port}...")
            
            # Connection acceptance loop
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"[→] Connection received from {client_address}")
                    
                    # Process in thread to support multiple connections
                    thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, client_address)
                    )
                    thread.daemon = True
                    thread.start()
                    
                except Exception as e:
                    print(f"[!] Error accepting connection: {e}")
        
        except Exception as e:
            print(f"[✗] Error starting proxy: {e}")
        finally:
            self.stop()
    
    def _handle_client(self, client_socket: socket.socket, client_address: tuple):
        """
        Process a client connection
        
        Args:
            client_socket (socket.socket): Client socket
            client_address (tuple): Client address
        """
        try:
            # Receive encrypted data from client
            encrypted_data = client_socket.recv(4096).decode('utf-8')
            
            if not encrypted_data:
                print(f"[!] No data received from {client_address}")
                return
            
            print(f"[🔐] Encrypted data received ({len(encrypted_data)} chars)")
            
            # Decrypt
            try:
                decrypted_message = self.crypto.decrypt(encrypted_data)
                print(f"[🔓] Decrypted: {decrypted_message}")
            except ValueError as e:
                print(f"[✗] Encryption error: {e}")
                response = b"Error: Decryption failed"
                client_socket.send(response)
                return
            
            # Connect to target server
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                target_socket.connect((self.target_host, self.target_port))
                print(f"[→] Connected to target server {self.target_host}:{self.target_port}")
                
                # Send decrypted request to target server
                target_socket.send(decrypted_message.encode('utf-8'))
                
                # Receive response from target server
                response = target_socket.recv(4096).decode('utf-8')
                print(f"[←] Response received from target: {response}")
                
                # Encrypt response
                encrypted_response = self.crypto.encrypt(response)
                print(f"[🔐] Response encrypted ({len(encrypted_response)} chars)")
                
                # Send encrypted response to client
                client_socket.send(encrypted_response.encode('utf-8'))
                print(f"[✓] Encrypted response sent to client\n")
                
            except socket.error as e:
                print(f"[✗] Error connecting to target server: {e}")
                error_response = self.crypto.encrypt(f"Error: Could not connect to target server")
                client_socket.send(error_response.encode('utf-8'))
            finally:
                target_socket.close()
        
        except Exception as e:
            print(f"[✗] Error processing client: {e}")
        finally:
            client_socket.close()
            print(f"[X] Connection closed with {client_address}\n")
    
    def stop(self):
        """Stop proxy server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("\n[✓] Proxy server stopped")
