"""
Interface Gradio para Currículo Personalizado com Pesquisa

Esta aplicação permite ao usuário fazer upload de um currículo,
informar a URL de uma vaga e receber um currículo personalizado
junto com um relatório de pesquisa da empresa.

NanoBanana + Gradio: Integração com CrewAI para personalização de currículos.
"""

import gradio as gr
import tempfile
import os
import shutil
from datetime import datetime

# Importar as crews do CrewAI
from crews.companies_research_crew.companies_research_crew import CompaniesResearchCrew
from crews.tailor_resume_crew.tailor_resume_crew import TailorResumeCrew


def read_file_content(file_path: str) -> str:
    """Lê o conteúdo de um arquivo de texto."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"


def extract_company_name(job_url: str, company_name: str = "") -> str:
    """Extrai ou usa o nome da empresa fornecido."""
    if company_name and company_name.strip():
        return company_name.strip()
    # Se não foi fornecido, retornar string genérica para pesquisa
    return "Empresa da vaga"


def process_resume(
    resume_file,
    job_url: str,
    company_name: str = "",
    research_considerations: str = "",
    resume_considerations: str = ""
) -> tuple[str, str, str]:
    """
    Processa o currículo através das Crews do CrewAI.
    
    Fluxo de execução:
    1. CompaniesResearchCrew - Pesquisa informações sobre a empresa
    2. TailorResumeCrew - Personaliza o currículo com base na pesquisa
    
    Args:
        resume_file: Arquivo do currículo (PDF, DOCX, MD, TXT)
        job_url: URL da vaga de emprego
        company_name: Nome da empresa (opcional)
        research_considerations: Considerações para equipe de pesquisa (opcional)
        resume_considerations: Considerações para equipe de estruturação (opcional)
    
    Returns:
        tuple: (currículo_markdown, relatório_markdown, caminho_download)
    """
    
    if not resume_file:
        raise gr.Error("Por favor, faça upload do seu currículo.")
    
    if not job_url or not job_url.strip():
        raise gr.Error("Por favor, informe a URL da vaga.")
    
    # ================================================================
    # CONFIGURAÇÃO DOS CAMINHOS DE ARQUIVOS
    # ================================================================
    
    # Diretório base do projeto (um nível acima de src/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Diretórios de entrada e saída
    inputs_dir = os.path.join(base_dir, "inputs")
    outputs_dir = os.path.join(base_dir, "outputs")
    
    # Garantir que os diretórios existem
    os.makedirs(inputs_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Caminhos dos arquivos de saída
    company_research_path = os.path.join(outputs_dir, "company_research.md")
    converted_resume_path = os.path.join(outputs_dir, "converted_resume.md")
    personalized_resume_path = os.path.join(outputs_dir, "personalized_resume.md")
    
    # Caminho do template do currículo
    resume_template_path = os.path.join(inputs_dir, "resume_template.md")
    
    # Copiar o arquivo de currículo para o diretório de inputs (se necessário)
    resume_filename = os.path.basename(resume_file)
    resume_input_path = os.path.join(inputs_dir, resume_filename)
    
    # Copiar apenas se não for o mesmo arquivo
    if os.path.abspath(resume_file) != os.path.abspath(resume_input_path):
        shutil.copy2(resume_file, resume_input_path)
    
    # Obter data atual
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Extrair nome da empresa
    company = extract_company_name(job_url, company_name)
    
    # ================================================================
    # ETAPA 1: COMPANIES RESEARCH CREW
    # Pesquisa informações sobre a empresa e a vaga
    # ================================================================
    
    try:
        # Inputs para a crew de pesquisa de empresas
        companies_research_inputs = {
            'company': company,
            'job_posting': job_url,
            'current_date': current_date,
            'company_research_path': company_research_path,
            'user_considerations_for_companies_research_crew': research_considerations or '',
            'resume_language': 'pt-BR',
        }
        
        # Criar e executar a crew de pesquisa
        companies_crew = CompaniesResearchCrew(inputs=companies_research_inputs)
        companies_result = companies_crew.crew().kickoff(inputs=companies_research_inputs)
        
        # Capturar o resultado usando .raw (MD completo não renderizado)
        company_report = companies_result.raw if hasattr(companies_result, 'raw') else str(companies_result)
        
    except Exception as e:
        # Em caso de erro, criar relatório com informação do erro
        company_report = f"""# ⚠️ Erro na Pesquisa da Empresa

Ocorreu um erro durante a pesquisa da empresa:

```
{str(e)}
```

A equipe de personalização do currículo continuará sem as informações da pesquisa.
"""
        # Criar arquivo de pesquisa vazio para não bloquear a próxima etapa
        with open(company_research_path, "w", encoding="utf-8") as f:
            f.write(company_report)
    
    # ================================================================
    # ETAPA 2: TAILOR RESUME CREW
    # Personaliza o currículo com base na pesquisa e na vaga
    # ================================================================
    
    try:
        # Inputs para a crew de personalização de currículo
        tailor_resume_inputs = {
            # Arquivo do currículo original
            'resume_path': resume_input_path,
            'resume_template_path': resume_template_path,
            
            # Informações da vaga
            'job_posting': job_url,
            
            # Resultado da pesquisa da empresa
            'company_research_path': company_research_path,
            
            # Caminhos de saída
            'md_target_resume_path': converted_resume_path,
            'crew_generated_resume_path': personalized_resume_path,
            
            # Considerações do usuário
            'user_considerations_for_resume_crew': resume_considerations or '',
            
            # Configurações gerais
            'resume_language': 'pt-BR',
            'current_date': current_date,
        }
        
        # Criar e executar a crew de personalização
        resume_crew = TailorResumeCrew(inputs=tailor_resume_inputs)
        resume_result = resume_crew.crew().kickoff(inputs=tailor_resume_inputs)
        
        # Capturar o resultado usando .raw (MD completo não renderizado)
        tailored_resume = resume_result.raw if hasattr(resume_result, 'raw') else str(resume_result)
        
    except Exception as e:
        # Em caso de erro, criar mensagem de erro
        tailored_resume = f"""# ⚠️ Erro na Personalização do Currículo

Ocorreu um erro durante a personalização do currículo:

```
{str(e)}
```

Por favor, verifique os logs para mais detalhes.
"""
    
    # ================================================================
    # FINALIZAÇÃO: Preparar arquivos para download
    # ================================================================
    
    # Usar o arquivo gerado pela crew ou criar um temporário
    if os.path.exists(personalized_resume_path):
        download_path = personalized_resume_path
    else:
        # Criar arquivo temporário para download
        temp_dir = tempfile.gettempdir()
        download_path = os.path.join(temp_dir, "curriculo_personalizado.md")
        with open(download_path, "w", encoding="utf-8") as f:
            f.write(tailored_resume)
    
    return tailored_resume, company_report, download_path


def create_interface():
    """Cria e retorna a interface Gradio."""
    
    with gr.Blocks() as demo:
        
        # Header
        gr.Markdown("""
        # 🎯 CalAI - Currículo Personalizado
        **Personalize seu currículo automaticamente com base na vaga desejada**
        """)
        
        with gr.Row():
            # Coluna de entrada
            with gr.Column(scale=1):
                gr.Markdown("### 📄 Dados de Entrada")
                
                resume_upload = gr.File(
                    label="Currículo",
                    file_types=[".pdf", ".docx", ".doc", ".md", ".txt", ".rtf"],
                    file_count="single",
                    type="filepath"
                )
                
                job_url = gr.Textbox(
                    label="URL da Vaga *",
                    placeholder="https://www.linkedin.com/jobs/view/...",
                    info="Cole aqui o link da vaga de emprego"
                )
                
                company_name = gr.Textbox(
                    label="Nome da Empresa (opcional)",
                    placeholder="Ex: Google, Microsoft, Nubank..."
                )
                
                with gr.Accordion("⚙️ Configurações Avançadas", open=False):
                    research_notes = gr.Textbox(
                        label="Considerações para Equipe de Pesquisa",
                        placeholder="Informações adicionais sobre a empresa ou vaga que podem ajudar na pesquisa...",
                        lines=3
                    )
                    
                    resume_notes = gr.Textbox(
                        label="Considerações para Estruturação do Currículo",
                        placeholder="Preferências específicas sobre como estruturar o currículo...",
                        lines=3
                    )
                
                process_btn = gr.Button(
                    "🚀 Processar Currículo",
                    variant="primary",
                    size="lg"
                )
        
        # Área de saída com abas
        gr.Markdown("---")
        gr.Markdown("### 📊 Resultados")
        
        with gr.Tabs() as output_tabs:
            with gr.Tab("📄 Currículo Personalizado"):
                resume_output = gr.Markdown(
                    value="_Aguardando processamento..._",
                    label="Currículo Renderizado"
                )
                download_file = gr.File(
                    label="Download do Currículo",
                    visible=False,
                    interactive=False
                )
            
            with gr.Tab("🔍 Relatório de Pesquisa"):
                report_output = gr.Markdown(
                    value="_Aguardando processamento..._",
                    label="Relatório da Empresa"
                )
        
        # Função para processar e atualizar a UI
        def on_process(resume_file, job_url, company_name, research_notes, resume_notes):
            resume_md, report_md, download_path = process_resume(
                resume_file,
                job_url,
                company_name,
                research_notes,
                resume_notes
            )
            return (
                resume_md,
                report_md,
                gr.File(value=download_path, visible=True)
            )
        
        # Conectar botão à função
        process_btn.click(
            fn=on_process,
            inputs=[resume_upload, job_url, company_name, research_notes, resume_notes],
            outputs=[resume_output, report_output, download_file],
            show_progress="full"
        )
        
        # Footer
        gr.Markdown("""
        ---
        💡 **Dica:** Quanto mais informações você fornecer, melhor será a personalização do seu currículo.
        
        🔧 *Protótipo desenvolvido com Gradio + NanoBanana*
        """)
    
    return demo


if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )
