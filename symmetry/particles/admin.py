from django.contrib import admin
from .models import EParticle, CParticle, Interaction, DecayMode

# Register your models here.

@admin.register(EParticle)
class EParticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'mass', 'charge', 'spin', 'particle_type')
    list_filter = ('particle_type', 'is_antiparticle')
    search_fields = ('name', 'particle_type')

@admin.register(CParticle)
class CParticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'mass', 'charge', 'spin', 'total_isospin')
    filter_horizontal = ('constituents',)
    search_fields = ('name',)

class ParticleListFilter(admin.SimpleListFilter):
    title = 'particle type'
    parameter_name = 'particle_type'

    def lookups(self, request, model_admin):
        return (
            ('eparticle', 'Elementary Particles'),
            ('cparticle', 'Composite Particles'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'eparticle':
            return queryset.instance_of(EParticle)
        if self.value() == 'cparticle':
            return queryset.instance_of(CParticle)

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'force', 'coupling_constant')
    list_filter = ('force', ParticleListFilter)
    filter_horizontal = ('particles',)

@admin.register(DecayMode)
class DecayModeAdmin(admin.ModelAdmin):
    list_display = ('parent', 'get_products', 'branching_ratio')
    list_filter = (ParticleListFilter,)
    filter_horizontal = ('products',)

    def get_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])
    get_products.short_description = 'Products'
