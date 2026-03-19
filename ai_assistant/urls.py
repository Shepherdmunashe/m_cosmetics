from django.urls import path
from . import views

urlpatterns = [
    path('admin/ai-assistant/', views.ai_panel, name='ai_panel'),
    path('admin/ai-assistant/generate/', views.ai_generate, name='ai_generate'),
]
