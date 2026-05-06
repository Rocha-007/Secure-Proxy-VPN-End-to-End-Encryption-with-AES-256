"""
Testes unitários para o módulo de criptografia
"""

import pytest
from src.encryption import SecureEncryption


class TestSecureEncryption:
    """Testes da classe SecureEncryption"""
    
    @pytest.fixture
    def crypto(self):
        """Fixture que cria instância de criptografia"""
        key = b"chave_teste_32_bytes_exatamente_ok"
        return SecureEncryption(key)
    
    def test_inicializacao_válida(self):
        """Testa inicialização com chave válida"""
        key = SecureEncryption.generate_key()
        crypto = SecureEncryption(key)
        assert crypto.key == key
    
    def test_inicializacao_chave_pequena(self):
        """Testa erro com chave pequena"""
        key = b"chave_pequena"
        with pytest.raises(ValueError):
            SecureEncryption(key)
    
    def test_encrypt_decrypt_simples(self, crypto):
        """Testa encriptação e descriptografia de mensagem simples"""
        mensagem_original = "Olá, Mundo!"
        
        # Encriptar
        encriptado = crypto.encrypt(mensagem_original)
        assert isinstance(encriptado, str)
        assert len(encriptado) > 0
        
        # Descriptografar
        descriptografado = crypto.decrypt(encriptado)
        assert descriptografado == mensagem_original
    
    def test_encrypt_decrypt_longo(self, crypto):
        """Testa com mensagem longa"""
        mensagem = "A" * 1000
        
        encriptado = crypto.encrypt(mensagem)
        descriptografado = crypto.decrypt(encriptado)
        
        assert descriptografado == mensagem
    
    def test_encrypt_decrypt_especial(self, crypto):
        """Testa com caracteres especiais"""
        mensagem = "Teste com acentuação: çáéíóú 🔐 Símbolos!"
        
        encriptado = crypto.encrypt(mensagem)
        descriptografado = crypto.decrypt(encriptado)
        
        assert descriptografado == mensagem
    
    def test_encrypt_vazio(self, crypto):
        """Testa encriptação de string vazia"""
        mensagem = ""
        
        encriptado = crypto.encrypt(mensagem)
        descriptografado = crypto.decrypt(encriptado)
        
        assert descriptografado == mensagem
    
    def test_diferentes_encriptações_diferentes(self, crypto):
        """Testa que mesma mensagem gera diferentes encriptações (IV aleatório)"""
        mensagem = "Mesma mensagem"
        
        encriptado1 = crypto.encrypt(mensagem)
        encriptado2 = crypto.encrypt(mensagem)
        
        # Devem ser diferentes (por causa do IV aleatório)
        assert encriptado1 != encriptado2
        
        # Mas ambos devem descriptografar para mesma mensagem
        assert crypto.decrypt(encriptado1) == mensagem
        assert crypto.decrypt(encriptado2) == mensagem
    
    def test_hmac_tampering_detection(self, crypto):
        """Testa detecção de manipulação de dados"""
        mensagem = "Dados importantes"
        encriptado = crypto.encrypt(mensagem)
        
        # Modificar um caractere na mensagem encriptada
        encriptado_modificado = encriptado[:-5] + "XXXXX"
        
        # Descriptografia deve falhar
        with pytest.raises(ValueError):
            crypto.decrypt(encriptado_modificado)
    
    def test_chaves_diferentes_falham(self):
        """Testa que chaves diferentes não conseguem descriptografar"""
        crypto1 = SecureEncryption(b"chave_um_32_bytes_exatamente_ok1")
        crypto2 = SecureEncryption(b"chave_dois_32bytes_exatamente_ok2")
        
        mensagem = "Teste de chaves diferentes"
        encriptado = crypto1.encrypt(mensagem)
        
        # Descriptografia com chave errada deve falhar
        with pytest.raises(ValueError):
            crypto2.decrypt(encriptado)
    
    def test_generate_key(self):
        """Testa geração de chave"""
        key1 = SecureEncryption.generate_key()
        key2 = SecureEncryption.generate_key()
        
        # Devem ter tamanho correto
        assert len(key1) == 32
        assert len(key2) == 32
        
        # Devem ser diferentes
        assert key1 != key2
        
        # Devem ser bytes
        assert isinstance(key1, bytes)
        assert isinstance(key2, bytes)
    
    def test_pkcs7_padding(self):
        """Testa padding PKCS7"""
        data = b"Teste"
        padded = SecureEncryption._pkcs7_pad(data, block_size=16)
        
        # Deve ter tamanho múltiplo de 16
        assert len(padded) % 16 == 0
        
        # Deve ter 11 bytes de padding (16 - 5)
        assert padded[-1] == 11
    
    def test_pkcs7_unpadding(self):
        """Testa remoção de padding PKCS7"""
        data = b"Teste"
        padded = SecureEncryption._pkcs7_pad(data, block_size=16)
        unpadded = SecureEncryption._pkcs7_unpad(padded)
        
        assert unpadded == data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
