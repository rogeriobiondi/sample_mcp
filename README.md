# Sample MCP Chat

Aplicacao de terminal para conversar com modelos da Anthropic usando MCP (Model Context Protocol).

O projeto conecta:

- um cliente de chat local;
- um ou mais servidores MCP via `stdio`;
- o modelo Claude para responder perguntas e chamar tools dinamicamente.

## O que este projeto faz

- Chat interativo no terminal.
- Uso de documentos como contexto com mencoes `@arquivo`.
- Comandos por prompt MCP com prefixo `/` (ex.: `/summary deposition.md`).
- Descoberta automatica de tools MCP e execucao durante a conversa.
- Suporte a servidores MCP extras passados por argumento de linha de comando.

## Arquitetura

Fluxo simplificado:

1. `main.py` carrega ambiente e inicializa clientes MCP.
2. `CliApp` (`core/cli.py`) controla input, historico e autocomplete.
3. `CliChat` (`core/cli_chat.py`) traduz entrada do usuario em mensagens para o modelo.
4. `Chat` (`core/chat.py`) roda o loop de conversa e tool use.
5. `Claude` (`core/claude.py`) encapsula chamadas da API Anthropic.
6. `ToolManager` (`core/tools.py`) descobre e executa tools no cliente MCP correto.
7. `mcp_server.py` expoe resources, prompts e tools de exemplo.

## Estrutura do projeto

```text
.
|-- main.py
|-- mcp_client.py
|-- mcp_server.py
|-- core/
|   |-- chat.py
|   |-- claude.py
|   |-- cli.py
|   |-- cli_chat.py
|   `-- tools.py
|-- pyproject.toml
`-- README.md
```

## Requisitos

- Python 3.10+
- Chave de API Anthropic (`ANTHROPIC_API_KEY`)
- Modelo Claude configurado em `CLAUDE_MODEL`

## Configuracao

Crie um arquivo `.env` na raiz (ou ajuste o existente):

```env
ANTHROPIC_API_KEY="sua_chave_aqui"
CLAUDE_MODEL="claude-sonnet-4-20250514"
# Opcional: use uv para iniciar o mcp_server padrao
USE_UV="1"
```

Observacao: `main.py` valida `CLAUDE_MODEL` e `ANTHROPIC_API_KEY`. Se algum estiver vazio, a aplicacao interrompe com erro.

## Instalacao e execucao

### Opcao 1 (recomendada): uv

```bash
pip install uv
uv venv
source .venv/bin/activate
uv pip install -e .
uv run main.py
```

### Opcao 2: venv + pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python main.py
```

## Uso

### 1) Pergunta normal

```text
> Qual o objetivo deste projeto?
```

### 2) Referencia de documento com `@`

```text
> Resuma os pontos principais de @report.pdf
```

Quando um documento e mencionado, o cliente tenta buscar seu conteudo via resource MCP e injeta no contexto da pergunta.

### 3) Comandos MCP com `/`

```text
> /summary deposition.md
> /format plan.md
```

Esses comandos usam prompts definidos no servidor MCP (`mcp_server.py`).

### 4) Autocomplete

- `Tab` completa comandos `/...`
- `Tab` apos `@` sugere IDs de documentos
- ao digitar espaco apos um comando, o CLI sugere argumentos (docs)

## Servidor MCP de exemplo

O `mcp_server.py` expoe:

- Tool `read_doc_contents`
- Tool `edit_doc_contents`
- Resource `docs://documents` (lista de IDs)
- Resource `docs://documents/{doc_id}` (conteudo)
- Prompt `format`
- Prompt `summary`

Os documentos sao mantidos em memoria no dicionario `docs`.

## Executando com servidores MCP adicionais

Voce pode passar scripts extras no comando:

```bash
uv run main.py caminho/para/outro_servidor.py
```

O app cria um cliente MCP para cada script adicional e agrega todas as tools disponiveis no loop de chat.

## Como estender

### Adicionar novos documentos

Edite o dicionario `docs` em `mcp_server.py`.

### Adicionar nova tool MCP

Crie uma nova funcao com `@mcp.tool(...)` em `mcp_server.py`.

### Adicionar novo prompt MCP

Crie uma funcao com `@mcp.prompt(...)` e consuma via comando `/nome_do_prompt id_doc`.

## Limitacoes atuais

- Nao ha suite de testes automatizados.
- Nao ha configuracao de lint/format/type-check no repositrio.
- Documentos de exemplo sao persistidos apenas em memoria (sem banco/arquivo).

## Troubleshooting rapido

- Erro de `CLAUDE_MODEL` vazio: configure a variavel no `.env`.
- Erro de `ANTHROPIC_API_KEY` vazio: configure chave valida no `.env`.
- Falha ao conectar MCP: confirme se o script do servidor executa sozinho.
- Comando `/...` sem efeito: verifique se o prompt existe em `list_prompts()` do servidor.
