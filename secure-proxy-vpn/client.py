#!/usr/bin/env python3
"""
Entry point: Secure Proxy Client

Usage:
    python client.py --message "Your message here" [--proxy 127.0.0.1] [--port 9999]
"""

import argparse
import sys
from src.proxy_client import ProxyClient


def main():
    parser = argparse.ArgumentParser(
        description="Proxy Client with AES-256 Encryption"
    )
    parser.add_argument(
        "--message",
        required=True,
        help="Message to send"
    )
    parser.add_argument(
        "--proxy",
        default="127.0.0.1",
        help="Proxy host (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9999,
        help="Proxy port (default: 9999)"
    )
    parser.add_argument(
        "--key",
        default="your_shared_key_32_bytes_example123",
        help="Shared key for encryption"
    )
    
    args = parser.parse_args()
    
    # Convert string to bytes
    key_bytes = (args.key * 2)[:32].encode('utf-8')
    
    # Create client and send message
    client = ProxyClient(
        shared_key=key_bytes,
        proxy_host=args.proxy,
        proxy_port=args.port
    )
    
    try:
        response = client.send_message(args.message)
        print(f"\n✅ Process completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
