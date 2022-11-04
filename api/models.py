
from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    profilepic = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    members = models.IntegerField()
    admin = models.CharField(max_length=100)


class User(models.Model):
    name = models.CharField(max_length=50)
    account = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    profilepic = models.CharField(max_length=200)


class Post(models.Model):
    content = models.CharField(max_length=500)
    club = models.IntegerField()
    posted_by = models.CharField(max_length=100)
    likes = models.ManyToManyField(User, blank=True)

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    clubId = models.IntegerField()
    postId = models.IntegerField()
    commented_by = models.CharField(max_length=50)
    comment = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
