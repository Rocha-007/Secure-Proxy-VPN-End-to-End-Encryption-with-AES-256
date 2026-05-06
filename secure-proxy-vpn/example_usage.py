"""
Practical usage example of Secure Proxy VPN

Demonstrates how to use the system components
"""

import threading
import time
from src.encryption import SecureEncryption
from src.proxy_server import ProxyServer
from src.proxy_client import ProxyClient
from src.echo_server import EchoServer


def example_pure_encryption():
    """
    Example 1: Use encryption directly
    """
    print("\n" + "="*60)
    print("📌 EXAMPLE 1: Pure Encryption")
    print("="*60)
    
    # Create encryption manager
    shared_key = b"secure_key_32_bytes_example_12345"
    crypto = SecureEncryption(shared_key)
    
    # Example messages
    messages = [
        "Hello, World!",
        "Sensitive client data",
        "Login: user@example.com | Password: securePassword123",
        "Bank transaction of $1,000.00"
    ]
    
    for message in messages:
        print(f"\n📝 Original message: {message}")
        
        # Encrypt
        encrypted = crypto.encrypt(message)
        print(f"🔐 Encrypted: {encrypted[:50]}..." if len(encrypted) > 50 else f"🔐 Encrypted: {encrypted}")
        
        # Decrypt
        decrypted = crypto.decrypt(encrypted)
        print(f"🔓 Decrypted: {decrypted}")
        print(f"✅ Match: {message == decrypted}")


def example_complete_system():
    """
    Example 2: Complete system (Echo Server + Proxy + Client)
    """
    print("\n\n" + "="*60)
    print("📌 EXAMPLE 2: Complete System")
    print("="*60)
    
    shared_key = b"secret_proxy_system_key_complete_k"
    
    # 1. Start echo server (target server)
    print("\n[1/4] Starting Echo Server...")
    echo_server = EchoServer(port=8888)
    thread_echo = threading.Thread(target=echo_server.start, daemon=True)
    thread_echo.start()
    time.sleep(1)
    
    # 2. Start proxy
    print("\n[2/4] Starting Secure Proxy...")
    proxy = ProxyServer(
        shared_key=shared_key,
        proxy_port=9999,
        target_host="127.0.0.1",
        target_port=8888
    )
    thread_proxy = threading.Thread(target=proxy.start, daemon=True)
    thread_proxy.start()
    time.sleep(1)
    
    # 3. Create client
    print("\n[3/4] Creating Client...")
    client = ProxyClient(
        shared_key=shared_key,
        proxy_host="127.0.0.1",
        proxy_port=9999
    )
    
    # 4. Send messages
    print("\n[4/4] Sending Encrypted Messages...\n")
    
    test_messages = [
        "First test message",
        "Second secure message",
        "Confidential client data"
    ]
    
    for msg in test_messages:
        try:
            print(f"\n📤 Sending: {msg}")
            response = client.send_message(msg)
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Stop servers
    echo_server.stop()
    proxy.stop()


def example_security_comparison():
    """
    Example 3: Comparison - With and Without Encryption
    """
    print("\n\n" + "="*60)
    print("📌 EXAMPLE 3: Comparison - With vs Without Encryption")
    print("="*60)
    
    confidential_message = "Card number: 1234-5678-9012-3456"
    
    print(f"\n📝 Confidential data: {confidential_message}")
    
    # WITHOUT ENCRYPTION (dangerous!)
    print("\n❌ WITHOUT ENCRYPTION (INSECURE!):")
    print(f"   Traveling in plain text: {confidential_message}")
    print("   ⚠️  Anyone on the network can read it!")
    
    # WITH ENCRYPTION (secure!)
    print("\n✅ WITH ENCRYPTION (SECURE!):")
    crypto = SecureEncryption(b"example_key_32_bytes_security_123")
    encrypted = crypto.encrypt(confidential_message)
    print(f"   Traveling encrypted: {encrypted}")
    print(f"   ✅ Protected with AES-256")
    print(f"   ✅ Authenticated with HMAC-SHA256")
    print(f"   ✅ Random IV for each message")


def main():
    """Run all examples"""
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   🔒 USAGE EXAMPLES - SECURE PROXY VPN           ║
    ║                                                  ║
    ║   Practical Demonstration of Encryption & Security
    ╚══════════════════════════════════════════════════╝
    """)
    
    try:
        # Example 1: Pure encryption
        example_pure_encryption()
        
        # Example 2: Complete system
        example_complete_system()
        
        # Example 3: Security comparison
        example_security_comparison()
        
        print("\n\n" + "="*60)
        print("✅ ALL EXAMPLES EXECUTED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
