"""
Management command to populate the database with predefined government institutions.
"""
from django.core.management.base import BaseCommand
from institutions.models import Institution, InstitutionCategory


class Command(BaseCommand):
    help = 'Populates the database with predefined government institutions'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating institutions...')

        # Define institutions
        institutions_data = [
            # Presidency and Top Level
            {'name': 'Office of the Presidency', 'type': 'department', 'description': 'Executive office of the President'},
            {'name': 'Office of the Vice Presidency', 'type': 'department', 'description': 'Executive office of the Vice President'},
            {'name': 'Council of Ministers', 'type': 'department', 'description': 'Cabinet of government ministers'},

            # Ministries
            {'name': 'Ministry of Interior', 'type': 'ministry', 'description': 'Internal affairs and domestic security'},
            {'name': 'Ministry of Finance', 'type': 'ministry', 'description': 'National budget and economic policy'},
            {'name': 'Ministry of Justice', 'type': 'ministry', 'description': 'Legal affairs and judicial system'},
            {'name': 'Ministry of Health', 'type': 'ministry', 'description': 'Public health and medical services'},
            {'name': 'Ministry of Education', 'type': 'ministry', 'description': 'Education policy and schools'},
            {'name': 'Ministry of Agriculture', 'type': 'ministry', 'description': 'Agricultural development and food security'},
            {'name': 'Ministry of Energy', 'type': 'ministry', 'description': 'Energy production and distribution'},
            {'name': 'Ministry of Transport', 'type': 'ministry', 'description': 'Transportation infrastructure and services'},
            {'name': 'Ministry of Information and Communication Technology', 'type': 'ministry', 'description': 'ICT development and digital services'},
            {'name': 'Ministry of Environment', 'type': 'ministry', 'description': 'Environmental protection and conservation'},
            {'name': 'Ministry of Foreign Affairs', 'type': 'ministry', 'description': 'International relations and diplomacy'},
            {'name': 'Ministry of Defense', 'type': 'ministry', 'description': 'National defense and military affairs'},

            # Security Agencies
            {'name': 'National Armed Forces', 'type': 'agency', 'description': 'Military defense forces'},
            {'name': 'National Police Service', 'type': 'agency', 'description': 'Law enforcement and public safety'},
            {'name': 'Coast Guard', 'type': 'agency', 'description': 'Maritime security and safety'},
            {'name': 'Intelligence Agency', 'type': 'agency', 'description': 'National intelligence and security'},

            # Economic Bodies
            {'name': 'Central Bank', 'type': 'authority', 'description': 'Monetary policy and financial regulation'},
            {'name': 'Revenue Authority', 'type': 'authority', 'description': 'Tax collection and revenue management'},
            {'name': 'Public Procurement Agency', 'type': 'agency', 'description': 'Government procurement oversight'},

            # Independent Commissions
            {'name': 'Electoral Commission', 'type': 'commission', 'description': 'Elections management and oversight'},
            {'name': 'Human Rights Commission', 'type': 'commission', 'description': 'Protection of human rights'},
            {'name': 'Anti-Corruption Commission', 'type': 'commission', 'description': 'Fighting corruption and fraud'},

            # Education and Research
            {'name': 'National University', 'type': 'other', 'description': 'Higher education institution'},
            {'name': 'National Statistics Office', 'type': 'agency', 'description': 'National statistics and data'},

            # Infrastructure and Utilities
            {'name': 'Water and Sanitation Authority', 'type': 'authority', 'description': 'Water supply and sanitation services'},
            {'name': 'National Electricity Company', 'type': 'other', 'description': 'Electricity generation and distribution'},
            {'name': 'Roads and Infrastructure Authority', 'type': 'authority', 'description': 'Road construction and maintenance'},
        ]

        created_count = 0
        updated_count = 0

        for inst_data in institutions_data:
            institution, created = Institution.objects.get_or_create(
                name=inst_data['name'],
                defaults={
                    'institution_type': inst_data['type'],
                    'description': inst_data['description'],
                    'is_active': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {institution.name}'))
            else:
                # Update existing institution
                institution.institution_type = inst_data['type']
                institution.description = inst_data['description']
                institution.is_active = True
                institution.save()
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated: {institution.name}'))

        # Create categories
        categories_data = [
            {
                'name': 'Executive',
                'description': 'Executive branch offices',
                'institutions': ['Office of the Presidency', 'Office of the Vice Presidency', 'Council of Ministers']
            },
            {
                'name': 'Security & Defense',
                'description': 'Security and defense agencies',
                'institutions': ['National Armed Forces', 'National Police Service', 'Coast Guard', 'Intelligence Agency', 'Ministry of Defense']
            },
            {
                'name': 'Economic Affairs',
                'description': 'Economic and financial institutions',
                'institutions': ['Central Bank', 'Revenue Authority', 'Ministry of Finance', 'Public Procurement Agency']
            },
            {
                'name': 'Social Services',
                'description': 'Health, education, and social welfare',
                'institutions': ['Ministry of Health', 'Ministry of Education', 'National University']
            },
            {
                'name': 'Infrastructure',
                'description': 'Infrastructure and utilities',
                'institutions': ['Ministry of Energy', 'Ministry of Transport', 'Water and Sanitation Authority',
                               'National Electricity Company', 'Roads and Infrastructure Authority']
            },
            {
                'name': 'Independent Bodies',
                'description': 'Independent commissions and oversight bodies',
                'institutions': ['Electoral Commission', 'Human Rights Commission', 'Anti-Corruption Commission']
            },
        ]

        cat_created_count = 0
        for cat_data in categories_data:
            category, created = InstitutionCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )

            if created:
                cat_created_count += 1

            # Add institutions to category
            for inst_name in cat_data['institutions']:
                try:
                    institution = Institution.objects.get(name=inst_name)
                    category.institutions.add(institution)
                except Institution.DoesNotExist:
                    pass

            category.save()

        self.stdout.write(self.style.SUCCESS(f'\n✓ Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  - Created {created_count} new institutions'))
        self.stdout.write(self.style.SUCCESS(f'  - Updated {updated_count} existing institutions'))
        self.stdout.write(self.style.SUCCESS(f'  - Created/updated {cat_created_count} categories'))
        self.stdout.write(self.style.SUCCESS(f'\n✓ Database population complete!'))
