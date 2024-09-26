import csv
import os
from django.core.management.base import BaseCommand
from fractions import Fraction
from particles.models import EParticle

class Command(BaseCommand):
    help = 'Import particle data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, nargs='?', default='particle_data.csv', 
                            help='Name of the CSV file in the management/commands directory')

    def handle(self, *args, **options):
        csv_file_name = options['csv_file']
        csv_file_path = os.path.join(os.path.dirname(__file__), csv_file_name)

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
            return

        def parse_fraction(value):
            if value == '':
                return None
            try:
                return float(value)
            except ValueError:
                return float(Fraction(value))

        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                particle, created = EParticle.objects.update_or_create(
                    name=row['name'],
                    defaults={
                        'mass': float(row['mass']),
                        'charge': parse_fraction(row['charge']),
                        'spin': row['spin'],
                        'particle_type': row['particle_type'],
                        'lepton_number': int(row['lepton_number']),
                        'baryon_number': parse_fraction(row['baryon_number']),
                        'isospin': parse_fraction(row['isospin']),
                        'strangeness': int(row['strangeness']),
                        'charm': int(row['charm']),
                        'bottomness': int(row['bottomness']),
                        'topness': int(row['topness']),
                        'lifetime': float(row['lifetime']) if row['lifetime'] != 'inf' else float('inf'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created particle: {particle.name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated particle: {particle.name}'))

        self.stdout.write(self.style.SUCCESS('Particle import completed'))