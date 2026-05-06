"""
Echo Server for testing
Simulates a real server responding to requests
"""

import socket
import threading


class EchoServer:
    """Simple Echo server for testing"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8888):
        self.host = host
        self.port = port
        self.running = False
        self.server_socket = None
    
    def start(self):
        """Start echo server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"[✓] Echo Server running on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, address)
                    )
                    thread.daemon = True
                    thread.start()
                except Exception as e:
                    if self.running:
                        print(f"[!] Error: {e}")
        except Exception as e:
            print(f"[✗] Error starting echo server: {e}")
        finally:
            self.stop()
    
    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """Process client connection"""
        try:
            data = client_socket.recv(1024).decode('utf-8')
            print(f"[Echo] Received from {address}: {data}")
            
            response = f"ECHO: {data}"
            client_socket.send(response.encode('utf-8'))
            print(f"[Echo] Sent to {address}: {response}")
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            client_socket.close()
    
    def stop(self):
        """Stop echo server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("[✓] Echo Server stopped")
