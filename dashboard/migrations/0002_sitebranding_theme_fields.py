from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitebranding",
            name="admin_accent_color",
            field=models.CharField(default="#378ADD", max_length=7),
        ),
        migrations.AddField(
            model_name="sitebranding",
            name="admin_background_color",
            field=models.CharField(default="#0F172A", max_length=7),
        ),
        migrations.AddField(
            model_name="sitebranding",
            name="admin_primary_color",
            field=models.CharField(default="#185FA5", max_length=7),
        ),
        migrations.AddField(
            model_name="sitebranding",
            name="admin_surface_color",
            field=models.CharField(default="#1E293B", max_length=7),
        ),
    ]
