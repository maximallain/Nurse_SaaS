from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import time

class Interval(models.Model):
    
    WeekDay_Choices = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    
    start_time = models.PositiveIntegerField(validators=[MaxValueValidator(95)],null=True)
    end_time = models.PositiveIntegerField(validators=[MaxValueValidator(96)], null=True)
    weekday = models.CharField(max_length=2, choices=WeekDay_Choices, null=True)
    #Définition de l'unicité d'un intervalle définit par start_time et end_time
    class Meta:
        unique_together = ["start_time", "end_time", "weekday"]


    @property
    def real_start_time(self):
        return convert_to_real_time(self.start_time)
    
    @property
    def real_end_time(self):
        return convert_to_real_time(self.end_time)

def convert_to_real_time(number):
        """Method that takes a integer as parameter and that calculate the real time based on around fifteen"""
        return time(hour=number//4, minute=(number%4)*15).isoformat(timespec='minutes')



        



