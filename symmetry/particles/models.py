from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Particle(models.Model):
    name = models.CharField(max_length=100)
    mass = models.FloatField(validators=[MinValueValidator(0.0)], help_text="Mass in MeV/c^2")
    charge = models.FloatField(choices=[
        (-1, '-1 (Negative)'),
        (-2/3, '-2/3'),
        (-1/3, '-1/3'),
        (0, '0 (Neutral)'),
        (1/3, '1/3'),
        (2/3, '2/3'),
        (1, '+1 (Positive)'),
    ])
    spin = models.CharField(max_length=10)
    lifetime = models.FloatField(validators=[MinValueValidator(0.0)], help_text="Lifetime in seconds")
    
    def __str__(self):
        return f"{self.name}, Mass: {self.mass} MeV/c^2, Charge: {self.charge}, Spin: {self.spin}"

    def mass_in_kg(self):
        return self.mass * 1.78266192e-30  # Conversion factor from MeV/c^2 to kg

class EParticle(Particle):
    PARTICLE_TYPES = [
        ('quark', 'Quark'),
        ('lepton', 'Lepton'),
        ('gauge_boson', 'Gauge Boson'),
        ('scalar_boson', 'Scalar Boson'),
    ]
    particle_type = models.CharField(max_length=20, choices=PARTICLE_TYPES)
    antiparticle = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='antiparticle_of')
    is_antiparticle = models.BooleanField(default=False)

    lepton_number = models.IntegerField(default=0)
    baryon_number = models.FloatField(default=0)
    isospin = models.FloatField(null=True, blank=True)
    strangeness = models.IntegerField(default=0)
    charm = models.IntegerField(default=0)
    bottomness = models.IntegerField(default=0)
    topness = models.IntegerField(default=0)

    def clean(self):
        super().clean()
        if self.antiparticle:
            if self.antiparticle == self:
                raise ValidationError("A particle cannot be its own antiparticle.")
            if self.antiparticle.antiparticle and self.antiparticle.antiparticle != self:
                raise ValidationError("Inconsistent antiparticle relationship.")
        
        if self.particle_type == 'quark':
            if self.baryon_number not in [-1/3, 1/3]:
                raise ValidationError("Quarks must have baryon number of +1/3 or -1/3")
        elif self.particle_type == 'lepton':
            if self.lepton_number not in [-1, 1]:
                raise ValidationError("Leptons must have lepton number of +1 or -1")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        if self.antiparticle and self.antiparticle.antiparticle != self:
            self.antiparticle.antiparticle = self
            self.antiparticle.save()

class CParticle(Particle):
    constituents = models.ManyToManyField(EParticle, related_name='composite_particles')
    
    total_isospin = models.FloatField(null=True, blank=True)
    total_angular_momentum = models.FloatField(null=True, blank=True)
    parity = models.IntegerField(choices=[(1, '+1'), (-1, '-1')], null=True, blank=True)
    
    def calculate_properties(self):
        # Implement the calculation of properties here
        pass

    def save(self, *args, **kwargs):
        self.calculate_properties()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.constituents.exists():
            raise ValidationError("A composite particle must have at least one constituent.")

    class Meta:
        verbose_name = "Composite Particle"
        verbose_name_plural = "Composite Particles"

class Interaction(models.Model):
    name = models.CharField(max_length=100)
    particles = models.ManyToManyField(Particle, related_name='interactions')
    description = models.TextField()
    force = models.CharField(max_length=50, choices=[
        ('strong', 'Strong Nuclear'),
        ('weak', 'Weak Nuclear'),
        ('electromagnetic', 'Electromagnetic')
    ])
    coupling_constant = models.FloatField(null=True, blank=True)
    conservation_rules = models.TextField(help_text="Describe what quantities are conserved in this interaction")

    def __str__(self):
        return f"{self.name} ({self.force})"

class DecayMode(models.Model):
    parent = models.ForeignKey(Particle, on_delete=models.CASCADE, related_name='decay_modes')
    products = models.ManyToManyField(Particle, related_name='product_of')
    branching_ratio = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    def clean(self):
        # ... (keep the existing clean method)
        pass

    def __str__(self):
        product_names = ', '.join(p.name for p in self.products.all())
        return f"{self.parent.name} -> {product_names} (BR: {self.branching_ratio:.2%})"