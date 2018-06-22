from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post

class Friend(models.Model):
    users = models.ManyToManyField(User, related_name='friends')
    me = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='owner')

    @classmethod
    def make_friend(cls, me, new_friend):
        friend, created = cls.objects.get_or_create(
            me=me,
        )
        friend.users.add(new_friend)
        friend.save()

    @classmethod
    def unfriend(cls, me, new_friend):
        friend, created = cls.objects.get_or_create(
            me=me,
        )
        friend.users.remove(new_friend)
        friend.save()

    def __str__(self):
        return self.me
