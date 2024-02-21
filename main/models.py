# models.py
from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    classes_done = models.PositiveIntegerField(default=0)
    classes_attended = models.PositiveIntegerField(default=0)

    def calculate_percentage(self):
        var=round((self.classes_attended / self.classes_done) * 100,2) if self.classes_done != 0 else 0
        formatted_percentage = '{:.2f}'.format(var)
        return (formatted_percentage ) 

class Feedback(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)