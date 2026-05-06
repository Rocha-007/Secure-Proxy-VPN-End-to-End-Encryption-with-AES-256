#!/usr/bin/env python3
"""
Interactive Encryption Tool

Allows users to interactively encrypt and decrypt messages with AES-256
"""

from src.encryption import SecureEncryption


def print_header():
    """Print program header"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║     🔐 INTERACTIVE ENCRYPTION TOOL                   ║
    ║                                                      ║
    ║  Encrypt and Decrypt Messages with AES-256          ║
    ╚══════════════════════════════════════════════════════╝
    """)


def print_menu():
    """Print main menu"""
    print("\n" + "="*60)
    print("MENU:")
    print("1. Encrypt a message")
    print("2. Decrypt a message")
    print("3. Generate new encryption key")
    print("4. Exit")
    print("="*60)


def encrypt_message(crypto):
    """Encrypt a user-provided message"""
    print("\n" + "-"*60)
    message = input("📝 Enter message to encrypt: ")
    
    if not message:
        print("❌ Error: Message cannot be empty!")
        return
    
    try:
        encrypted = crypto.encrypt(message)
        print(f"\n✅ Encryption successful!")
        print(f"📝 Original:  {message}")
        print(f"🔐 Encrypted: {encrypted}")
    except Exception as e:
        print(f"❌ Error: {e}")


def decrypt_message(crypto):
    """Decrypt a user-provided encrypted message"""
    print("\n" + "-"*60)
    encrypted = input("🔐 Enter encrypted message: ")
    
    if not encrypted:
        print("❌ Error: Encrypted message cannot be empty!")
        return
    
    try:
        decrypted = crypto.decrypt(encrypted)
        print(f"\n✅ Decryption successful!")
        print(f"🔐 Encrypted:  {encrypted}")
        print(f"📝 Decrypted:  {decrypted}")
    except Exception as e:
        print(f"❌ Error: {e}")


def generate_key():
    """Generate and display a new encryption key"""
    print("\n" + "-"*60)
    key = SecureEncryption.generate_key()
    print(f"🔑 New encryption key generated:")
    print(f"   {key}")
    print(f"\n💡 Key length: {len(key)} bytes (256 bits)")
    print(f"⚠️  Save this key if you want to decrypt messages later!")
    
    use_new = input("\n❓ Use this new key? (y/n): ").lower()
    if use_new == 'y':
        return key
    return None


def main():
    """Main program loop"""
    print_header()
    
    # Initialize with default key
    default_key = b"default_encryption_key_32_bytes_long"
    crypto = SecureEncryption(default_key)
    
    print(f"🔑 Using default encryption key")
    print(f"💡 Tip: You can generate a new key from the menu\n")
    
    while True:
        print_menu()
        choice = input("\n👉 Choose an option (1-4): ").strip()
        
        if choice == '1':
            encrypt_message(crypto)
        
        elif choice == '2':
            decrypt_message(crypto)
        
        elif choice == '3':
            new_key = generate_key()
            if new_key:
                crypto = SecureEncryption(new_key)
                print("✅ New key set successfully!")
        
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option! Please choose 1-4.")


if __name__ == "__main__":
    main()
