#!/usr/bin/env python3
"""Quick test of job scoring logic"""

student_skills = ['Python', 'JavaScript', 'React']

jobs = [
    {'title': 'Junior Developer', 'requirements': ['Python', 'JavaScript'], 'is_remote': True, 'salary_min': 50000},
    {'title': 'Senior Engineer', 'requirements': ['Python', 'Go', 'Kubernetes'], 'is_remote': False, 'salary_min': None},
    {'title': 'Full Stack Developer', 'requirements': ['JavaScript', 'React', 'Node.js'], 'is_remote': True, 'salary_min': 60000},
    {'title': 'Backend Developer', 'requirements': ['Python', 'Django', 'PostgreSQL'], 'is_remote': False, 'salary_min': 55000},
]

def calc_skill_score(student_skills, required_skills):
    if not required_skills:
        return 0.5
    student_set = set(s.lower() for s in student_skills)
    required_set = set(s.lower() for s in required_skills)
    matched = len(student_set.intersection(required_set))
    return min(matched / len(required_set), 1.0)

def calc_interest_score(title):
    title_lower = title.lower()
    if any(word in title_lower for word in ['junior', 'entry', 'intern', 'associate', 'graduate']):
        return 0.9
    elif any(word in title_lower for word in ['senior', 'lead', 'principal', 'staff']):
        return 0.4
    else:
        return 0.7

def calc_popularity_score(job):
    score = 0.5
    if job.get('is_remote'):
        score += 0.2
    if job.get('salary_min') or job.get('salary_max'):
        score += 0.2
    if job.get('requirements') and len(job['requirements']) >= 3:
        score += 0.1
    return min(score, 1.0)

# Weights
W_EMB = 0.40
W_SKILL = 0.25
W_INT = 0.15
W_POP = 0.10
W_ACT = 0.10

print("\nJob Match Scores:")
print("=" * 80)

for job in jobs:
    skill_score = calc_skill_score(student_skills, job['requirements'])
    interest_score = calc_interest_score(job['title'])
    popularity_score = calc_popularity_score(job)
    activity_score = 0.8  # Assume recent
    embedding_score = skill_score * 0.8 + 0.1
    
    final_score = (W_EMB * embedding_score + W_SKILL * skill_score + 
                   W_INT * interest_score + W_POP * popularity_score + W_ACT * activity_score)
    
    match_pct = int(final_score * 100)
    print(f"\n{job['title']}:")
    print(f"  Match: {match_pct}%")
    print(f"  - Skill Match: {skill_score:.2f} ({int(skill_score*100)}%)")
    print(f"  - Interest: {interest_score:.1f}")
    print(f"  - Popularity: {popularity_score:.1f}")
    print(f"  - Embedding: {embedding_score:.2f}")

print("\n" + "=" * 80)
