import re

def extract_skills(text):
    skills = ['Python', 'Django', 'Machine Learning', 'Data Analysis', 'Communication', 'Leadership']
    extracted = [skill for skill in skills if re.search(rf'\b{skill}\b', text, re.IGNORECASE)]
    return extracted

