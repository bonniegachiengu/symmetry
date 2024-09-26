from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import EParticle

# Create your views here.

class ParticleListView(ListView):
    model = EParticle
    template_name = 'particles/particle_list.html'
    context_object_name = 'particles'

class ParticleDetailView(DetailView):
    model = EParticle
    template_name = 'particles/particle_detail.html'
    context_object_name = 'particle'
