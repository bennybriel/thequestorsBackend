from datetime import datetime
from typing import Dict, Any
from ...models.career import CareerPath, ProfessionalQualification
from ...models.education import EducationPath, University
from ..interfaces import IPlanGenerator

class PlanGenerator(IPlanGenerator):
    def generate(self, career_path_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        career_path = CareerPath.objects.get(id=career_path_id)
        education_path = EducationPath.objects.filter(career_path=career_path).first()
        
        if not education_path:
            raise ValueError("No education path found for this career")
        
        return {
            'career': self._get_career_data(career_path),
            'education': self._get_education_data(education_path),
            'qualifications': self._get_qualifications(career_path),
            'timeline': self._generate_timeline(career_path, education_path),
            'salary_projection': self._generate_salary_projection(career_path)
        }
    
    def _get_career_data(self, career_path):
        return {
            'title': career_path.title,
            'description': career_path.description,
            'required_skills': career_path.required_skills,
            'salary_range': career_path.salary_range,
            'job_outlook': career_path.job_outlook
        }
    
    def _get_education_data(self, education_path):
        universities = University.objects.filter(
            university_career_paths__career_path=education_path.career_path,
            university_career_paths__strength_rating__gte=4.0
        ).order_by('global_ranking')[:5]
        
        return {
            'degree': education_path.degree_name,
            'duration': education_path.typical_duration,
            'recommended_majors': education_path.recommended_majors,
            'universities': [
                {
                    'name': uni.name,
                    'country': uni.country,
                    'ranking': uni.global_ranking,
                    'salary': float(uni.average_graduate_salary)
                }
                for uni in universities
            ]
        }
    
    def _get_qualifications(self, career_path):
        quals = ProfessionalQualification.objects.filter(
            career_path=career_path
        ).order_by('-marketability_boost')[:3]
        
        return [
            {
                'name': qual.name,
                'issuer': qual.issuing_organization,
                'description': qual.description,
                'salary_boost': float(qual.average_salary_boost)
            }
            for qual in quals
        ]
    
    def _generate_timeline(self, career_path, education_path):
        current_year = datetime.now().year
        duration = int(education_path.typical_duration.split()[0])
        
        timeline = []
        for year in range(duration + 5):  # Education + 5 years career
            entry = {'year': current_year + year}
            
            if year < duration:
                entry['phase'] = 'Education'
                entry['milestones'] = [
                    f"Year {year + 1} of {education_path.degree_name}",
                    f"Focus on: {education_path.recommended_majors[year % len(education_path.recommended_majors)]}"
                ]
            else:
                entry['phase'] = 'Career'
                career_year = year - duration
                entry['milestones'] = [
                    f"{'Junior' if career_year < 2 else 'Senior'} {career_path.title}",
                    "Develop professional network"
                ]
            
            timeline.append(entry)
        
        return timeline
    
    def _generate_salary_projection(self, career_path):
        # Simplified salary projection logic
        base_salary = self._parse_salary(career_path.salary_range)
        projections = []
        
        for year in range(10):
            salary = base_salary * (1.05 ** year)  # 5% annual growth
            projections.append({
                'year': datetime.now().year + year,
                'salary': round(salary),
                'factors': ["Annual performance increase"]
            })
        
        return projections
    
    def _parse_salary(self, salary_range):
        try:
            parts = salary_range.replace('$', '').replace(',', '').split('-')
            return (float(parts[0]) + float(parts[1])) / 2
        except:
            return 60000  # Default fallback