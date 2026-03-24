from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_userprofile_role_change_approval"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="role_change_reviewed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="role_change_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "No request"),
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("rejected", "Rejected"),
                ],
                default="",
                max_length=20,
            ),
        ),
    ]
