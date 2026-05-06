"""
Secure Proxy VPN - Encryption and proxy module
"""

from .encryption import SecureEncryption
from .proxy_server import ProxyServer
from .proxy_client import ProxyClient

__version__ = "1.0.0"
__author__ = "Security Professional"

__all__ = ["SecureEncryption", "ProxyServer", "ProxyClient"]
