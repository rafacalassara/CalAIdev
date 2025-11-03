# CrewAI - Artigos Técnicos Colaborativos

Projeto simples demonstrando uma equipe CrewAI com agentes de pesquisa, escrita e revisão trabalhando em cadeia para gerar artigos técnicos curtos a partir de um tema fornecido pelo usuário.

![Visão geral da aplicação](./assets/01%20-%20CrewAI.png)
![Estrutura dos agentes](./assets/02%20-%20Estrutura.png)
![Equipe em execução](./assets/03%20-%20Equipe.png)


## Pré-requisitos

Execute os comandos abaixo na ordem para preparar o ambiente:

```powershell
pip install uv
uv init --python=3.12.9
uv add crewai[tools] "crewai[google-genai]" ddgs
```

Caso o `.venv` não seja criado automaticamente:
```powershell
uv venv
uv sync
```

Para executar o projeto:
```powershell
uv run .\main.py
```

## Chave de API do Google Gemini

O arquivo `main.py` utiliza um objeto `LLM` configurado com o modelo `gemini/gemini-2.0-flash`. Substitua a chave presente no código por uma variável de ambiente segura, por exemplo:

```powershell

llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key="YOUR_API_KEY_HERE",
)
```

> **Importante:** Não compartilhe nem versione sua chave real. Gere e gerencie as chaves em <https://aistudio.google.com/u/1/api-keys>.

## Uso

1. Execute `uv run .\main.py`.
2. Informe o tema desejado quando solicitado.
3. O resultado final será exibido no terminal e salvo em `artigo_final.md`.
