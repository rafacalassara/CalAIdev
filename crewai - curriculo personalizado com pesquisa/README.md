# 🎯 CalAI - Currículo Personalizado com Pesquisa

Sistema de personalização automática de currículos baseado em IA, utilizando [CrewAI](https://www.crewai.com/) para orquestrar agentes inteligentes que pesquisam empresas e adaptam seu currículo para vagas específicas.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-1.2.1+-green?style=for-the-badge)
![Gradio](https://img.shields.io/badge/Gradio-5.49+-orange?style=for-the-badge&logo=gradio&logoColor=white)

## 📋 Sobre o Projeto

O CalAI automatiza o processo de personalização de currículos através de duas equipes de agentes de IA:

### 🔍 Companies Research Crew
Equipe responsável por pesquisar informações sobre a empresa e a vaga:
- **Researcher**: Pesquisa informações relevantes sobre a empresa usando DuckDuckGo e scraping de websites
- **Reporting Analyst**: Compila as informações em um relatório estruturado

### 📄 Tailor Resume Crew
Equipe responsável por personalizar o currículo:
- **Resume Converter**: Converte o currículo original (PDF, DOCX, etc.) para formato Markdown estruturado
- **Job Requirements Analyst**: Analisa os requisitos da vaga através do link fornecido
- **Resume Personalizer**: Gera um currículo personalizado baseado na pesquisa da empresa e requisitos da vaga

## ⚙️ Pré-requisitos

- **Python 3.11+**
- **[uv](https://docs.astral.sh/uv/)** - Gerenciador de pacotes e ambientes Python
- **Chave de API da OpenAI**

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositório>
cd crewai-curriculo-personalizado-com-pesquisa
```

### 2. Instale o uv (se ainda não tiver)

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e configure sua chave da API:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da OpenAI:

```env
OPENAI_API_KEY=sua-chave-aqui
```

### 4. Instale as dependências

O uv irá criar automaticamente um ambiente virtual e instalar as dependências:

```bash
uv sync
```

## 🖥️ Executando a Aplicação

Para iniciar a interface gráfica Gradio:

```bash
uv run src/app.py
```

A aplicação será iniciada e estará disponível em: **http://127.0.0.1:7860**

## 📁 Estrutura do Projeto

```
crewai-curriculo-personalizado-com-pesquisa/
├── inputs/                          # Arquivos de entrada
│   ├── resume_template.md           # Template de currículo em Markdown
│   └── Profile.pdf                  # Exemplo de currículo
├── outputs/                         # Arquivos gerados
│   ├── company_research.md          # Relatório de pesquisa da empresa
│   ├── converted_resume.md          # Currículo convertido para MD
│   └── personalized_resume.md       # Currículo personalizado final
├── src/
│   ├── app.py                       # Interface Gradio principal
│   ├── crews/
│   │   ├── companies_research_crew/ # Crew de pesquisa de empresas
│   │   │   ├── config/
│   │   │   │   ├── agents.yaml      # Configuração dos agentes
│   │   │   │   └── tasks.yaml       # Configuração das tarefas
│   │   │   └── companies_research_crew.py
│   │   └── tailor_resume_crew/      # Crew de personalização de currículo
│   │       ├── config/
│   │       │   ├── agents.yaml
│   │       │   └── tasks.yaml
│   │       └── tailor_resume_crew.py
│   └── tools/                       # Ferramentas customizadas
│       ├── ddgs_tool.py             # Ferramenta de busca DuckDuckGo
│       └── multi_document_reader_tool.py  # Leitor de múltiplos formatos
├── .env                             # Variáveis de ambiente (não versionado)
├── .env.example                     # Exemplo de variáveis de ambiente
├── pyproject.toml                   # Configuração do projeto e dependências
└── uv.lock                          # Lock file do uv
```

## 🎮 Como Usar

1. **Acesse a interface** em http://127.0.0.1:7860 após iniciar a aplicação

2. **Faça upload do seu currículo** (formatos suportados: PDF, DOCX, DOC, MD, TXT, RTF)

3. **Cole a URL da vaga** de emprego (ex: link do LinkedIn Jobs)

4. **Opcionalmente**, informe:
   - Nome da empresa (ajuda na pesquisa)
   - Considerações para a equipe de pesquisa
   - Considerações para a estruturação do currículo

5. **Clique em "🚀 Processar Currículo"**

6. **Aguarde o processamento** - o sistema irá:
   - Pesquisar informações sobre a empresa
   - Analisar a vaga de emprego
   - Converter seu currículo para Markdown
   - Gerar um currículo personalizado

7. **Visualize os resultados** nas abas:
   - **Currículo Personalizado**: Seu currículo adaptado para a vaga
   - **Relatório de Pesquisa**: Informações coletadas sobre a empresa

8. **Faça download** do currículo personalizado em formato Markdown

## 🔧 Configuração Avançada

### Modelo de IA

Por padrão, o sistema utiliza o modelo `gpt-5-mini`. Você pode alterar o modelo definindo a variável de ambiente:

```env
LLM_MODEL=gpt-5
```

### Template de Currículo

O template de currículo em `inputs/resume_template.md` define a estrutura esperada do currículo gerado. Você pode personalizar este template conforme suas preferências.

## 📦 Dependências Principais

| Pacote | Descrição |
|--------|-----------|
| `crewai[tools]` | Framework de orquestração de agentes de IA |
| `gradio` | Interface web interativa |
| `pypdf` | Leitura de arquivos PDF |
| `docx2txt` | Leitura de arquivos DOCX |
| `duckduckgo-search` | Pesquisa na web via DuckDuckGo |
| `markdown2` | Conversão de Markdown |

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Desenvolvido com ❤️ por CalAI.dev**
