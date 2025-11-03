import textwrap

from ddgs import DDGS
from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool


class WebSearchTool(BaseTool):
    """Ferramenta personalizada para buscar informações na web usando DuckDuckGo."""
    name: str = "Busca na Web"
    description: str = "Busca informações na web para uma consulta dada"

    def _run(self, query: str) -> str:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            return "\n".join([f"{r['title']}: {r['body']}" for r in results])


# Definindo Modelo LLM
llm = LLM(
    model="gemini/gemini-2.0-flash", # https://ai.google.dev/gemini-api/docs/models
    api_key="YOUR_API_KEY_HERE",  # https://aistudio.google.com/u/1/api-keys
)

# Definindo os agentes
def criar_agentes() -> list[Agent]:
    """Cria os agentes da equipe: Pesquisador, Escritor e Revisor."""
    
    agente_pesquisa = Agent(
        role="Agente de Pesquisa",
        goal=textwrap.dedent("""
            Realizar pesquisa aprofundada sobre o tema fornecido usando busca na web.
            Coletar informações precisas, atualizadas e relevantes.
            """).strip(),
        backstory=textwrap.dedent("""
            Você é um pesquisador especialista que utiliza ferramentas de busca na web
            para encontrar informações precisas e atualizadas sobre qualquer tema.
            Sua missão é fornecer dados confiáveis para apoiar a criação de conteúdo.
            """).strip(),
        tools=[WebSearchTool()],
        llm=llm,
        verbose=True
    )
    
    agente_escritor = Agent(
        role="Agente Escritor",
        goal=textwrap.dedent("""
            Escrever um artigo técnico claro e envolvente baseado nas descobertas da pesquisa.
            Estruturar o conteúdo de forma lógica e informativa.
            """).strip(),
        backstory=textwrap.dedent("""
            Você é um escritor técnico habilidoso que cria artigos informativos e bem estruturados.
            Seu objetivo é transformar dados de pesquisa em conteúdo acessível e interessante.
            """).strip(),
        llm=llm,
        verbose=True
    )
    
    agente_revisor = Agent(
        role="Agente Revisor",
        goal=textwrap.dedent("""
            Revisar o artigo para verificar precisão, clareza, gramática e completude.
            Sugerir melhorias e fornecer a versão final polida.
            """).strip(),
        backstory=textwrap.dedent("""
            Você é um revisor meticuloso que garante a qualidade do conteúdo técnico.
            Sua atenção aos detalhes ajuda a refinar artigos para máxima clareza e impacto.
            """).strip(),
        llm=llm,
        verbose=True
    )
    
    return agente_pesquisa, agente_escritor, agente_revisor


def criar_tarefas(agente_pesquisa: Agent, agente_escritor: Agent, agente_revisor: Agent) -> list[Task]:
    """Cria as tarefas para a equipe: Pesquisa, Escrita e Revisão."""
    
    tarefa_pesquisa = Task(
        description=textwrap.dedent("""
            Pesquise o tema '{topic}' de forma aprofundada usando busca na web.
            Forneça descobertas detalhadas, pontos-chave e fontes.
            """).strip(),
        expected_output="Um resumo de pesquisa abrangente com informações-chave e fontes.",
        agent=agente_pesquisa
    )
    
    tarefa_escrita = Task(
        description=textwrap.dedent("""
            Escreva um artigo técnico sobre o tema baseado nas descobertas da pesquisa.
            Torne-o informativo, bem estruturado e envolvente.
            """).strip(),
        expected_output="Um artigo técnico completo pronto para revisão.",
        agent=agente_escritor,
        context=[tarefa_pesquisa]
    )
    
    tarefa_revisao = Task(
        description=textwrap.dedent("""
            Revise o artigo escrito para verificar precisão, gramática, clareza e completude.
            Forneça a versão final polida com quaisquer melhorias feitas.
            """).strip(),
        expected_output="O artigo final polido com melhorias implementadas em português brasileiro.",
        agent=agente_revisor,
        context=[tarefa_escrita],
        output_file="artigo_final.md"
    )
    
    return tarefa_pesquisa, tarefa_escrita, tarefa_revisao


def criar_equipe(agentes: list[Agent], tarefas: list[Task]) -> Crew:
    """Cria a equipe CrewAI com agentes e tarefas."""
    return Crew(
        agents=agentes,
        tasks=tarefas,
        verbose=True
    )


if __name__ == "__main__":
    # Cria agentes e tarefas
    agentes = criar_agentes()
    tarefas = criar_tarefas(*agentes)
    
    # Cria a equipe
    equipe = criar_equipe(agentes, tarefas)
    
    # Executa o processo
    tema = input("Digite o tema para o artigo: ")
    resultado = equipe.kickoff(inputs={"topic": tema})
    
    print("\n=== ARTIGO FINAL ===\n")
    print(resultado)