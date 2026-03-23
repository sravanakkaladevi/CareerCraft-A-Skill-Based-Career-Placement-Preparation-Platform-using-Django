from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0004_language_cheatsheet_url_language_practice_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='learn_topics/'),
        ),
        migrations.AddField(
            model_name='topic',
            name='summary',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='content_image',
            field=models.ImageField(blank=True, null=True, upload_to='learn_lessons/'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='image_caption',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
