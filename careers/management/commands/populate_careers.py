from django.core.management.base import BaseCommand
from careers.models import Industry, Career

class Command(BaseCommand):
    help = 'Populates the database with initial Industries and Careers'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating careers...')

        # Define Data
        data = {
            'Technology': [
                {
                    'title': 'Data Scientist',
                    'description': 'Analyze complex data to help organizations make better decisions.',
                    'education': 'Bachelor/Master in Computer Science or Statistics',
                    'salary': 'RM 4,000 - RM 8,000',
                    'outlook': 'High demand across all sectors.',
                    'trait': 'ANALYTICAL'
                },
                {
                    'title': 'Software Developer',
                    'description': 'Design, build, and maintain software applications.',
                    'education': 'Bachelor in Computer Science or Software Engineering',
                    'salary': 'RM 3,500 - RM 7,000',
                    'outlook': 'Growing rapidly with digital transformation.',
                    'trait': 'TECHNICAL'
                },
            ],
            'Arts & Design': [
                {
                    'title': 'Graphic Designer',
                    'description': 'Create visual concepts to communicate ideas that inspire and inform.',
                    'education': 'Diploma/Degree in Graphic Design',
                    'salary': 'RM 2,500 - RM 5,000',
                    'outlook': 'Steady demand in marketing and advertising.',
                    'trait': 'CREATIVE'
                },
            ],
            'Human Services': [
                {
                    'title': 'Social Worker',
                    'description': 'Help people solve and cope with problems in their everyday lives.',
                    'education': 'Degree in Social Work or Psychology',
                    'salary': 'RM 2,800 - RM 4,500',
                    'outlook': 'Stable demand in healthcare and community services.',
                    'trait': 'SOCIAL'
                },
            ],
            'Business': [
                {
                    'title': 'Project Manager',
                    'description': 'Plan and oversee projects to ensure they are completed in a timely fashion.',
                    'education': 'Degree in Business Administration or Management',
                    'salary': 'RM 5,000 - RM 10,000',
                    'outlook': 'Essential role in many large organizations.',
                    'trait': 'STRUCTURED'
                }
            ]
        }

        count = 0
        for industry_name, careers in data.items():
            industry, _ = Industry.objects.get_or_create(name=industry_name)
            
            for c in careers:
                Career.objects.get_or_create(
                    title=c['title'],
                    defaults={
                        'industry': industry,
                        'description': c['description'],
                        'education_required': c['education'],
                        'salary_range': c['salary'],
                        'outlook': c['outlook'],
                        'primary_trait': c['trait']
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} careers and related industries.'))
