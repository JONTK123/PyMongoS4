# PyMongoS4 - Sistema de Mensagens Criptografadas

Sistema de mensagens criptografadas desenvolvido em Python utilizando MongoDB como banco de dados e criptografia AES para segurança das mensagens.

## 📋 Descrição do Projeto

PyMongoS4 é uma aplicação de linha de comando que permite aos usuários enviarem e receberem mensagens criptografadas. O sistema utiliza autenticação de usuários e criptografia AES-CBC com PKCS5 padding para garantir a segurança e privacidade das comunicações.

## 👥 Autores

- Filipe Daniel M. T. Mota
- Thiago Luiz Fossa
- Alex Insel

## ✨ Funcionalidades

- **Autenticação de Usuários**: Sistema seguro de login com email e senha
- **Envio de Mensagens Criptografadas**: Mensagens são criptografadas usando AES antes de serem armazenadas
- **Leitura de Mensagens**: Visualização de mensagens recebidas com descriptografia
- **Gerenciamento de Usuários**: Lista todos os usuários cadastrados no sistema
- **Segurança**: Criptografia AES-CBC com chave personalizada por mensagem
- **Interface Intuitiva**: Menu interativo simples e fácil de usar

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação principal
- **MongoDB**: Banco de dados NoSQL para armazenamento de usuários e mensagens
- **PyMongo 4.10.1**: Driver Python para MongoDB
- **AES-PKCS5 1.0.3**: Biblioteca de criptografia AES
- **Cryptography 43.0.1**: Biblioteca de primitivas criptográficas
- **CFFI 1.17.1**: Interface de funções estrangeiras C para Python
- **DNSPython 2.7.0**: Kit de ferramentas DNS
- **pycparser 2.22**: Parser C para Python

## 📦 Pré-requisitos

- Python 3.7 ou superior
- Pip (gerenciador de pacotes Python)
- Conta MongoDB Atlas ou instância MongoDB local
- Conexão com a internet para acessar o banco de dados

## 🚀 Instalação

1. **Clone o repositório**:
```bash
git clone https://github.com/JONTK123/PyMongoS4.git
cd PyMongoS4
```

2. **Navegue até o diretório src**:
```bash
cd src
```

3. **Crie um ambiente virtual (recomendado)**:
```bash
python -m venv env
```

4. **Ative o ambiente virtual**:
   - No Windows:
   ```bash
   env\Scripts\activate
   ```
   - No Linux/Mac:
   ```bash
   source env/bin/activate
   ```

5. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

1. **Configure a conexão com MongoDB**:
   - Crie um arquivo `.env` no diretório `src/` com a seguinte variável:
   ```
   MONGODB_URI=sua_string_de_conexao_mongodb
   ```
   - Exemplo:
   ```
   MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
   # Substitua 'usuario' e 'senha' pelas suas credenciais reais do MongoDB
   ```

2. **Estrutura do Banco de Dados**:
   O sistema utiliza um banco de dados chamado `pymongo` com as seguintes coleções:
   
   - **users**: Armazena informações dos usuários
     ```json
     {
       "nome": "Nome do Usuário",
       "nickname": "email@exemplo.com",
       "password": "senha123"
     }
     ```
     **Nota**: As senhas são armazenadas em texto plano no banco de dados. Em um ambiente de produção, recomenda-se utilizar hash de senhas (bcrypt, argon2, etc.).
   
   - **messages**: Armazena as mensagens criptografadas
     ```json
     {
       "to": "destinatario@exemplo.com",
       "nickname": "remetente@exemplo.com",
       "content": "mensagem_criptografada_base64",
       "datetime": ISODate("2025-10-15T23:42:00Z")
     }
     ```

## 🎮 Como Usar

1. **Execute a aplicação**:
```bash
python main.py
```

2. **Faça login**:
   - Digite seu email (nickname)
   - Digite sua senha
   - Se as credenciais estiverem corretas, você será autenticado

3. **Menu Principal**:
   - **Opção 1 - Enviar mensagem**:
     - Selecione o destinatário da lista
     - Digite a mensagem
     - Digite uma chave de criptografia (será ajustada para 16 caracteres)
     - A mensagem será criptografada e enviada
   
   - **Opção 2 - Ler as mensagens**:
     - Selecione o remetente para ver mensagens
     - Escolha a mensagem específica
     - Digite a chave de descriptografia
     - A mensagem será descriptografada e exibida
   
   - **Opção 3 - Desligar**:
     - Encerra a aplicação

## 🔐 Segurança

- **Criptografia AES-CBC**: Todas as mensagens são criptografadas usando AES em modo CBC
- **PKCS5 Padding**: Garante que mensagens de qualquer tamanho sejam criptografadas corretamente
- **Chaves Personalizadas**: Cada mensagem pode usar uma chave diferente
- **Formato Base64**: Mensagens criptografadas são codificadas em Base64 para armazenamento seguro

**Nota Importante**: A chave de criptografia é ajustada automaticamente para 16 caracteres. Certifique-se de lembrar da chave usada para criptografar cada mensagem.

## 📁 Estrutura do Projeto

```
PyMongoS4/
│
├── README.md                 # Documentação do projeto
├── src/                      # Código fonte
│   ├── main.py              # Arquivo principal da aplicação
│   ├── mongohandler.py      # Classe para manipulação do MongoDB
│   ├── models.py            # Modelos de dados (Users, Messages)
│   ├── handler.py           # Handlers auxiliares
│   ├── requirements.txt     # Dependências do projeto
│   ├── .env                 # Variáveis de ambiente (não versionado)
│   └── env/                 # Ambiente virtual Python (não versionado)
```

## 🔧 Arquitetura

### Classes Principais

1. **MongoHandler** (`mongohandler.py`):
   - Gerencia conexão com MongoDB
   - Métodos de autenticação de usuários
   - CRUD de mensagens
   - Funções de criptografia e descriptografia

2. **Users** (`models.py`):
   - Modelo de dados para usuários
   - Campos: nome, nickname (email), password

3. **Messages** (`models.py`):
   - Modelo de dados para mensagens
   - Campos: to (destinatário), nickname (remetente), content (conteúdo criptografado), datetime

4. **Main** (`main.py`):
   - Interface de usuário
   - Menu interativo
   - Fluxo de autenticação e operações

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte de um trabalho acadêmico.

## 🐛 Problemas Conhecidos

- A string de conexão MongoDB está hardcoded no arquivo `mongohandler.py` como fallback
- Recomenda-se usar sempre variáveis de ambiente para credenciais sensíveis

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório do GitHub.

## 🔄 Roadmap

Possíveis melhorias futuras:
- [ ] Interface gráfica (GUI)
- [ ] Suporte para anexos de arquivos
- [ ] Notificações em tempo real
- [ ] Grupos de conversação
- [ ] Histórico de mensagens paginado
- [ ] Autenticação de dois fatores (2FA)
- [ ] Exportação de conversas

---

**Desenvolvido com 💙 por estudantes apaixonados por tecnologia**
