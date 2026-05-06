# 🔐 Secure Proxy VPN - Criptografia Ponta-a-Ponta

Um sistema de proxy com criptografia AES-256 que demonstra conceitos fundamentais de segurança de rede.

## 📋 O que você vai aprender

- ✅ **Criptografia Simétrica (AES-256)** - Proteger dados em trânsito
- ✅ **Socket Programming** - Comunicação TCP/IP
- ✅ **Key Exchange** - Como trocar chaves de forma segura
- ✅ **Message Authentication** - Garantir integridade dos dados
- ✅ **Protocol Design** - Estruturar comunicação entre cliente/servidor

## 🏗️ Arquitetura

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Cliente   │─────────│ Proxy Server │─────────│  Servidor   │
│  (encripta) │◀──────▶ │  (descriptografa)   │  (responde)  │
└─────────────┘         └──────────────┘         └─────────────┘
    Mensagem                Tunel Seguro             Serviço
    Original          (AES-256 Criptografado)       Original
```

## 🚀 Como usar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o servidor proxy
```bash
python server.py --port 9999 --target 127.0.0.1 8888
```

### 3. Conectar um cliente
```bash
python client.py --proxy 127.0.0.1 9999 --message "Olá, mundo seguro!"
```

### 4. Executar testes
```bash
pytest tests/ -v
```

## 📁 Estrutura do Projeto

```
secure-proxy-vpn/
├── src/
│   ├── __init__.py
│   ├── encryption.py      # Criptografia AES-256
│   ├── proxy_server.py    # Servidor proxy
│   └── proxy_client.py    # Cliente proxy
├── tests/
│   ├── __init__.py
│   └── test_encryption.py # Testes unitários
├── server.py              # Entry point servidor
├── client.py              # Entry point cliente
├── requirements.txt
└── README.md
```

## 🔑 Conceitos de Segurança

### 1. **Chave Compartilhada**
- Ambos os lados usam a mesma chave AES-256
- Em produção, usaria key exchange (Diffie-Hellman)

### 2. **Inicialização Vetorial (IV)**
- Cada mensagem usa um IV aleatório
- Previne padrões repetitivos

### 3. **HMAC (Hash-based Message Authentication Code)**
- Garante integridade dos dados
- Detecta alterações durante transmissão

### 4. **Padding**
- AES trabalha com blocos de 16 bytes
- Padding PKCS7 para mensagens menores

## 💡 Exemplo Prático

```python
from src.encryption import SecureEncryption

# Criar instância com chave segura
crypto = SecureEncryption(shared_key=b"sua_chave_32_bytes_aqui123456")

# Encriptar
mensagem = "Dados sensíveis do cliente"
criptografado = crypto.encrypt(mensagem)
print(f"Enviando: {criptografado}")

# Descriptografar
descriptografado = crypto.decrypt(criptografado)
print(f"Recebido: {descriptografado}")
```

## 🎯 Próximos Passos (Melhorias)

- [ ] Implementar Diffie-Hellman Key Exchange
- [ ] Adicionar Rate Limiting e DDoS Protection
- [ ] Implementar TLS/SSL nativo
- [ ] Dashboard de monitoramento
- [ ] Logging avançado
- [ ] Suporte a múltiplas conexões simultâneas

## ⚠️ Aviso de Segurança

Este é um projeto educacional. Para produção:
- Use certificados SSL/TLS adequados
- Implemente autenticação robusta
- Adicione logging e auditoria
- Realize security audits profissionais
- Nunca compartilhe chaves em código

## 📚 Referências

- https://docs.python-guide.org/
- https://cryptography.io/
- https://owasp.org/
- RFC 3394 - AES Key Wrap Algorithm

---

**Desenvolvido como projeto educacional de Cibersegurança** 🔐
