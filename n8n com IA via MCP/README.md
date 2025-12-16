# 🚀 N8N com IA via MCP

Integração do **N8N** com assistentes de IA através do protocolo **MCP** (Model Context Protocol) no **VS Code**.

Este projeto permite que você controle e crie workflows do N8N diretamente através de conversas com IA no VS Code!

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Pré-requisitos](#-pré-requisitos)
- [Passo 1: Clonar o Repositório](#-passo-1-clonar-o-repositório)
- [Passo 2: Obter a API Key do N8N](#-passo-2-obter-a-api-key-do-N8N)
- [Passo 3: Ativar o MCP no VS Code](#-passo-3-ativar-o-mcp-no-vs-code)
- [Passo 4: Usar o Agente N8N](#-passo-4-usar-o-agente-N8N)
- [Configuração Avançada](#-configuração-avançada)
- [Troubleshooting](#-troubleshooting)
- [Skills do Agente](#-skills-do-agente)

---

## 🎯 Visão Geral

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  VS Code +      │────▶│    N8N-MCP      │────▶│      N8N        │
│  Copilot        │     │   (Docker)      │     │  (porta 5678)   │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       │
         │                      │                       │
    Você conversa          Traduz comandos         Executa workflows
    com o agente           para API do N8N         e automações
```

### O que você pode fazer:

- ✅ Criar workflows via conversa
- ✅ Listar e gerenciar workflows existentes
- ✅ Validar configurações de nodes
- ✅ Debugar erros em workflows
- ✅ Buscar documentação de nodes

---

## 📦 Pré-requisitos

- **Docker Desktop** instalado e rodando
- **VS Code** com a extensão **GitHub Copilot** configurada
- **N8N** rodando (localmente em `http://localhost:5678` ou em outro servidor)
- Acesso à internet para baixar a imagem Docker do MCP

---

## 📥 Passo 1: Clonar o Repositório

```powershell
# Clone o repositório
git clone https://github.com/rafacalassara/CalAIdev.git

# Entre na pasta do projeto
cd "CalAIdev/n8n com IA via MCP"
```

---

## Passo 2: Obter a API Key do N8N

1. Acesse o N8N em: `http://localhost:5678`
2. Crie sua conta (primeira vez) ou faça login
3. Vá em **Configurações** → **API**
4. Clique em **Create API Key**
5. **Copie e guarde a chave gerada** - você vai precisar dela no próximo passo!

---

## 🖥️ Passo 3: Ativar o MCP no VS Code

### 3.1 Abrir o projeto no VS Code

```powershell
code .
```

### 3.2 Ativar o MCP

1. Abra a **barra lateral do Chat** (ícone do Copilot ou `Ctrl+Shift+I`)
2. Clique no ícone de **ferramentas** (🔧) na parte inferior do chat
3. Procure por **"n8nMcp"** na lista de MCPs
4. **Ative** o MCP clicando no toggle

### 3.3 Configurar as credenciais

Na **primeira vez** que você ativar o MCP, o VS Code vai solicitar duas informações:

1. **N8N API Key** - Cole a API Key que você obteve no Passo 2
2. **MCP Auth Token** - Pode ser qualquer token seguro (ex: gere um em [random.org](https://www.random.org/strings/))

> 💡 **O VS Code armazena essas credenciais de forma segura!** Você só precisa configurar uma vez.

---

## 🤖 Passo 4: Usar o Agente N8N

### 4.1 Selecionar o Agente

1. Na aba de **Chat** do VS Code, olhe na **parte inferior**
2. Clique no seletor de agentes (pode mostrar "Copilot" ou "Ask")
3. Selecione o agente **`n8n-workflow-builder`**

> O agente está definido no arquivo `.github/agents/n8n-workflow-builder.agent.md`

### 4.2 Começar a usar!

Agora é só conversar com o agente! Exemplos de comandos:

```
"Liste todos os workflows do N8N"
```

```
"Crie um workflow que recebe um webhook e envia uma mensagem no Slack"
```

```
"Valide meu workflow e corrija os erros"
```

O agente irá usar as ferramentas MCP para interagir diretamente com seu N8N! 🎉

---

## ⚙️ Configuração Avançada

### Como funciona o mcp.json

O arquivo `.vscode/mcp.json` já vem configurado no projeto. Ele usa o Docker para rodar o servidor MCP:

```json
{
  "inputs": [
    { "type": "promptString", "id": "n8nApiKey", "description": "N8N API Key", "password": true },
    { "type": "promptString", "id": "mcpAuthToken", "description": "MCP Auth Token", "password": true }
  ],
  "servers": {
    "n8nMcp": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "MCP_MODE=stdio",
        "-e", "LOG_LEVEL=error",
        "-e", "N8N_MCP_TELEMETRY_DISABLED=true",
        "-e", "WEBHOOK_SECURITY_MODE=moderate",
        "-e", "N8N_API_URL=http://host.docker.internal:5678",
        "-e", "N8N_API_KEY=${input:n8nApiKey}",
        "-e", "AUTH_TOKEN=${input:mcpAuthToken}",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
```

### Opção alternativa: Credenciais fixas

Se preferir não usar prompts, você pode colocar as credenciais diretamente no arquivo (não recomendado para repositórios públicos):

```json
{
  "servers": {
    "n8nMcp": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "MCP_MODE=stdio",
        "-e", "LOG_LEVEL=error",
        "-e", "N8N_MCP_TELEMETRY_DISABLED=true",
        "-e", "WEBHOOK_SECURITY_MODE=moderate",
        "-e", "N8N_API_URL=http://host.docker.internal:5678",
        "-e", "N8N_API_KEY=SUA_API_KEY_AQUI",
        "-e", "AUTH_TOKEN=SEU_TOKEN_AQUI",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
```

### Conectando a um N8N remoto

Se seu N8N está em outro servidor, altere a variável `N8N_API_URL`:

```json
"-e", "N8N_API_URL=https://seu-N8N.exemplo.com",
```

---

## 🔧 Troubleshooting

### ❌ MCP não aparece na lista de ferramentas

1. Verifique se o arquivo `.vscode/mcp.json` está na pasta `.vscode`
2. Verifique se o JSON está válido (sem erros de sintaxe)
3. Reinicie o VS Code completamente (`Ctrl+Shift+P` → "Reload Window")

### ❌ Erro de conexão com o N8N

1. Verifique se o **Docker Desktop está rodando**
2. Verifique se o **N8N está acessível** em `http://localhost:5678`
3. Verifique se a **API Key está correta**

Para resetar as credenciais:
1. `Ctrl+Shift+P` → "MCP: Reset Cached Inputs"
2. Desative e reative o MCP na lista de ferramentas

### ❌ Erro "denied" ao baixar imagem do GHCR

Se você receber o erro `error from registry: denied`, tente:

```powershell
# Fazer pull da imagem manualmente
docker pull ghcr.io/czlonkowski/n8n-mcp:latest
```

**Alternativas:**
- Use o serviço hospedado gratuito em [dashboard.n8n-mcp.com](https://dashboard.n8n-mcp.com/)
- Use `npx n8n-mcp` diretamente (sem Docker)

### ❌ Agente não encontra as ferramentas do N8N

1. Verifique se o MCP está **ativado** (toggle verde) na lista de ferramentas
2. Verifique se você selecionou o agente **n8n-workflow-builder**
3. Tente perguntar: "Liste os workflows do N8N"

---

## 📚 Skills do Agente

Este projeto inclui skills especializadas para o agente de IA criar workflows no N8N:

| Skill | Descrição |
|-------|-----------|
| **MCP Tools Expert** | Uso correto das ferramentas MCP |
| **Workflow Patterns** | Padrões comuns de workflows |
| **Node Configuration** | Configuração correta de nodes |
| **Validation Expert** | Validação e correção de erros |
| **Expression Syntax** | Sintaxe de expressões do N8N |
| **Code JavaScript** | Code nodes em JavaScript |
| **Code Python** | Code nodes em Python |

Consulte a pasta `n8n-skills/` para documentação detalhada.

---

## 📁 Estrutura do Projeto

```
n8n com IA via MCP/
├── 📄 README.md                      # Este arquivo
├── 📄 AGENTS.md                      # Guardrails para o agente IA
├── 📁 .vscode/                       # Configurações do VS Code
│   └── mcp.json                      # Configuração do MCP (usa Docker)
├── 📁 .github/                       
│   └── agents/                       # Definição dos agentes
│       └── n8n-workflow-builder.agent.md
└── 📁 n8n-skills/                    # Skills do agente
    └── skills/
        ├── n8n-mcp-tools-expert/
        ├── n8n-workflow-patterns/
        ├── n8n-node-configuration/
        └── ...
```

---

## Créditos

Este projeto utiliza os excelentes repositórios criados por **Romuald Członkowski** ([@czlonkowski](https://github.com/czlonkowski)):

| Repositório | Descrição |
|-------------|-----------|
| [**n8n-mcp**](https://github.com/czlonkowski/n8n-mcp) | Servidor MCP para integração com N8N |
| [**n8n-skills**](https://github.com/czlonkowski/n8n-skills) | Skills especializadas para construir workflows N8N com IA |

Muito obrigado ao Romuald por criar e manter essas ferramentas incríveis que tornam possível a integração do N8N com assistentes de IA! 🎉

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🔗 Links Úteis

- [N8N Documentação](https://docs.n8n.io/)
- [N8N Cloud](https://n8n.io/) - Se você não tem N8N instalado
- [MCP Protocol](https://modelcontextprotocol.io/)
- [N8N-MCP GitHub](https://github.com/czlonkowski/n8n-mcp)
- [VS Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub Copilot](https://github.com/features/copilot)

---

<p align="center">
  Feito com ❤️ para a comunidade N8N brasileira
</p>
