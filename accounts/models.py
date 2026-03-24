from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    TARGET_ROLE_CHOICES = [
        ("frontend", "Frontend Developer"),
        ("backend", "Backend Developer"),
        ("fullstack", "Full Stack Developer"),
        ("data", "Data Analyst"),
        ("ai_ml", "AI / ML Engineer"),
        ("devops", "DevOps / Cloud Engineer"),
        ("cybersecurity", "Cybersecurity Analyst"),
        ("mobile", "Android Developer"),
    ]
    TARGET_DOMAIN_CHOICES = [
        ("", "Select domain"),
        ("web", "Web Development"),
        ("ai_ml", "AI / ML"),
        ("data_science", "Data Science"),
        ("cloud", "Cloud / DevOps"),
        ("cybersecurity", "Cybersecurity"),
        ("android", "Android"),
        ("careertech", "CareerTech"),
        ("edtech", "EdTech"),
    ]
    EXPERIENCE_CHOICES = [
        ("fresher", "Fresher"),
        ("experienced", "Experienced"),
    ]
    ROLE_CHANGE_STATUS_CHOICES = [
        ("", "No request"),
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    theme_color = models.CharField(max_length=7, default='#185FA5')
    target_role = models.CharField(max_length=30, choices=TARGET_ROLE_CHOICES, blank=True, default='')
    target_domain = models.CharField(max_length=30, choices=TARGET_DOMAIN_CHOICES, blank=True, default='')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    pending_target_role = models.CharField(max_length=30, choices=TARGET_ROLE_CHOICES, blank=True, default='')
    pending_target_domain = models.CharField(max_length=30, choices=TARGET_DOMAIN_CHOICES, blank=True, default='')
    pending_experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, blank=True, default='')
    role_change_status = models.CharField(max_length=20, choices=ROLE_CHANGE_STATUS_CHOICES, blank=True, default='')
    role_change_requested_at = models.DateTimeField(blank=True, null=True)
    role_change_reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profile"

    @property
    def is_profile_complete(self):
        return bool(self.target_role and self.target_domain and self.experience_level)

    @property
    def has_pending_role_change(self):
        return self.role_change_status == 'pending'
