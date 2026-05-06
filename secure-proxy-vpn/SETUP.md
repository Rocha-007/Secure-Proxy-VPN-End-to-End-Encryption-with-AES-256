# Guia de Instalação e Execução

## ✅ Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para versionamento)

## 📦 Instalação

### Passo 1: Clonar/Copiar Projeto
```bash
cd Projeto-Pessoal
cd secure-proxy-vpn
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências
```bash
pip install -r requirements.txt
```

## 🚀 Execução

### Opção 1: Executar Exemplos

Demonstra todos os recursos do projeto:
```bash
python example_usage.py
```

**O que você verá:**
- ✅ Encriptação básica
- ✅ Sistema completo funcionando
- ✅ Comparação com/sem criptografia

### Opção 2: Usar em Dois Terminais Separados

**Terminal 1 - Iniciar Servidor Echo:**
```bash
# Servidor que responde com echo
cd src
python -c "from echo_server import EchoServer; EchoServer().start()"
```

**Terminal 2 - Iniciar Proxy:**
```bash
python server.py --port 9999
```

**Terminal 3 - Enviar Mensagens:**
```bash
# Enviar diferentes mensagens
python client.py --message "Olá, mundo seguro!"
python client.py --message "Testando criptografia AES-256"
python client.py --message "Dados sensíveis do cliente"
```

### Opção 3: Executar Testes Unitários

```bash
# Instalar pytest
pip install pytest

# Rodar testes
pytest tests/ -v

# Rodar com cobertura
pytest tests/ --cov=src
```

## 📊 Saída Esperada

### Exemplo de Execução com Cliente
```
╔═══════════════════════════════════════╗
║   🔒 Cliente Seguro                    ║
║   Conectando a 127.0.0.1:9999   
╚═══════════════════════════════════════╝

[✓] Conectado ao proxy 127.0.0.1:9999
[🔐] Mensagem encriptada (87 chars)
[📝] Mensagem original: Olá, mundo seguro!
[→] Mensagem encriptada enviada ao proxy
[←] Resposta encriptada recebida (92 chars)
[🔓] Resposta descriptografada: ECHO: Olá, mundo seguro!
[X] Conexão com proxy fechada

✅ Processo completado com sucesso!
```

## 🔧 Opções de Configuração

### Servidor Proxy
```bash
python server.py --help

Opções:
  --port PORT              Porta do proxy (padrão: 9999)
  --target-host HOST       Host do servidor alvo (padrão: 127.0.0.1)
  --target-port PORT       Porta do servidor alvo (padrão: 8888)
  --key CHAVE             Chave compartilhada (padrão: predefinida)
```

Exemplo com customização:
```bash
python server.py --port 8000 --target-host example.com --target-port 80
```

### Cliente
```bash
python client.py --help

Opções:
  --message MSG           Mensagem a enviar (obrigatório)
  --proxy HOST            Host do proxy (padrão: 127.0.0.1)
  --port PORT             Porta do proxy (padrão: 9999)
  --key CHAVE            Chave compartilhada (padrão: predefinida)
```

Exemplos:
```bash
python client.py --message "Teste" --proxy 192.168.1.100 --port 8000

python client.py --message "Dados sensíveis" --key "sua_chave_custom_32_bytes"
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'cryptography'"

**Solução:**
```bash
pip install cryptography==41.0.7
```

### Erro: "Address already in use"

**Causa:** Porta já está ocupada
**Solução:**
```bash
# Usar porta diferente
python server.py --port 9998
```

**Ou liberar porta (Windows):**
```powershell
# Encontrar processo usando porta
netstat -ano | findstr ":9999"

# Matar processo (PID)
taskkill /PID <PID> /F
```

### Erro: "Connection refused"

**Causa:** Proxy não está rodando
**Solução:** 
1. Certifique-se que proxy está iniciado em outro terminal
2. Verifique porta correta
3. Verifique endereço IP

### Erro ao Descriptografar: "HMAC inválido"

**Causa:** Dados foram alterados em trânsito
**O que fazer:**
- Verificar se a chave é a mesma cliente/servidor
- Verificar se dados não foram corrompidos
- Este é comportamento **esperado** em caso de ataque

## 📈 Monitoramento

### Ver tráfego de encriptação

O proxy mostra em tempo real:
```
[→] Conexão recebida de ('127.0.0.1', 54321)
[🔐] Dados encriptados recebidos (87 chars)
[🔓] Descriptografado: Olá, mundo seguro!
[→] Conectado ao servidor alvo 127.0.0.1:8888
[←] Resposta recebida do alvo: ECHO: Olá, mundo seguro!
[🔐] Resposta encriptada (92 chars)
[✓] Resposta encriptada enviada ao cliente
```

## 📚 Próximos Passos

Depois de executar com sucesso:

1. **Entender o código:**
   - Leia [TECHNICAL.md](TECHNICAL.md)
   - Estude `src/encryption.py` em detalhes
   - Entenda o fluxo em `src/proxy_server.py`

2. **Modificar e experimentar:**
   - Altere tamanho de chave
   - Adicione logs adicionais
   - Implemente compressão

3. **Expandir funcionalidade:**
   - Adicione autenticação de usuários
   - Implemente rate limiting
   - Crie dashboard de monitoramento

4. **Implementar em portfólio:**
   - Faça o deploy em servidor real
   - Adicione certificados SSL
   - Documente bem em README

## 🎓 Conceitos para Aprender

Enquanto trabalha neste projeto, você aprenderá:

- ✅ AES-256 Criptografia Simétrica
- ✅ HMAC Autenticação
- ✅ Socket Programming (TCP/IP)
- ✅ Programação Concorrente (Threading)
- ✅ Tratamento de Erros Robusto
- ✅ Testes Unitários
- ✅ Design Patterns (Factory, Strategy)
- ✅ Documentação Técnica Professional

## 📞 Suporte

Para dúvidas sobre:
- **Criptografia**: Veja [TECHNICAL.md](TECHNICAL.md)
- **Como usar**: Veja exemplos em `example_usage.py`
- **Código**: Veja comentários em `src/`
- **Testes**: Veja `tests/`

---

**Versão 1.0** | Projeto Educacional | Maio 2026
