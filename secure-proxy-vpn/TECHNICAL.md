# Documentação Técnica - Secure Proxy VPN

## 🎯 Visão Geral

Sistema educacional de proxy com criptografia AES-256 que demonstra:
- **Criptografia Simétrica**: AES-256-CBC
- **Autenticação de Mensagens**: HMAC-SHA256
- **Programação de Sockets**: TCP/IP
- **Design de Protocolos Seguros**

## 🔐 Especificações de Criptografia

### Algoritmo Principal: AES-256-CBC

```
┌─────────────────────────────────────────┐
│ ENCRIPTAÇÃO (Cliente → Proxy)           │
├─────────────────────────────────────────┤
│ 1. Gerar IV aleatório (16 bytes)        │
│ 2. Aplicar padding PKCS7                │
│ 3. Encriptar com AES-256-CBC            │
│ 4. Calcular HMAC-SHA256                 │
│ 5. Combinar: IV + HMAC + Ciphertext     │
│ 6. Codificar em Base64                  │
└─────────────────────────────────────────┘
```

### Componentes de Segurança

| Componente | Tamanho | Propósito |
|-----------|--------|----------|
| **Chave AES** | 256 bits (32 bytes) | Encriptação |
| **IV** | 128 bits (16 bytes) | Aleatoriedade |
| **HMAC-SHA256** | 256 bits (32 bytes) | Autenticação |
| **Bloco AES** | 128 bits (16 bytes) | Unidade de operação |

### Estrutura da Mensagem Encriptada

```
┌─────────┬──────────┬─────────────────┐
│   IV    │   HMAC   │  Ciphertext     │
├─────────┼──────────┼─────────────────┤
│ 16 bytes│ 32 bytes │ N*16 bytes      │
└─────────┴──────────┴─────────────────┘
         ↓
    Base64 Encoded
```

## 🔑 Protocolo de Comunicação

### Fase 1: Handshake Inicial (Futuro)
```
[Cliente] -----(Public Key)----→ [Proxy]
[Proxy]   -----(Encrypted Key)--→ [Cliente]
```

*Nota: Versão atual usa chave pré-compartilhada*

### Fase 2: Comunicação Segura

```
Cliente                  Proxy                 Servidor Alvo
   │                      │                        │
   ├──(Criptografado)────→│                        │
   │                      ├─(Descriptografado)────→│
   │                      │                        │
   │                      │←─(Resposta)───────────┤
   │←─(Criptografado)─────┤                        │
```

## 📊 Fluxo de Dados Detalhado

### Cliente Envia Mensagem

```python
# Entrada
mensagem = "Dados confidenciais"

# Passo 1: Encriptação
iv = os.urandom(16)  # Gerar IV aleatório
ciphertext = AES_CBC(chave, iv, plaintext)

# Passo 2: Autenticação
hmac = HMAC_SHA256(hmac_key, iv + ciphertext)

# Passo 3: Montagem
pacote = iv + hmac + ciphertext

# Passo 4: Codificação
encoded = Base64(pacote)

# Saída
→ Envia encoded ao proxy
```

### Proxy Processa Mensagem

```python
# Entrada (recebe do cliente)
encoded_msg = "..." # Base64

# Passo 1: Decodificação
pacote = Base64_decode(encoded_msg)
iv = pacote[0:16]
hmac = pacote[16:48]
ciphertext = pacote[48:]

# Passo 2: Verificação HMAC
hmac_calculado = HMAC_SHA256(hmac_key, iv + ciphertext)
assert hmac == hmac_calculado  # Verificar integridade

# Passo 3: Descriptografia
plaintext = AES_CBC_decrypt(chave, iv, ciphertext)

# Passo 4: Enviar para servidor alvo
→ Envia plaintext ao servidor

# Passo 5: Receber resposta
resposta = servidor.recv()

# Passo 6: Re-encriptar (mesmo processo)
resposta_encriptada = encrypt(resposta)

# Saída
→ Envia resposta_encriptada ao cliente
```

## 🛡️ Proteções Implementadas

### 1. **Confidencialidade**
- Criptografia AES-256
- Cada mensagem com IV único
- Impossível ler dados sem chave

### 2. **Integridade**
- HMAC-SHA256 autentica mensagens
- Detecta alterações durante transmissão
- Rejeita mensagens modificadas

### 3. **Anti-Replay (Futuro)**
- Timestamps em mensagens
- Números sequenciais
- Cache de mensagens já recebidas

### 4. **Timing Attack Protection**
- Uso de `hmac.compare_digest()`
- Comparação em tempo constante
- Previne análise por tempo de execução

## 🔍 Análise de Casos de Uso

### Caso 1: Interceptação de Mensagem

```
Atacante intercepta: "Y7f8k2x9mQ=="
- Não consegue ler (encriptado)
- Se modificar: HMAC falha
- Resultado: Mensagem rejeitada ✅
```

### Caso 2: Replay Attack

```
Atacante captura e envia mesma mensagem novamente
Versão atual: Executa novamente (vulnerável)
Versão futura: Timestamp/Nonce previne ✅
```

### Caso 3: Man-in-the-Middle

```
Cliente ←→ Atacante ←→ Proxy ←→ Servidor
        (Pode interceptar)
- Sem conhecer a chave, não consegue ler
- Modificação causa falha HMAC
- Resultado: Seguro contra MITM sem chave ✅
```

## 📈 Complexidade Computacional

| Operação | Complexidade | Tempo Aprox. |
|----------|-------------|-------------|
| Encriptação (256B) | O(1) | ~0.1ms |
| HMAC-SHA256 | O(1) | ~0.05ms |
| Descriptografia (256B) | O(1) | ~0.1ms |
| Comparação HMAC | O(1) time-safe | ~32 comparações |

## 🚀 Otimizações Possíveis

### Curto Prazo
```python
- Usar buffer de 4KB ao invés de 1KB
- Implementar connection pooling
- Adicionar compressão (zlib)
```

### Médio Prazo
```python
- Usar asyncio para I/O não-bloqueante
- Implementar TLS 1.3 nativo
- Suportar múltiplos algoritmos
```

### Longo Prazo
```python
- Perfect Forward Secrecy (PFS)
- Diffie-Hellman Key Exchange
- Elliptic Curve Cryptography
- Zero-Knowledge Proofs
```

## 🧪 Casos de Teste Críticos

### Teste de Segurança 1: Detecção de Tampering
```python
def test_hmac_tampering_detection():
    crypto = SecureEncryption(key)
    msg = "Dados"
    encrypted = crypto.encrypt(msg)
    
    # Modificar um byte
    corrupted = encrypted[:-5] + "XXXXX"
    
    # Deve falhar
    with pytest.raises(ValueError):
        crypto.decrypt(corrupted)  ✅
```

### Teste de Segurança 2: Chaves Diferentes
```python
def test_different_keys_fail():
    crypto1 = SecureEncryption(key1)
    crypto2 = SecureEncryption(key2)
    
    encrypted = crypto1.encrypt("msg")
    
    # Deve falhar com chave diferente
    with pytest.raises(ValueError):
        crypto2.decrypt(encrypted)  ✅
```

### Teste de Segurança 3: IV Aleatório
```python
def test_random_iv():
    crypto = SecureEncryption(key)
    msg = "Mensagem repetida"
    
    enc1 = crypto.encrypt(msg)
    enc2 = crypto.encrypt(msg)
    
    # Devem ser diferentes (IV aleatório)
    assert enc1 != enc2  ✅
    
    # Mas ambos descriptografam corretamente
    assert crypto.decrypt(enc1) == msg  ✅
    assert crypto.decrypt(enc2) == msg  ✅
```

## 📚 Referências de Segurança

- **NIST SP 800-38A**: Recomendações para Cipher Block Modes
- **FIPS 197**: Especificação do AES
- **RFC 2104**: HMAC - Keyed-Hashing for Message Authentication
- **OWASP**: Top 10 Vulnerabilidades Web

## 📋 Checklist de Produção

- [ ] Implementar Perfect Forward Secrecy
- [ ] Usar TLS 1.3 ao invés de criptografia customizada
- [ ] Adicionar rate limiting
- [ ] Implementar logging e auditoria
- [ ] Realizar security audit profissional
- [ ] Testes de penetração
- [ ] Certificados SSL/TLS válidos
- [ ] Autenticação de usuários
- [ ] Controle de acesso
- [ ] Backup e recuperação de desastres

---

**Documento Técnico v1.0** | Educacional | Não use em produção sem auditoria profissional
