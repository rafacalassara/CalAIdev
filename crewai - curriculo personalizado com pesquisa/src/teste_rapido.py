from crews.companies_research_crew.companies_research_crew import CompaniesResearchCrew
from crews.tailor_resume_crew.tailor_resume_crew import TailorResumeCrew

if __name__ == '__main__':
    inputs = {
        # Companies Research Crew
        'company': 'AnswerThis (YC F25)',
        'user_considerations_for_companies_research_crew': '',

        # Tailor Resume Crew
        'resume_path': 'inputs/Profile.pdf',
        'resume_template_path': 'inputs/resume_template.md',
        'user_considerations_for_resume_crew': 'Focus on Python and AI/ML experience',
        'md_target_resume_path': 'outputs/converted_resume.md',
        'crew_generated_resume_path': 'outputs/personalized_resume.md',

        # Inputs Gerais
        'company_research_path': 'outputs/company_research.md',
        'job_posting': 'https://www.linkedin.com/jobs/view/4300149206/',
        'current_date': '2025-12-16',
        'resume_language': 'pt-br',
    }
    companies_crew_instance = CompaniesResearchCrew(inputs=inputs)
    companies_crew_instance.crew().kickoff(inputs=inputs)

    resume_crew_instance = TailorResumeCrew(inputs=inputs)
    resume_crew_instance.crew().kickoff(inputs=inputs)