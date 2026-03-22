from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    theme_color = models.CharField(max_length=7, default='#185FA5')

    def __str__(self):
        return f"{self.user.username} profile"
