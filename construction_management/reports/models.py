from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    name = models.CharField(max_length=255)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_generated = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/')
    
    def __str__(self):
        return self.name
