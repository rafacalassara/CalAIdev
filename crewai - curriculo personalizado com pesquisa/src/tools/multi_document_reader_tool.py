from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os


class MultiDocumentReaderInput(BaseModel):
    """Schema de entrada para a ferramenta de leitura de documentos"""
    file_path: str = Field(..., description="O caminho completo do arquivo a ser lido (PDF, DOCX, MD ou TXT)")


class MultiDocumentReaderTool(BaseTool):
    name: str = "Document Reader"
    description: str = (
        "Read and extract text content from documents. "
        "Supports PDF, DOCX, Markdown (.md), and plain text (.txt) files. "
        "Use this tool to read resumes, templates, company research documents, and any other text-based files. "
        "Returns the full text content of the document."
    )
    args_schema: Type[BaseModel] = MultiDocumentReaderInput

    def _run(self, file_path: str) -> str:
        """Lê o conteúdo de um documento baseado na sua extensão"""
        
        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            return f"Erro: Arquivo não encontrado: {file_path}"
        
        # Obtém a extensão do arquivo
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        try:
            if ext == '.pdf':
                return self._read_pdf(file_path)
            elif ext == '.docx':
                return self._read_docx(file_path)
            elif ext in ['.md', '.txt', '.markdown']:
                return self._read_text(file_path)
            else:
                return f"Erro: Formato de arquivo não suportado: {ext}. Formatos suportados: PDF, DOCX, MD, TXT"
        except Exception as e:
            return f"Erro ao ler o arquivo {file_path}: {str(e)}"
    
    def _read_pdf(self, file_path: str) -> str:
        """Lê conteúdo de um arquivo PDF usando pypdf"""
        from pypdf import PdfReader
        
        reader = PdfReader(file_path)
        text_content = []
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
        
        if not text_content:
            return "Aviso: O PDF não contém texto extraível (pode ser um PDF de imagem)."
        
        return "\n\n".join(text_content)
    
    def _read_docx(self, file_path: str) -> str:
        """Lê conteúdo de um arquivo DOCX usando docx2txt"""
        import docx2txt
        
        text = docx2txt.process(file_path)
        
        if not text or text.strip() == "":
            return "Aviso: O documento DOCX está vazio ou não contém texto."
        
        return text
    
    def _read_text(self, file_path: str) -> str:
        """Lê conteúdo de arquivos de texto (MD, TXT)"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content or content.strip() == "":
            return "Aviso: O arquivo de texto está vazio."
        
        return content
