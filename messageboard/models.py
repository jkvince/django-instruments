from django.db import models
from django.urls import reverse
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(
        'accounts.CustomUser',
        on_delete = models.CASCADE
    )
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title[:50]

    def get_absolute_url(self):
        return reverse('messageboard:post_detail', args=[str(self.id)])


class Comment(models.Model):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    author = models.ForeignKey(
        'accounts.CustomUser',
        on_delete = models.CASCADE
    )
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("messageboard:post_list")