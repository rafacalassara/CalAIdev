from crews.companies_research_crew.companies_research_crew import CompaniesResearchCrew

if __name__ == '__main__':
    inputs = {
        'company': 'AnswerThis (YC F25)',
        'job_posting': 'https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4300149206',
        'current_date': '2025-12-04',
        'resume_language': 'pt-br',
        'user_considerations_for_companies_research_crew': '',
    }
    equipe = CompaniesResearchCrew(
        inputs=inputs,
    )
    
    equipe.crew().kickoff(inputs=inputs)