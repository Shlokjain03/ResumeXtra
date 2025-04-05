def analyze_resume(text):
    suggestions = []
    score = 100

    if "experience" not in text.lower():
        suggestions.append("Add an experience section.")
        score -= 20

    if "education" not in text.lower():
        suggestions.append("Include your educational qualifications.")
        score -= 15

    if "skills" not in text.lower():
        suggestions.append("Mention your relevant skills.")
        score -= 15

    return suggestions, max(score, 0)

def extract_skills(text):
    keywords = ["Python", "Java", "Flask", "Django", "SQL", "Machine Learning", "Data Analysis"]
    return [kw for kw in keywords if kw.lower() in text.lower()]
