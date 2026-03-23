from django.contrib.auth.models import User
from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default="DEV")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    color = models.CharField(max_length=20, default="#2563EB")
    tutorial_url = models.URLField(blank=True)
    cheatsheet_url = models.URLField(blank=True)
    practice_url = models.URLField(blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Topic(models.Model):
    LEVEL = [("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced")]
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="learn_topics/", blank=True, null=True)
    level = models.CharField(max_length=20, choices=LEVEL, default="beginner")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.language.name} - {self.title}"


class Lesson(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    theory = models.TextField()
    content_image = models.ImageField(upload_to="learn_lessons/", blank=True, null=True)
    image_caption = models.CharField(max_length=255, blank=True)
    syntax_example = models.TextField(blank=True)
    practice_note = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class LessonImage(models.Model):
    ALIGNMENT = [
        ("left", "Left"),
        ("center", "Center"),
        ("right", "Right"),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_images")
    image = models.ImageField(upload_to="learn_lesson_gallery/")
    caption = models.CharField(max_length=255, blank=True)
    alignment = models.CharField(max_length=10, choices=ALIGNMENT, default="center")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.lesson.title} image {self.order}"


class BlogPost(models.Model):
    CATEGORY = [
        ("ai", "AI Tools"),
        ("tech", "Tech Updates"),
        ("career", "Career Tips"),
        ("placement", "Placement Tips"),
        ("interview", "Interview Prep"),
    ]
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=20, choices=CATEGORY, default="tech")
    cover_image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_time = models.IntegerField(default=3)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=800)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} on {self.post.title}"

    @property
    def like_count(self):
        return self.reactions.filter(value=1).count()

    @property
    def dislike_count(self):
        return self.reactions.filter(value=-1).count()


class BlogCommentReaction(models.Model):
    VALUE_CHOICES = [
        (1, "Like"),
        (-1, "Dislike"),
    ]

    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["comment", "user"]

    def __str__(self):
        label = "Like" if self.value == 1 else "Dislike"
        return f"{self.user.username} - {label}"
