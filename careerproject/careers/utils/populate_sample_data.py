import os
import django
from datetime import datetime
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerprojectcls.settings')
django.setup()

from django.contrib.auth.models import User
from ..models.user import UserProfile
from ..models.career import CareerPath, ProfessionalQualification
from ..models.education import EducationPath, University, UniversityCareerPath

@transaction.atomic
def populate_data():
    print("Deleting old data...")
    User.objects.all().delete()
    CareerPath.objects.all().delete()
    University.objects.all().delete()
    
    print("Creating sample users...")
    users = [
        {'username': 'student1', 'email': 'student1@example.com', 'password': 'testpass123'},
        {'username': 'career_changer', 'email': 'changer@example.com', 'password': 'testpass123'},
        {'username': 'grad_student', 'email': 'grad@example.com', 'password': 'testpass123'},
    ]
    
    for user_data in users:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        UserProfile.objects.create(
            user=user,
            hobbies=['photography', 'hiking', 'coding'],
            passions=['environmental sustainability', 'education'],
            skills=['Python', 'JavaScript', 'Data Analysis'],
            vision="To make a positive impact through technology",
            dream="Become a CTO of a sustainability-focused tech company"
        )
    
    print("Creating career paths...")
    career_paths = [
        {
            'title': 'Software Engineer',
            'description': 'Design, develop, and maintain software applications and systems.',
            'required_skills': ['Python', 'JavaScript', 'Algorithms', 'Data Structures', 'Cloud Computing'],
            'salary_range': '$70,000 - $120,000',
            'job_outlook': 'Much faster than average (22% growth)',
            'industry': 'Technology'
        },
        {
            'title': 'Data Scientist',
            'description': 'Extract insights from complex data to drive business decisions.',
            'required_skills': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics'],
            'salary_range': '$85,000 - $140,000',
            'job_outlook': 'Much faster than average (31% growth)',
            'industry': 'Technology'
        },
        {
            'title': 'Sustainability Consultant',
            'description': 'Help organizations implement environmentally sustainable practices.',
            'required_skills': ['Environmental Science', 'Project Management', 'Data Analysis', 'Communication'],
            'salary_range': '$60,000 - $110,000',
            'job_outlook': 'Faster than average (11% growth)',
            'industry': 'Environmental Services'
        }
    ]
    
    created_careers = []
    for career_data in career_paths:
        career = CareerPath.objects.create(**career_data)
        created_careers.append(career)
    
    print("Creating professional qualifications...")
    qualifications = [
        {
            'career_path': created_careers[0],  # Software Engineer
            'name': 'AWS Certified Developer - Associate',
            'issuing_organization': 'Amazon Web Services',
            'description': 'Validates technical expertise in developing and maintaining AWS applications.',
            'exam_requirements': '1 exam, 130 minutes, multiple choice',
            'average_salary_boost': 15.0,
            'marketability_boost': 20.0
        },
        {
            'career_path': created_careers[1],  # Data Scientist
            'name': 'Google Professional Data Engineer',
            'issuing_organization': 'Google',
            'description': 'Demonstrates ability to design data processing systems and machine learning models.',
            'exam_requirements': '1 exam, 2 hours, hands-on labs',
            'average_salary_boost': 18.0,
            'marketability_boost': 25.0
        },
        {
            'career_path': created_careers[2],  # Sustainability Consultant
            'name': 'LEED Green Associate',
            'issuing_organization': 'US Green Building Council',
            'description': 'Demonstrates knowledge of green building principles and practices.',
            'exam_requirements': '2-hour exam, 100 multiple-choice questions',
            'average_salary_boost': 12.0,
            'marketability_boost': 15.0
        }
    ]
    
    for qual_data in qualifications:
        ProfessionalQualification.objects.create(**qual_data)
    
    print("Creating universities...")
    universities = [
        {
            'name': 'Massachusetts Institute of Technology',
            'country': 'USA',
            'global_ranking': 1,
            'program_strengths': ['Computer Science', 'Engineering', 'Artificial Intelligence'],
            'industry_connections': ['Google', 'Microsoft', 'NASA'],
            'notable_alumni': ['Buzz Aldrin', 'Kofi Annan'],
            'internship_opportunities': True,
            'average_graduate_salary': 95000
        },
        {
            'name': 'Stanford University',
            'country': 'USA',
            'global_ranking': 2,
            'program_strengths': ['Computer Science', 'Business', 'Environmental Science'],
            'industry_connections': ['Apple', 'Facebook', 'Tesla'],
            'notable_alumni': ['Elon Musk', 'Sergey Brin'],
            'internship_opportunities': True,
            'average_graduate_salary': 92000
        },
        {
            'name': 'ETH Zurich',
            'country': 'Switzerland',
            'global_ranking': 6,
            'program_strengths': ['Environmental Science', 'Engineering', 'Physics'],
            'industry_connections': ['CERN', 'Nestle', 'UBS'],
            'notable_alumni': ['Albert Einstein', 'John von Neumann'],
            'internship_opportunities': True,
            'average_graduate_salary': 88000
        }
    ]
    
    created_universities = []
    for uni_data in universities:
        university = University.objects.create(**uni_data)
        created_universities.append(university)
    
    print("Creating education paths...")
    education_paths = [
        {
            'career_path': created_careers[0],  # Software Engineer
            'degree_name': 'Bachelor of Science in Computer Science',
            'recommended_majors': ['Computer Science', 'Software Engineering', 'Computer Engineering'],
            'typical_duration': '4 years',
            'top_universities': [
                {'name': 'MIT', 'rank': 1},
                {'name': 'Stanford', 'rank': 2},
                {'name': 'Carnegie Mellon', 'rank': 3}
            ]
        },
        {
            'career_path': created_careers[1],  # Data Scientist
            'degree_name': 'Master of Science in Data Science',
            'recommended_majors': ['Data Science', 'Computer Science', 'Statistics'],
            'typical_duration': '2 years',
            'top_universities': [
                {'name': 'Stanford', 'rank': 1},
                {'name': 'MIT', 'rank': 2},
                {'name': 'UC Berkeley', 'rank': 3}
            ]
        },
        {
            'career_path': created_careers[2],  # Sustainability Consultant
            'degree_name': 'Bachelor of Environmental Science',
            'recommended_majors': ['Environmental Science', 'Sustainability Studies', 'Environmental Policy'],
            'typical_duration': '4 years',
            'top_universities': [
                {'name': 'ETH Zurich', 'rank': 1},
                {'name': 'Stanford', 'rank': 2},
                {'name': 'Wageningen University', 'rank': 3}
            ]
        }
    ]
    
    for edu_data in education_paths:
        EducationPath.objects.create(**edu_data)
    
    print("Creating university-career path relationships...")
    university_career_links = [
        {'university': created_universities[0], 'career_path': created_careers[0], 'strength_rating': 4.8},
        {'university': created_universities[0], 'career_path': created_careers[1], 'strength_rating': 4.5},
        {'university': created_universities[1], 'career_path': created_careers[0], 'strength_rating': 4.7},
        {'university': created_universities[1], 'career_path': created_careers[1], 'strength_rating': 4.9},
        {'university': created_universities[2], 'career_path': created_careers[2], 'strength_rating': 4.6},
    ]
    
    for link_data in university_career_links:
        UniversityCareerPath.objects.create(**link_data)
    
    print("Sample data population complete!")

if __name__ == '__main__':
    populate_data()