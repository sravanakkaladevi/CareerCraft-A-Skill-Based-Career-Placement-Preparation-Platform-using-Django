from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_userprofile_personalization"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="pending_experience_level",
            field=models.CharField(
                blank=True,
                choices=[("fresher", "Fresher"), ("experienced", "Experienced")],
                default="",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="pending_target_domain",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Select domain"),
                    ("web", "Web Development"),
                    ("ai_ml", "AI / ML"),
                    ("data_science", "Data Science"),
                    ("cloud", "Cloud / DevOps"),
                    ("cybersecurity", "Cybersecurity"),
                    ("android", "Android"),
                    ("careertech", "CareerTech"),
                    ("edtech", "EdTech"),
                ],
                default="",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="pending_target_role",
            field=models.CharField(
                blank=True,
                choices=[
                    ("frontend", "Frontend Developer"),
                    ("backend", "Backend Developer"),
                    ("fullstack", "Full Stack Developer"),
                    ("data", "Data Analyst"),
                    ("ai_ml", "AI / ML Engineer"),
                    ("devops", "DevOps / Cloud Engineer"),
                    ("cybersecurity", "Cybersecurity Analyst"),
                    ("mobile", "Android Developer"),
                ],
                default="",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="role_change_requested_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
