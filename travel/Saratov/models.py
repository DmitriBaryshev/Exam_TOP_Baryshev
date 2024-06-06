from django.db import models
from django.contrib.auth.models import AbstractUser


class Saratov(models.Model):
    title = models.CharField(max_length=655)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)


class User(AbstractUser):
    pass


class BlogMessage(models.Model):
    objects = models.Manager()

    # hidden
    sender = models.ForeignKey('User', on_delete=models.PROTECT)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    # form
    text = models.CharField(
        verbose_name='Содержание', max_length=1028
    )

    def __str__(self):
        return f'<BLOG {self.sender}>'
