from django.core.management.base import BaseCommand
from assessment.models import Question

class Command(BaseCommand):
    help = 'Populates the database with initial assessment questions'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating questions...')
        
        # Interest Questions (Likert 1-5)
        interest_questions = [
            # Analytical
            {'text': 'Analyzing data to solve complex problems', 'trait': 'ANALYTICAL'},
            {'text': 'Conducting scientific experiments', 'trait': 'ANALYTICAL'},
            
            # Creative
            {'text': 'Designing graphics or digital art', 'trait': 'CREATIVE'},
            {'text': 'Writing stories or articles', 'trait': 'CREATIVE'},
            
            # Social
            {'text': 'Teaching people new skills', 'trait': 'SOCIAL'},
            {'text': 'Helping others with personal problems', 'trait': 'SOCIAL'},
            
            # Technical
            {'text': 'Building or repairing electronic devices', 'trait': 'TECHNICAL'},
            {'text': 'Programming software applications', 'trait': 'TECHNICAL'},
            
            # Structured
            {'text': 'Organizing files and records efficiently', 'trait': 'STRUCTURED'},
            {'text': 'Creating detailed project plans', 'trait': 'STRUCTURED'},
        ]

        created_count = 0
        for idx, q_data in enumerate(interest_questions):
            q, created = Question.objects.get_or_create(
                text=q_data['text'],
                defaults={
                    'question_type': Question.Type.INTEREST,
                    'primary_trait': q_data['trait'],
                    'order': idx + 1
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} questions.'))
