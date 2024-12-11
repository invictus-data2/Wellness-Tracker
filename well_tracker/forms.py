from django import forms
from .models import PreSessionMetrics, PostSessionMetrics

class PreForm(forms.ModelForm):
    class Meta:
        model = PreSessionMetrics
        fields = ['client_name', 'coach_name', 'date', 'weight', 'sleep', 'soreness', 'mental_stress', 'fatigue', 'pain_scale', 'stiffness', 'grip_strength', 'rhr', 'sleep_quantity']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Custom date input widget
        }
       

class PostForm(forms.ModelForm):
    class Meta:
        model = PostSessionMetrics
        fields = ['client_name', 'coach_name', 'date', 'rpe', 'pain_scale', 'session_duration', 'avg_HR']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Custom date input widget
        }
        
        # Comment
