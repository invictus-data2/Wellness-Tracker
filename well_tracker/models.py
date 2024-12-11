from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class PreSessionMetrics(models.Model):
    client_name = models.CharField(max_length=100, blank= False, null= False)
    coach_name = models.CharField(max_length=100, blank= False, null= False)
    date = models.DateField(default=timezone.now)
    weight = models.FloatField(blank= True, null= True)
    sleep = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank= False, null= False)
    soreness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank= False, null= False)
    mental_stress = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank= False, null= False)
    fatigue = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank= False, null= False)
    pain_scale = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank= False, null= False)
    stiffness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank= False, null= False)
    composite_score = models.FloatField(blank= False, null= False) 
    grip_strength = models.FloatField(blank=True, null=True)
    rhr = models.FloatField(blank= True, null= True)
    sleep_quantity = models.FloatField(blank= True, null= True)
 
    def __str__(self):
        return self.client_name

class PostSessionMetrics(models.Model):
    client_name = models.CharField(max_length=100, blank= False, null= False)
    coach_name = models.CharField(max_length=100, blank= False, null= False)
    date = models.DateField(default=timezone.now)
    rpe = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=False, null=False)
    pain_scale = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=False, null=False)
    session_duration = models.IntegerField(validators=[MinValueValidator(1)], help_text="Enter session duration in minutes only.", blank=False, null=False)
    avg_HR = models.FloatField(default=0)
    acwr_rpe = models.FloatField(default=0)
    acwr_HR = models.FloatField(default=0)
    def __str__(self):
        return self.client_name
