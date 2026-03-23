import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0005_topic_summary_topic_cover_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='learn_lesson_gallery/')),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('alignment', models.CharField(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], default='center', max_length=10)),
                ('order', models.IntegerField(default=0)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_images', to='learn.lesson')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
    ]
