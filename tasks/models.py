from django.db import models
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(default="", null=False)
    description = models.TextField(null=True)
    creation_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed')
        ]
    )

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



