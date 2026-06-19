from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=100)
    sets = models.IntegerField()
    reps = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.exercise
    
class Diet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.food_name
    
class WeightProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.weight)
    
class ProgressPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='progress_photos/')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username