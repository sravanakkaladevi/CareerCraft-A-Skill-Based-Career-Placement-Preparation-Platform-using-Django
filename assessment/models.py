from django.db import models
from django.contrib.auth.models import User


class SkillTopic(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='📊')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class SkillQuestion(models.Model):
    DIFFICULTY = [('easy','Easy'),('medium','Medium'),('hard','Hard')]
    topic = models.ForeignKey(SkillTopic, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=400)
    option_b = models.CharField(max_length=400)
    option_c = models.CharField(max_length=400)
    option_d = models.CharField(max_length=400)
    correct_option = models.CharField(max_length=1)
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, default='medium')

    def __str__(self):
        return self.question_text[:60]


class SkillScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(SkillTopic, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    percentage = models.IntegerField()
    assessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-assessed_at']

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - {self.percentage}%"

    @classmethod
    def get_latest_per_topic(cls, user):
        topics = SkillTopic.objects.all()
        results = []
        for topic in topics:
            latest = cls.objects.filter(user=user, topic=topic).first()
            results.append({
                'topic': topic,
                'score': latest,
            })
        return results