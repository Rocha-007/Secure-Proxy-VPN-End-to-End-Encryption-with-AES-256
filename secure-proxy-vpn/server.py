#!/usr/bin/env python3
"""
Entry point: Start Proxy Server

Usage:
    python server.py [--port 9999]
"""

import argparse
import sys
from src.proxy_server import ProxyServer
from src.encryption import SecureEncryption


def main():
    parser = argparse.ArgumentParser(
        description="Proxy Server with AES-256 Encryption"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=9999,
        help="Proxy port (default: 9999)"
    )
    parser.add_argument(
        "--target-host",
        default="127.0.0.1",
        help="Target server host (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--target-port",
        type=int,
        default=8888,
        help="Target server port (default: 8888)"
    )
    parser.add_argument(
        "--key",
        default="your_shared_key_32_bytes_example123",
        help="Shared key for encryption"
    )
    
    args = parser.parse_args()
    
    # Convert string to bytes (expand if necessary)
    key_bytes = (args.key * 2)[:32].encode('utf-8')
    
    # Start proxy
    proxy = ProxyServer(
        shared_key=key_bytes,
        proxy_port=args.port,
        target_host=args.target_host,
        target_port=args.target_port
    )
    
    try:
        proxy.start()
    except KeyboardInterrupt:
        print("\n[!] Server interrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
