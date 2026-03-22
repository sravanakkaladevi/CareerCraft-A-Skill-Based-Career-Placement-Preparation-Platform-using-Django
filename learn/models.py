from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='💻')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    color = models.CharField(max_length=20, default='#2563EB')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Topic(models.Model):
    LEVEL = [('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced')]
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=LEVEL, default='beginner')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.language.name} — {self.title}"


class Lesson(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    theory = models.TextField()
    syntax_example = models.TextField(blank=True)
    practice_note = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    CATEGORY = [
        ('ai', 'AI Tools'),
        ('tech', 'Tech Updates'),
        ('career', 'Career Tips'),
        ('placement', 'Placement Tips'),
        ('interview', 'Interview Prep'),
    ]
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=20, choices=CATEGORY, default='tech')
    cover_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_time = models.IntegerField(default=3)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=800)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.post.title}"
