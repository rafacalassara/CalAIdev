import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import ScrapeWebsiteTool
from tools.multi_document_reader_tool import MultiDocumentReaderTool


@CrewBase
class TailorResumeCrew():
    """Tailor Resume Crew - Personalizes resumes for specific job positions"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    llm_model: LLM = None
    inputs: dict = None

    def __init__(self, inputs: dict, model: str = None):
        self.llm_config(model)
        self.inputs = inputs

    def llm_config(self, model: str) -> LLM:
        self.llm_model = LLM(
            model=os.getenv('LLM_MODEL', 'gpt-5-mini') if not model else model,
        )
        return self.llm_model

    @agent
    def resume_converter(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_converter'],
            tools=[MultiDocumentReaderTool()],
            llm=self.llm_model,
            verbose=True
        )

    @agent
    def job_requirements_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['job_requirements_analyst'],
            tools=[ScrapeWebsiteTool()],
            llm=self.llm_model,
            verbose=True
        )

    @agent
    def resume_personalizer(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_personalizer'],
            tools=[MultiDocumentReaderTool()],
            llm=self.llm_model,
            verbose=True
        )

    # Tasks
    @task
    def convert_resume_task(self) -> Task:
        return Task(
            config=self.tasks_config['convert_resume_task'],
            output_file=self.inputs['md_target_resume_path'],
            agent=self.resume_converter()
        )

    @task
    def analyze_job_requirements_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_job_requirements_task'],
            agent=self.job_requirements_analyst()
        )

    @task
    def personalize_resume_task(self) -> Task:
        return Task(
            config=self.tasks_config['personalize_resume_task'],
            output_file=self.inputs['crew_generated_resume_path'],
            agent=self.resume_personalizer()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


if __name__ == '__main__':
    inputs = {
        'resume_path': 'inputs/sample_resume.pdf',
        'resume_template_path': 'inputs/resume_template.md',
        'job_posting': 'https://www.linkedin.com/jobs/view/4300149206/',
        'company_research_path': 'outputs/company_research.md',
        'user_considerations_for_resume_crew': 'Focus on Python and AI/ML experience',
        'resume_language': 'pt-BR',
        'current_date': '2025-12-16',
        'md_target_resume_path': 'outputs/converted_resume.md',
        'crew_generated_resume_path': 'outputs/personalized_resume.md',
    }
    crew_instance = TailorResumeCrew(inputs=inputs)
    result = crew_instance.crew().kickoff(inputs=inputs)
    print(result)
