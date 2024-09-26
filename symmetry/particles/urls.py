from django.urls import path
from .views import ParticleListView, ParticleDetailView

urlpatterns = [
    path('', ParticleListView.as_view(), name='particle_list'),
    path('<int:pk>/', ParticleDetailView.as_view(), name='particle_detail'),
]