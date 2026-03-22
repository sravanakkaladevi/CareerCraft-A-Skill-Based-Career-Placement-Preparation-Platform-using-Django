from django.db import models


class SiteBranding(models.Model):
    company_name = models.CharField(max_length=80, default="CareerCraft")
    tagline = models.CharField(
        max_length=140,
        default="Skill-Based Placement Prep Platform",
    )
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site branding"
        verbose_name_plural = "Site branding"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        defaults = {
            "company_name": "CareerCraft",
            "tagline": "Skill-Based Placement Prep Platform",
        }
        return cls.objects.get_or_create(pk=1, defaults=defaults)[0]
