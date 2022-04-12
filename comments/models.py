from django.db import models


class Comment(models.Model):
    # comment's user
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=60)
    text = models.TextField()
    # comment's time
    created_time = models.DateTimeField(auto_now_add=True)
    # comment is one to many
    blog = models.ForeignKey('project.Bloginfo', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_time']
        verbose_name = "Comments"
        verbose_name_plural = verbose_name

