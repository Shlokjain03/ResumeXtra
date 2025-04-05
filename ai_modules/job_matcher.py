def recommend_jobs(user_skills):
    job_db = [
        {"title": "Data Analyst", "skills": ["Python", "SQL", "Data Analysis"]},
        {"title": "Backend Developer", "skills": ["Flask", "Python", "SQL"]},
        {"title": "ML Engineer", "skills": ["Python", "Machine Learning", "Data Analysis"]},
    ]
    
    recommended = []
    for job in job_db:
        match_count = len(set(user_skills) & set(job['skills']))
        if match_count:
            job['match_percent'] = int((match_count / len(job['skills'])) * 100)
            recommended.append(job)
    return sorted(recommended, key=lambda x: x['match_percent'], reverse=True)