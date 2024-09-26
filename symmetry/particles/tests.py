from django.test import TestCase
from .models import EParticle, Fermion, Boson

# Create your tests here.

class ParticleModelTests(TestCase):
    def test_create_fermion(self):
        fermion = Fermion.objects.create(name="Electron", mass=9.1e-31, charge=-1, spin="1/2")
        self.assertEqual(fermion.particle_type, 'fermion')

    # Add more tests...
